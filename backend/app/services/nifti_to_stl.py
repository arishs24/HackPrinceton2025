"""
Service to segment NIfTI files and convert brain regions to STL files
This integrates the segmentation scripts into the backend service
"""
import os
import subprocess
import sys
import nibabel as nib
import numpy as np
from skimage import measure
import trimesh
from pathlib import Path
from typing import List, Dict, Optional

# Brain region labels mapping
REGION_LABELS = {
    0: "Background",
    1: "CSF_(Cerebrospinal_Fluid)",
    2: "Gray_Matter",
    3: "White_Matter",
    4: "Deep_Gray_Matter",
    5: "Brain_Stem",
    6: "Cerebellum",
    10: "Left_Thalamus",
    11: "Left_Caudate",
    12: "Left_Putamen",
    13: "Left_Pallidum",
    14: "3rd_Ventricle",
    15: "4th_Ventricle",
    16: "Brain_Stem",
    17: "Left_Hippocampus",
    18: "Left_Amygdala",
    26: "Left_Accumbens_area",
    28: "Left_VentralDC",
    31: "Left_choroid_plexus",
    41: "Right_Cerebral_White_Matter",
    42: "Right_Cerebral_Cortex",
    43: "Right_Lateral_Ventricle",
    44: "Right_Inf_Lat_Vent",
    46: "Right_Cerebellum_White_Matter",
    47: "Right_Cerebellum_Cortex",
    49: "Right_Thalamus",
    50: "Right_Caudate",
    51: "Right_Putamen",
    52: "Right_Pallidum",
    53: "Right_Hippocampus",
    54: "Right_Amygdala",
    58: "Right_Accumbens_area",
    60: "Right_VentralDC",
    63: "Right_choroid_plexus",
    173: "Hypothalamus",
    174: "Left_Hypothalamus",
    175: "Right_Hypothalamus",
}


def segment_nifti_to_regions(input_file: str, output_dir: str) -> Optional[str]:
    """
    Segment a NIfTI file into brain regions using SynthSeg or alternative methods.
    Returns path to segmented file, or None if failed.
    """
    os.makedirs(output_dir, exist_ok=True)
    segmented_output = os.path.join(output_dir, "segmented_brain.nii.gz")
    
    # Check if SynthSeg is available
    base_dir = Path(__file__).parent.parent.parent.parent  # Go up to project root
    synthseg_dir = base_dir / "SynthSeg"
    script_path = synthseg_dir / "scripts" / "commands" / "SynthSeg_predict.py"
    
    if script_path.exists():
        try:
            print(f"Using SynthSeg to segment {input_file}...")
            cmd = [
                sys.executable,
                str(script_path),
                "--i", input_file,
                "--o", segmented_output,
                "--parc"
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(synthseg_dir),
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0 and os.path.exists(segmented_output):
                print(f"Segmentation complete: {segmented_output}")
                return segmented_output
            else:
                print(f"SynthSeg error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("SynthSeg timed out")
        except Exception as e:
            print(f"SynthSeg error: {e}")
    
    # Fallback: Use simple thresholding-based segmentation
    print("Using fallback segmentation method...")
    try:
        return segment_with_thresholding(input_file, segmented_output)
    except Exception as e:
        print(f"Fallback segmentation failed: {e}")
        return None


def segment_with_thresholding(input_file: str, output_file: str) -> str:
    """
    Simple thresholding-based segmentation as fallback.
    Creates basic tissue type labels.
    """
    img = nib.load(input_file)
    data = img.get_fdata()
    
    # Normalize
    data_norm = (data - data.min()) / (data.max() - data.min() + 1e-8)
    
    # Simple thresholding for tissue types
    segmented = np.zeros_like(data, dtype=np.int32)
    
    # Background
    segmented[data_norm < 0.1] = 0
    # CSF
    segmented[(data_norm >= 0.1) & (data_norm < 0.3)] = 1
    # Gray Matter
    segmented[(data_norm >= 0.3) & (data_norm < 0.6)] = 2
    # White Matter
    segmented[(data_norm >= 0.6) & (data_norm < 0.8)] = 3
    # Deep structures (simplified)
    segmented[data_norm >= 0.8] = 4
    
    # Save segmented image
    seg_img = nib.Nifti1Image(segmented, img.affine, img.header)
    nib.save(seg_img, output_file)
    
    return output_file


def extract_regions_to_nifti(segmented_file: str, output_dir: str) -> Dict[int, Dict]:
    """
    Extract individual brain regions from segmented file as separate NIfTI files.
    Returns dictionary mapping label to region info.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    seg_img = nib.load(segmented_file)
    seg_data = seg_img.get_fdata().astype(np.int32)
    
    unique_labels = np.unique(seg_data)
    unique_labels = unique_labels[unique_labels > 0]  # Remove background
    
    extracted_regions = {}
    
    for label in unique_labels:
        region_mask = (seg_data == label).astype(np.float32)
        
        if np.sum(region_mask) < 100:  # Skip tiny regions
            continue
        
        region_img = nib.Nifti1Image(region_mask, seg_img.affine, seg_img.header)
        
        region_name = REGION_LABELS.get(int(label), f"Region_{int(label)}")
        safe_name = region_name.replace(" ", "_").replace("/", "_")
        filename = f"{safe_name}_{int(label)}.nii.gz"
        filepath = os.path.join(output_dir, filename)
        
        nib.save(region_img, filepath)
        extracted_regions[int(label)] = {
            'name': region_name,
            'file': filepath,
            'voxels': int(np.sum(region_mask))
        }
    
    return extracted_regions


def nifti_to_stl(nifti_file: str, stl_file: str, iso_level: float = 0.5) -> bool:
    """
    Convert a NIfTI file to STL format using marching cubes.
    Returns True if successful.
    """
    try:
        img = nib.load(nifti_file)
        data = img.get_fdata()
        
        if np.count_nonzero(data) < 100:
            return False
        
        # Get spacing from header
        spacing = img.header.get_zooms()[:3]
        
        # Marching cubes
        verts, faces, normals, values = measure.marching_cubes(
            data,
            level=iso_level,
            spacing=spacing
        )
        
        if len(verts) == 0:
            return False
        
        # Create trimesh
        mesh = trimesh.Trimesh(vertices=verts, faces=faces, vertex_normals=normals)
        
        # Export STL
        mesh.export(stl_file)
        
        return True
    except Exception as e:
        print(f"Error converting {nifti_file} to STL: {e}")
        return False


def process_nifti_to_stl_files(
    input_file: str,
    case_id: str,
    stl_base_dir: str = "stl"
) -> List[Dict[str, str]]:
    """
    Main function: Process NIfTI file -> Segment -> Extract regions -> Convert to STL.
    Returns list of STL file info dictionaries.
    """
    # Create case-specific directories
    case_stl_dir = os.path.join(stl_base_dir, case_id)
    temp_seg_dir = os.path.join("temp_seg", case_id)
    os.makedirs(case_stl_dir, exist_ok=True)
    os.makedirs(temp_seg_dir, exist_ok=True)
    
    # Step 1: Segment the brain
    segmented_file = segment_nifti_to_regions(input_file, temp_seg_dir)
    if not segmented_file or not os.path.exists(segmented_file):
        raise RuntimeError("Segmentation failed")
    
    # Step 2: Extract individual regions
    regions = extract_regions_to_nifti(segmented_file, temp_seg_dir)
    
    # Step 3: Convert each region to STL
    stl_files = []
    for label, region_info in regions.items():
        nifti_path = region_info['file']
        region_name = region_info['name']
        
        # Create STL filename
        safe_name = region_name.replace(" ", "_").replace("/", "_")
        stl_filename = f"{safe_name}.stl"
        stl_path = os.path.join(case_stl_dir, stl_filename)
        
        # Convert to STL
        if nifti_to_stl(nifti_path, stl_path):
            stl_files.append({
                'filename': stl_filename,
                'path': stl_path,
                'name': region_name,
                'label': label,
                'voxels': region_info['voxels']
            })
            print(f"Created STL: {stl_filename}")
    
    return stl_files

