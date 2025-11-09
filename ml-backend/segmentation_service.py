"""
Segmentation service that uses the existing segmentation scripts
"""
import os
import sys
import subprocess
import nibabel as nib
import numpy as np
from skimage import measure
import trimesh
from pathlib import Path
from typing import List, Dict, Optional

# Import functions from existing scripts
# We'll call the scripts as subprocesses or import their functions
def run_segmentation_script(input_file: str, output_dir: str) -> Optional[str]:
    """
    Run the existing segment_brain_regions.py script
    Returns path to segmented file
    """
    base_dir = Path(__file__).parent.parent
    segmented_output = os.path.join(output_dir, "segmented_brain.nii.gz")
    
    try:
        # Add parent directory to path to import the script
        sys.path.insert(0, str(base_dir))
        from segment_brain_regions import (
            segment_with_synthseg,
            check_synthseg_installed
        )
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if SynthSeg is available
        if not check_synthseg_installed():
            print("SynthSeg not found, using fallback...")
            # Try alternative method
            from segment_brain_regions import segment_with_alternative
            if segment_with_alternative(input_file, segmented_output):
                return segmented_output
            return None
        
        # Run segmentation
        if segment_with_synthseg(input_file, segmented_output):
            return segmented_output
        else:
            # Try alternative if SynthSeg fails
            from segment_brain_regions import segment_with_alternative
            if segment_with_alternative(input_file, segmented_output):
                return segmented_output
            return None
            
    except ImportError as e:
        print(f"Could not import segmentation functions: {e}")
        return None
    except Exception as e:
        print(f"Segmentation error: {e}")
        return None


def extract_regions_to_nifti(segmented_file: str, output_dir: str) -> Dict[int, Dict]:
    """
    Extract individual brain regions from segmented file
    Uses the existing extract_regions function
    """
    try:
        base_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(base_dir))
        from segment_brain_regions import extract_regions
        
        regions = extract_regions(segmented_file, output_dir)
        return regions
    except Exception as e:
        print(f"Error extracting regions: {e}")
        return {}


def nifti_to_stl(nifti_file: str, stl_file: str, iso_level: float = 0.5) -> bool:
    """
    Convert NIfTI file to STL using marching cubes
    Uses the same approach as make_3d_model.py
    """
    try:
        img = nib.load(nifti_file)
        data = img.get_fdata()
        
        if np.count_nonzero(data) < 100:
            return False
        
        # Get spacing from header
        spacing = img.header.get_zooms()[:3]
        
        # Marching cubes (same as make_3d_model.py)
        verts, faces, normals, values = measure.marching_cubes(
            data,
            level=iso_level,
            spacing=spacing
        )
        
        if len(verts) == 0:
            return False
        
        # Create trimesh (same as make_3d_model.py)
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
    Main function: Process NIfTI -> Segment -> Extract regions -> Convert to STL
    Uses existing segmentation scripts
    """
    # Create case-specific directories
    case_stl_dir = os.path.join(stl_base_dir, case_id)
    temp_seg_dir = os.path.join("temp_seg", case_id)
    os.makedirs(case_stl_dir, exist_ok=True)
    os.makedirs(temp_seg_dir, exist_ok=True)
    
    # Step 1: Segment the brain using existing script
    segmented_file = run_segmentation_script(input_file, temp_seg_dir)
    if not segmented_file or not os.path.exists(segmented_file):
        raise RuntimeError("Segmentation failed")
    
    # Step 2: Extract individual regions using existing function
    regions = extract_regions_to_nifti(segmented_file, temp_seg_dir)
    
    # Step 3: Convert each region to STL (same as make_3d_model.py)
    stl_files = []
    for label, region_info in regions.items():
        nifti_path = region_info['file']
        region_name = region_info['name']
        
        # Create STL filename (same naming as make_3d_model.py)
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

