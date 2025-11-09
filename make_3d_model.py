import nibabel as nib
import numpy as np
from skimage import measure
import trimesh
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# --- CONFIG ---
seg_dir = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\segmented_regions"
output_mesh = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\combined_brain_mesh.stl"
output_dir = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\3d_meshes"

os.makedirs(output_dir, exist_ok=True)

# Color mapping for different brain regions
region_colors = {
    'gray': (0.8, 0.8, 0.8, 0.7),
    'white': (1.0, 1.0, 0.9, 0.7),
    'deep': (0.6, 0.4, 0.8, 0.8),
    'brainstem': (1.0, 0.4, 0.4, 0.8),
    'cerebellum': (0.4, 0.8, 0.4, 0.8),
    'thalamus': (1.0, 0.6, 0.2, 0.8),
    # Brain lobes
    'frontal': (1.0, 0.3, 0.3, 0.8),
    'temporal': (0.3, 0.8, 0.3, 0.8),
    'parietal': (0.3, 0.3, 1.0, 0.8),
    'occipital': (1.0, 0.8, 0.3, 0.8),
    'default': (0.7, 0.7, 0.7, 0.6)
}

def get_color_for_region(fname):
    """Get color based on region name"""
    fname_lower = fname.lower()
    # Check for lobes first
    if 'frontal' in fname_lower:
        return region_colors['frontal']
    elif 'temporal' in fname_lower:
        return region_colors['temporal']
    elif 'parietal' in fname_lower:
        return region_colors['parietal']
    elif 'occipital' in fname_lower:
        return region_colors['occipital']
    elif 'gray' in fname_lower and 'deep' not in fname_lower:
        return region_colors['gray']
    elif 'white' in fname_lower:
        return region_colors['white']
    elif 'deep' in fname_lower:
        return region_colors['deep']
    elif 'brainstem' in fname_lower or 'brain_stem' in fname_lower:
        return region_colors['brainstem']
    elif 'cerebellum' in fname_lower:
        return region_colors['cerebellum']
    elif 'thalamus' in fname_lower:
        return region_colors['thalamus']
    else:
        return region_colors['default']

# --- Process all segmented region files ---
all_meshes = []
mesh_info = []

# Get all NIfTI files except the full segmentation and CSF
nii_files = [f for f in os.listdir(seg_dir) 
             if f.endswith(".nii.gz") 
             and f != "segmented_brain.nii.gz"
             and "csf" not in f.lower() 
             and "cerebrospinal" not in f.lower()]

print(f"Found {len(nii_files)} region files to process (CSF excluded)...\n")

for fname in sorted(nii_files):
    path = os.path.join(seg_dir, fname)
    print(f"Processing {fname}...")
    
    try:
        img = nib.load(path)
        data = img.get_fdata()
        
        if np.count_nonzero(data) < 100:
            print(f"  Skipping {fname}: empty or tiny segmentation")
            continue

        # Use marching cubes to create 3D mesh
        iso = 0.5
        verts, faces, normals, values = measure.marching_cubes(data, level=iso, spacing=img.header.get_zooms()[:3])
        
        if len(verts) == 0:
            print(f"  Skipping {fname}: no vertices generated")
            continue
        
        # Get color for this region
        color = get_color_for_region(fname)
        
        # Create trimesh object
        mesh = trimesh.Trimesh(vertices=verts, faces=faces, vertex_normals=normals)
        
        # Apply color to vertices
        mesh.visual.vertex_colors = [int(c * 255) for c in color[:3]] * len(mesh.vertices)
        
        all_meshes.append(mesh)
        
        # Save individual mesh
        try:
            region_name = fname.replace('.nii.gz', '').replace(' ', '_')
            individual_mesh_path = os.path.join(output_dir, f"{region_name}.stl")
            mesh.export(individual_mesh_path)
        except Exception as e:
            print(f"  Warning: Could not save individual mesh: {e}")
            individual_mesh_path = None
        
        mesh_info.append({
            'name': fname,
            'vertices': len(verts),
            'faces': len(faces),
            'color': color
        })
        
        print(f"  Added {fname} ({len(verts)} vertices, {len(faces)} faces)")
        
    except Exception as e:
        print(f"  Error processing {fname}: {e}")
        continue

if not all_meshes:
    raise RuntimeError("No brain region segmentations found in folder")

print(f"\n{'='*60}")
print(f"Successfully processed {len(all_meshes)} brain regions")
print(f"{'='*60}\n")

# Combine all meshes
print("Combining all meshes...")
combined_mesh = trimesh.util.concatenate(all_meshes)
combined_mesh.export(output_mesh)
print(f"Saved combined 3D mesh: {output_mesh}\n")

# --- Create 3D visualization ---
print("Creating 3D visualization...")
fig = plt.figure(figsize=(16, 12))

# Create 4 subplots for different views
views = [
    (90, 0, "Front View"),
    (0, 0, "Top View"),
    (0, 90, "Side View"),
    (45, 45, "Isometric View")
]

for idx, (elev, azim, title) in enumerate(views, 1):
    ax = fig.add_subplot(2, 2, idx, projection='3d')
    
    for i, (mesh, info) in enumerate(zip(all_meshes, mesh_info)):
        # Create poly collection for this mesh
        poly3d = Poly3DCollection(
            mesh.vertices[mesh.faces],
            alpha=info['color'][3],
            facecolor=info['color'][:3],
            edgecolor='none',
            linewidths=0.1
        )
        ax.add_collection3d(poly3d)
    
    # Set equal aspect ratio
    bounds = combined_mesh.bounds
    center = combined_mesh.centroid
    max_range = np.array([bounds[1] - bounds[0]]).max() / 2.0
    ax.set_xlim(center[0] - max_range, center[0] + max_range)
    ax.set_ylim(center[1] - max_range, center[1] + max_range)
    ax.set_zlim(center[2] - max_range, center[2] + max_range)
    
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title, fontsize=12, fontweight='bold')

plt.suptitle('3D Brain Region Segmentation (CSF Excluded)', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()

# Save the visualization
viz_path = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\brain_3d_visualization.png"
plt.savefig(viz_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved visualization: {viz_path}\n")

# Print summary
print(f"{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"Total regions: {len(all_meshes)}")
print(f"Combined mesh: {output_mesh}")
print(f"Individual meshes: {output_dir}")
print(f"Visualization: {viz_path}")
print(f"\nRegions processed:")
for info in mesh_info:
    print(f"  - {info['name']}: {info['vertices']:,} vertices, {info['faces']:,} faces")

print(f"\n{'='*60}")
print("3D visualization complete!")
print(f"{'='*60}\n")
