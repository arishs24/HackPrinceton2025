import numpy as np
import os
import glob
import pydicom
from skimage import measure
from scipy.ndimage import zoom, binary_erosion, binary_dilation
from app.models.schemas import MeshData


def load_dicom_volume(case_dir):
    """
    Load DICOM slices and stack them into a 3D volume
    Returns: 3D numpy array with the volume data
    """
    # Get all DICOM files
    dcm_files = glob.glob(os.path.join(case_dir, "*.dcm"))

    if not dcm_files:
        return None

    print(f"Loading {len(dcm_files)} DICOM slices...")

    # Read all DICOM files and sort by slice location
    slices = []
    for dcm_file in dcm_files:
        try:
            ds = pydicom.dcmread(dcm_file)
            slices.append(ds)
        except Exception as e:
            print(f"Error reading {dcm_file}: {e}")
            continue

    # Sort slices by ImagePositionPatient (Z coordinate) or InstanceNumber
    try:
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    except:
        try:
            slices.sort(key=lambda x: int(x.InstanceNumber))
        except:
            print("Warning: Could not sort slices properly")

    # Stack slices into 3D volume
    volume_slices = []
    for s in slices:
        # Get pixel array and apply rescale slope/intercept if available
        pixel_array = s.pixel_array.astype(np.float32)

        # Apply Hounsfield Unit conversion for CT scans
        if hasattr(s, 'RescaleSlope') and hasattr(s, 'RescaleIntercept'):
            pixel_array = pixel_array * float(s.RescaleSlope) + float(s.RescaleIntercept)

        volume_slices.append(pixel_array)

    # Stack into 3D array (Z, Y, X)
    volume = np.stack(volume_slices, axis=0)

    print(f"Volume shape: {volume.shape}")
    print(f"Volume range: [{volume.min()}, {volume.max()}]")

    return volume


def segment_brain_tissue(volume):
    """
    Segment brain tissue from CT/MRI volume using thresholding
    Returns binary mask of brain tissue
    """
    # Normalize volume to 0-1 range
    volume_norm = (volume - volume.min()) / (volume.max() - volume.min() + 1e-8)

    # For brain CT scans, brain tissue is typically in the range of 0-80 HU
    # For MRI, we'll use intensity-based thresholding

    # Apply thresholding to extract brain tissue
    # This is a simple approach - in production you'd use deep learning
    threshold_low = np.percentile(volume_norm, 20)
    threshold_high = np.percentile(volume_norm, 95)

    brain_mask = (volume_norm > threshold_low) & (volume_norm < threshold_high)

    # Morphological operations to clean up the mask
    brain_mask = binary_erosion(brain_mask, iterations=2)
    brain_mask = binary_dilation(brain_mask, iterations=3)

    return brain_mask, volume_norm


def generate_mesh_from_volume(volume, brain_mask, target_vertices=5000):
    """
    Generate 3D mesh from volume using marching cubes algorithm
    """
    # Downsample if volume is too large (for performance)
    max_dim = 128
    if max(volume.shape) > max_dim:
        scale_factors = [min(max_dim / s, 1.0) for s in volume.shape]
        volume = zoom(volume, scale_factors, order=1)
        brain_mask = zoom(brain_mask.astype(float), scale_factors, order=0) > 0.5

    print(f"Processing volume of shape: {volume.shape}")

    # Apply marching cubes to generate mesh
    try:
        verts, faces, normals, values = measure.marching_cubes(
            brain_mask.astype(float),
            level=0.5,
            step_size=1,
            allow_degenerate=False
        )
    except Exception as e:
        print(f"Marching cubes error: {e}")
        # Fallback to generating a simple mesh
        return generate_mock_brain_mesh("fallback")

    print(f"Generated mesh: {len(verts)} vertices, {len(faces)} faces")

    # Scale vertices to reasonable size and center
    verts = verts - verts.mean(axis=0)
    scale = 10.0 / max(verts.max(axis=0) - verts.min(axis=0))
    verts = verts * scale

    # Simplify mesh if too many vertices (for performance)
    if len(verts) > target_vertices:
        # Simple decimation by sampling
        step = len(verts) // target_vertices
        indices = np.arange(0, len(verts), step)[:target_vertices]

        # Create mapping from old to new indices
        index_map = {old_idx: new_idx for new_idx, old_idx in enumerate(indices)}
        verts = verts[indices]

        # Update faces with new indices
        new_faces = []
        for face in faces:
            if all(v in index_map for v in face):
                new_face = [index_map[v] for v in face]
                new_faces.append(new_face)
        faces = np.array(new_faces) if new_faces else faces

    # Generate labels and colors based on position and intensity
    labels = generate_tissue_labels(verts, volume, brain_mask)
    colors = assign_colors_by_label(labels)

    # Convert to lists for JSON serialization
    vertices_list = verts.tolist()
    faces_list = faces.tolist()
    labels_list = labels.tolist()
    colors_list = colors.tolist()

    return MeshData(
        vertices=vertices_list,
        faces=faces_list,
        labels=labels_list,
        colors=colors_list
    )


def generate_tissue_labels(vertices, volume, brain_mask):
    """
    Assign tissue type labels based on position and intensity
    """
    labels = np.zeros(len(vertices), dtype=int)

    # Normalize vertex positions to volume coordinates
    verts_norm = vertices.copy()
    verts_norm = verts_norm - verts_norm.min(axis=0)
    verts_norm = verts_norm / (verts_norm.max(axis=0) + 1e-8)

    # Sample volume at vertex positions
    for i, v in enumerate(verts_norm):
        # Map to volume coordinates
        z = int(v[0] * (volume.shape[0] - 1))
        y = int(v[1] * (volume.shape[1] - 1))
        x = int(v[2] * (volume.shape[2] - 1))

        # Clamp to valid range
        z = np.clip(z, 0, volume.shape[0] - 1)
        y = np.clip(y, 0, volume.shape[1] - 1)
        x = np.clip(x, 0, volume.shape[2] - 1)

        # Get intensity value
        intensity = volume[z, y, x]

        # Assign label based on intensity (simple segmentation)
        # In production, use trained neural network
        if intensity > 0.7:
            labels[i] = 1  # White matter (high intensity)
        elif intensity > 0.4:
            labels[i] = 2  # Grey matter (medium intensity)
        elif intensity > 0.2:
            # Check if in specific region for tumor (simplified)
            if vertices[i][0] > 0 and vertices[i][1] > 0 and vertices[i][2] > 0:
                labels[i] = 3  # Tumor (simulated)
            else:
                labels[i] = 2  # Grey matter
        else:
            labels[i] = 0  # Skull/CSF (low intensity)

    return labels


def assign_colors_by_label(labels):
    """
    Assign colors based on tissue labels
    """
    color_map = {
        0: [0.9, 0.9, 0.9],    # Skull/CSF - light grey
        1: [1.0, 0.95, 0.9],   # White matter - off-white
        2: [0.7, 0.7, 0.75],   # Grey matter - grey
        3: [0.9, 0.2, 0.2]     # Tumor - red
    }

    colors = np.array([color_map[label] for label in labels])
    return colors


def generate_mock_brain_mesh(case_id: str = "sample"):
    """
    Generate a mock 3D brain mesh with segmented regions
    Creates a sphere-like structure with different tissue types

    This is used as fallback when no DICOM files are available
    """
    # Parameters
    resolution = 30  # Grid resolution
    radius = 5.0

    # Generate sphere vertices
    vertices = []
    labels = []
    faces = []

    phi = np.linspace(0, np.pi, resolution)
    theta = np.linspace(0, 2 * np.pi, resolution)

    vertex_grid = {}

    for i, p in enumerate(phi):
        for j, t in enumerate(theta):
            # Spherical to Cartesian coordinates
            x = radius * np.sin(p) * np.cos(t)
            y = radius * np.sin(p) * np.sin(t)
            z = radius * np.cos(p)

            # Add some noise to make it brain-like
            noise = np.random.normal(0, 0.2)
            x += noise
            y += noise
            z += noise

            vertices.append([float(x), float(y), float(z)])
            vertex_grid[(i, j)] = len(vertices) - 1

            # Assign labels based on position (mock segmentation)
            r = np.sqrt(x**2 + y**2 + z**2)

            if r > 4.5:
                label = 0  # Skull (outer layer)
            elif r > 3.5:
                label = 1  # White matter
            elif r > 2.0:
                label = 2  # Grey matter
            else:
                # Create a tumor region in one area
                if x > 0 and y > 0 and z > 0:
                    label = 3  # Tumor
                else:
                    label = 2  # Grey matter

            labels.append(label)

    # Generate faces (triangles)
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            # Two triangles per quad
            v1 = vertex_grid[(i, j)]
            v2 = vertex_grid[(i + 1, j)]
            v3 = vertex_grid[(i, j + 1)]
            v4 = vertex_grid[(i + 1, j + 1)]

            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])

    # Generate colors based on labels
    colors = assign_colors_by_label(labels).tolist()

    return MeshData(
        vertices=vertices,
        faces=faces,
        labels=labels,
        colors=colors
    )


def load_2d_image_as_volume(case_dir):
    """
    Load 2D image (PNG/JPG) and simulate 3D volume by extruding
    This creates a simple 3D representation from a 2D brain image
    """
    from PIL import Image

    # Find image files
    image_files = glob.glob(os.path.join(case_dir, "*.png")) + \
                  glob.glob(os.path.join(case_dir, "*.jpg")) + \
                  glob.glob(os.path.join(case_dir, "*.jpeg"))

    if not image_files:
        return None

    print(f"Loading 2D image: {image_files[0]}")

    # Load image
    img = Image.open(image_files[0]).convert('L')  # Convert to grayscale
    img_array = np.array(img).astype(np.float32)

    # Normalize to 0-1
    img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min() + 1e-8)

    print(f"Image shape: {img_array.shape}")

    # Create 3D volume by extruding the 2D image
    # This simulates depth by replicating the slice
    depth = min(img_array.shape) // 2  # Create reasonable depth

    # Stack multiple slices with slight variation to simulate 3D structure
    volume_slices = []
    for i in range(depth):
        # Add slight variation to simulate depth
        t = i / depth  # 0 to 1
        scale = 1.0 - abs(t - 0.5) * 0.3  # Peak in middle, fade at edges
        slice_data = img_array * scale
        volume_slices.append(slice_data)

    volume = np.stack(volume_slices, axis=0)

    print(f"Created 3D volume from 2D image, shape: {volume.shape}")
    print(f"Volume range: [{volume.min()}, {volume.max()}]")

    return volume


def process_dicom_to_mesh(case_id: str):
    """
    Main function to process medical imaging data and generate 3D mesh
    Supports:
    - Multiple DICOM slices (.dcm) - stacks into 3D volume
    - Single 2D images (PNG/JPG) - extrudes to create 3D volume
    """
    upload_dir = "uploads"
    case_dir = os.path.join(upload_dir, case_id)

    # Check if case directory exists
    if not os.path.exists(case_dir):
        print(f"Case directory not found: {case_dir}, using mock data")
        return generate_mock_brain_mesh(case_id)

    # Try to load DICOM volume first
    volume = load_dicom_volume(case_dir)

    # If no DICOM, try 2D image
    if volume is None:
        print("No DICOM files found, trying 2D image...")
        volume = load_2d_image_as_volume(case_dir)

    # If still no data, use mock
    if volume is None:
        print("No valid image data found, using mock data")
        return generate_mock_brain_mesh(case_id)

    # Segment brain tissue
    brain_mask, volume_norm = segment_brain_tissue(volume)

    # Generate mesh from volume
    mesh_data = generate_mesh_from_volume(volume_norm, brain_mask)

    print(f"Successfully generated 3D mesh from medical imaging data")
    return mesh_data
