# Brain Region Segmentation

This tool segments brain MRI scans (NIfTI format) into multiple anatomical regions including:
- Thalamus (left and right)
- Hypothalamus
- Hippocampus
- Amygdala
- Caudate
- Putamen
- Pallidum
- And many more...

## Installation

### Option 1: Using SynthSeg (Recommended)

```bash
pip install -r requirements_segmentation.txt
```

Or install manually:
```bash
pip install synthseg tensorflow nibabel numpy scipy scikit-image
```

### Option 2: Using ANTsPyNet (Alternative)

```bash
pip install antspynet
```

## Usage

### Basic Usage

```bash
python segment_brain_regions.py
```

The script will:
1. Load your brain scan (`IXI648-Guys-1107-T1.nii.gz`)
2. Segment it into multiple brain regions
3. Extract each region as a separate NIfTI file
4. Generate a summary report

### Output

The script creates a `segmented_regions/` directory containing:
- `segmented_brain.nii.gz` - Full segmentation with all regions labeled
- Individual region files (e.g., `Left_Thalamus_10.nii.gz`, `Right_Thalamus_49.nii.gz`)
- `segmentation_report.txt` - Summary of all segmented regions

## Configuration

Edit the script to change:
- `INPUT_FILE`: Path to your brain scan
- `OUTPUT_DIR`: Where to save segmented regions

## Troubleshooting

### SynthSeg Installation Issues

If SynthSeg fails to install:
1. Make sure you have Python 3.8+
2. Install TensorFlow separately: `pip install tensorflow`
3. Try: `pip install synthseg --no-cache-dir`

### Memory Issues

If you run out of memory:
- The script uses "fast" mode by default
- For very large files, you may need to resize the input first

### Alternative Tools

If SynthSeg doesn't work, the script will try:
- ANTsPyNet (requires separate installation)
- Other available segmentation tools

## References

- SynthSeg: https://github.com/BBillot/SynthSeg
- ANTsPyNet: https://github.com/ANTsX/ANTsPyNet

