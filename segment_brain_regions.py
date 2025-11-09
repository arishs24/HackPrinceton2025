"""
Brain Region Segmentation Script
Segments a brain MRI scan into multiple regions (thalamus, hypothalamus, etc.)
Uses SynthSeg for comprehensive brain segmentation
"""

import os
import sys
import subprocess
import nibabel as nib
import numpy as np
from pathlib import Path

# Configuration
INPUT_FILE = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\IXI648-Guys-1107-T1.nii.gz"
OUTPUT_DIR = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\segmented_regions"
SEGMENTED_OUTPUT = os.path.join(OUTPUT_DIR, "segmented_brain.nii.gz")

# Brain region labels
# Note: SynthSeg provides anatomical regions (thalamus, hypothalamus, etc.)
# ANTsPyNet deep_atropos provides tissue types (CSF, gray matter, white matter, etc.)
REGION_LABELS = {
    # Tissue types (from ANTsPyNet deep_atropos)
    0: "Background",
    1: "CSF (Cerebrospinal Fluid)",
    2: "Gray Matter",
    3: "White Matter",
    4: "Deep Gray Matter",
    5: "Brain Stem",
    6: "Cerebellum",
    # Anatomical regions (from SynthSeg - if available)
    10: "Left Thalamus",
    11: "Left Caudate",
    12: "Left Putamen",
    13: "Left Pallidum",
    14: "3rd Ventricle",
    15: "4th Ventricle",
    16: "Brain Stem",
    17: "Left Hippocampus",
    18: "Left Amygdala",
    26: "Left Accumbens area",
    28: "Left VentralDC",
    31: "Left choroid plexus",
    41: "Right Cerebral White Matter",
    42: "Right Cerebral Cortex",
    43: "Right Lateral Ventricle",
    44: "Right Inf Lat Vent",
    46: "Right Cerebellum White Matter",
    47: "Right Cerebellum Cortex",
    49: "Right Thalamus",
    50: "Right Caudate",
    51: "Right Putamen",
    52: "Right Pallidum",
    53: "Right Hippocampus",
    54: "Right Amygdala",
    58: "Right Accumbens area",
    60: "Right VentralDC",
    63: "Right choroid plexus",
    # Additional labels for hypothalamus and other regions
    173: "Hypothalamus",
    174: "Left Hypothalamus",
    175: "Right Hypothalamus",
}

def check_synthseg_installed():
    """Check if SynthSeg is installed"""
    # Check if SynthSeg directory exists
    synthseg_dir = os.path.join(os.path.dirname(__file__), "SynthSeg")
    if os.path.exists(synthseg_dir):
        # Check if the main script exists
        script_path = os.path.join(synthseg_dir, "scripts", "commands", "SynthSeg_predict.py")
        if os.path.exists(script_path):
            return True
    return False

def install_synthseg():
    """Install SynthSeg from GitHub"""
    print("SynthSeg needs to be cloned from GitHub...")
    synthseg_dir = os.path.join(os.path.dirname(__file__), "SynthSeg")
    
    if os.path.exists(synthseg_dir):
        print(f"SynthSeg directory found at {synthseg_dir}")
        return True
    
    print("Cloning SynthSeg from GitHub...")
    print("This may take a few minutes...")
    try:
        import git
        repo_url = "https://github.com/BBillot/SynthSeg.git"
        git.Repo.clone_from(repo_url, synthseg_dir)
        print("SynthSeg cloned successfully!")
        
        # Install dependencies
        req_file = os.path.join(synthseg_dir, "requirements.txt")
        if os.path.exists(req_file):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        else:
            # Install basic dependencies
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "nibabel", "numpy", "scipy", "scikit-image", 
                                 "tensorflow", "gitpython", "--upgrade"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
        return True
    except ImportError:
        # gitpython not installed, try manual clone instructions
        print("gitpython not available. Installing it...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            return install_synthseg()  # Retry
        except:
            print("\nPlease install SynthSeg manually:")
            print("   git clone https://github.com/BBillot/SynthSeg.git")
            print("   cd SynthSeg")
            print("   pip install -r requirements.txt")
            return False
    except Exception as e:
        print(f"Error installing SynthSeg: {e}")
        print("\nPlease install SynthSeg manually:")
        print("   git clone https://github.com/BBillot/SynthSeg.git")
        print("   cd SynthSeg")
        print("   pip install -r requirements.txt")
        return False

def segment_with_synthseg(input_file, output_file):
    """Segment brain using SynthSeg"""
    try:
        print(f"Starting segmentation of {input_file}...")
        print("This may take a few minutes (especially on first run as models download)...")
        
        # Get SynthSeg directory
        synthseg_dir = os.path.join(os.path.dirname(__file__), "SynthSeg")
        script_path = os.path.join(synthseg_dir, "scripts", "commands", "SynthSeg_predict.py")
        
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"SynthSeg script not found at {script_path}")
        
        # Run SynthSeg using command line
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            sys.executable,
            script_path,
            "--i", input_file,
            "--o", output_file,
            "--parc"  # Enable cortical parcellation for lobes
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=synthseg_dir)
        
        if result.returncode == 0:
            print(f"Segmentation complete! Output saved to {output_file}")
            return True
        else:
            print(f"SynthSeg error: {result.stderr}")
            raise RuntimeError("SynthSeg segmentation failed")
            
    except FileNotFoundError as e:
        print(f"SynthSeg not found: {e}")
        print("Trying alternative method...")
        return segment_with_alternative(input_file, output_file)
    except Exception as e:
        print(f"Error during segmentation: {e}")
        import traceback
        traceback.print_exc()
        print("\nTrying alternative method...")
        return segment_with_alternative(input_file, output_file)

def segment_with_alternative(input_file, output_file):
    """Alternative segmentation method using available tools"""
    try:
        # Try using ANTsPyNet if available
        import ants
        import antspynet
        print("Using ANTsPyNet for brain segmentation...")
        print("This may take several minutes (models will download on first run)...")
        
        # Load image with ANTs
        print("Loading brain image...")
        img = ants.image_read(input_file)
        
        # Use deepAtropos for brain segmentation
        # This automatically downloads models on first run
        try:
            print("Running deepAtropos segmentation (this may take 5-10 minutes)...")
            seg_dict = antspynet.deep_atropos(img, do_preprocessing=True, verbose=True)
            
            # deep_atropos returns a dictionary with multiple segmentations
            # We need to combine them into a single labeled image
            print("Combining segmentations into single labeled image...")
            
            # Get the segmentation image (usually the 'segmentation' key or combine all)
            if isinstance(seg_dict, dict):
                # Create a combined segmentation with labels
                # Common keys: 'segmentation', 'background', 'csf', 'gray_matter', 'white_matter', etc.
                if 'segmentation' in seg_dict:
                    seg = seg_dict['segmentation']
                else:
                    # Combine all segmentations into one labeled image
                    # Start with background (label 0)
                    seg = ants.image_clone(img) * 0
                    
                    # Label map for tissue types
                    label_map = {
                        'background': 0,
                        'csf': 1,
                        'gray_matter': 2,
                        'white_matter': 3,
                        'deep_gray_matter': 4,
                        'brain_stem': 5,
                        'cerebellum': 6
                    }
                    
                    # Find the maximum probability for each voxel and assign label
                    # Create a list of all tissue images
                    import numpy as np
                    tissue_images = []
                    tissue_labels = []
                    
                    # Get all tissue probability maps
                    for key, tissue_img in seg_dict.items():
                        if key in label_map:
                            try:
                                tissue_np = tissue_img.numpy() if hasattr(tissue_img, 'numpy') else np.array(tissue_img)
                                tissue_images.append(tissue_np)
                                tissue_labels.append(label_map[key])
                            except:
                                pass
                    
                    if tissue_images:
                        # Stack all probability maps
                        prob_stack = np.stack(tissue_images, axis=-1)
                        # Get the label with maximum probability for each voxel
                        max_idx = np.argmax(prob_stack, axis=-1)
                        # Create labeled image
                        seg_numpy = np.zeros_like(tissue_images[0], dtype=np.int32)
                        for i, label in enumerate(tissue_labels):
                            seg_numpy[max_idx == i] = label
                        
                        # Convert back to ANTs image
                        seg = ants.from_numpy(seg_numpy, origin=img.origin, 
                                            spacing=img.spacing, direction=img.direction)
                    else:
                        # Fallback: use first available image
                        seg = list(seg_dict.values())[0]
            else:
                seg = seg_dict
            
            # Save segmentation
            print(f"Saving segmentation to {output_file}...")
            ants.image_write(seg, output_file)
            print(f"Segmentation complete using ANTsPyNet!")
            return True
        except Exception as e:
            print(f"ANTsPyNet segmentation error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except ImportError as e:
        print(f"ANTsPyNet not available: {e}")
        print("Please install: pip install antspynet")
        return False
    except Exception as e:
        print(f"Alternative method failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def extract_regions(segmented_file, output_dir):
    """Extract individual brain regions from the segmented file"""
    print("\nExtracting individual brain regions...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load segmented image
    seg_img = nib.load(segmented_file)
    seg_data = seg_img.get_fdata().astype(np.int32)
    
    # Get unique labels
    unique_labels = np.unique(seg_data)
    unique_labels = unique_labels[unique_labels > 0]  # Remove background
    
    print(f"Found {len(unique_labels)} unique brain regions")
    
    extracted_regions = {}
    
    for label in unique_labels:
        # Create binary mask for this region
        region_mask = (seg_data == label).astype(np.float32)
        
        if np.sum(region_mask) > 0:  # Only save if region exists
            # Create NIfTI image for this region
            region_img = nib.Nifti1Image(region_mask, seg_img.affine, seg_img.header)
            
            # Get region name
            region_name = REGION_LABELS.get(int(label), f"Region_{int(label)}")
            # Clean filename
            safe_name = region_name.replace(" ", "_").replace("/", "_")
            filename = f"{safe_name}_{int(label)}.nii.gz"
            filepath = os.path.join(output_dir, filename)
            
            # Save region
            nib.save(region_img, filepath)
            extracted_regions[int(label)] = {
                'name': region_name,
                'file': filepath,
                'voxels': int(np.sum(region_mask))
            }
            
            print(f"  Extracted: {region_name} ({int(np.sum(region_mask))} voxels)")
    
    return extracted_regions

def create_summary_report(regions, output_dir):
    """Create a summary report of segmented regions"""
    report_path = os.path.join(output_dir, "segmentation_report.txt")
    
    with open(report_path, 'w') as f:
        f.write("Brain Segmentation Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total regions segmented: {len(regions)}\n\n")
        f.write("Regions:\n")
        f.write("-" * 50 + "\n")
        
        # Sort by label value
        for label in sorted(regions.keys()):
            region = regions[label]
            f.write(f"Label {label:3d}: {region['name']:40s} - {region['voxels']:8d} voxels\n")
    
    print(f"\nSummary report saved to: {report_path}")

def main():
    """Main function"""
    print("=" * 60)
    print("Brain Region Segmentation Tool")
    print("=" * 60)
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found: {INPUT_FILE}")
        return
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check and install SynthSeg if needed
    if not check_synthseg_installed():
        print("SynthSeg not found. Installing...")
        if not install_synthseg():
            print("Failed to install SynthSeg. Please install manually:")
            print("   pip install synthseg")
            return
    
    # Perform segmentation
    if not segment_with_synthseg(INPUT_FILE, SEGMENTED_OUTPUT):
        print("Segmentation failed!")
        return
    
    # Extract individual regions
    regions = extract_regions(SEGMENTED_OUTPUT, OUTPUT_DIR)
    
    # Create summary report
    create_summary_report(regions, OUTPUT_DIR)
    
    print("\n" + "=" * 60)
    print("Segmentation complete!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    # Print key regions
    print("\nKey regions found:")
    key_regions = ['Thalamus', 'Hypothalamus', 'Hippocampus', 'Amygdala', 'Caudate', 'Putamen']
    for label, region in regions.items():
        if any(key in region['name'] for key in key_regions):
            print(f"  • {region['name']}: {region['voxels']} voxels")

if __name__ == "__main__":
    main()

