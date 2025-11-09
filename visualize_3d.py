"""
Quick 3D visualization of brain meshes
"""
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# Load the combined mesh
mesh_path = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\combined_brain_mesh.stl"
mesh_dir = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\3d_meshes"

print("Loading 3D meshes...")

# Load individual meshes with colors
region_colors = {
    'csf': (0.2, 0.6, 1.0, 0.6),
    'gray': (0.8, 0.8, 0.8, 0.7),
    'white': (1.0, 1.0, 0.9, 0.7),
    'deep': (0.6, 0.4, 0.8, 0.8),
    'brainstem': (1.0, 0.4, 0.4, 0.8),
    'cerebellum': (0.4, 0.8, 0.4, 0.8),
    'thalamus': (1.0, 0.6, 0.2, 0.8),
}

meshes = []
colors = []

for fname in sorted(os.listdir(mesh_dir)):
    if not fname.endswith('.stl'):
        continue
    
    mesh = trimesh.load(os.path.join(mesh_dir, fname))
    meshes.append(mesh)
    
    # Get color
    fname_lower = fname.lower()
    if 'csf' in fname_lower:
        colors.append(region_colors['csf'])
    elif 'gray' in fname_lower and 'deep' not in fname_lower:
        colors.append(region_colors['gray'])
    elif 'white' in fname_lower:
        colors.append(region_colors['white'])
    elif 'deep' in fname_lower:
        colors.append(region_colors['deep'])
    elif 'brainstem' in fname_lower or 'brain_stem' in fname_lower:
        colors.append(region_colors['brainstem'])
    elif 'cerebellum' in fname_lower:
        colors.append(region_colors['cerebellum'])
    elif 'thalamus' in fname_lower:
        colors.append(region_colors['thalamus'])
    else:
        colors.append((0.7, 0.7, 0.7, 0.6))
    
    print(f"  Loaded {fname}")

print(f"\nLoaded {len(meshes)} meshes\n")

# Create visualization
print("Creating 3D visualization...")
fig = plt.figure(figsize=(16, 12))

views = [
    (90, 0, "Front View"),
    (0, 0, "Top View"),
    (0, 90, "Side View"),
    (45, 45, "Isometric View")
]

# Get combined bounds
all_verts = np.vstack([m.vertices for m in meshes])
center = all_verts.mean(axis=0)
max_range = (all_verts.max(axis=0) - all_verts.min(axis=0)).max() / 2.0

for idx, (elev, azim, title) in enumerate(views, 1):
    ax = fig.add_subplot(2, 2, idx, projection='3d')
    
    for mesh, color in zip(meshes, colors):
        poly3d = Poly3DCollection(
            mesh.vertices[mesh.faces],
            alpha=color[3],
            facecolor=color[:3],
            edgecolor='none',
            linewidths=0.1
        )
        ax.add_collection3d(poly3d)
    
    ax.set_xlim(center[0] - max_range, center[0] + max_range)
    ax.set_ylim(center[1] - max_range, center[1] + max_range)
    ax.set_zlim(center[2] - max_range, center[2] + max_range)
    
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title(title, fontsize=12, fontweight='bold')

plt.suptitle('3D Brain Region Segmentation', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()

# Save visualization
viz_path = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\brain_3d_visualization.png"
print("Saving visualization (this may take a moment)...")
plt.savefig(viz_path, dpi=150, bbox_inches='tight')
plt.close()  # Close the figure to free memory
print(f"Saved visualization: {viz_path}\n")

print("="*60)
print("3D Visualization Complete!")
print("="*60)
print(f"Combined mesh: {mesh_path}")
print(f"Individual meshes: {mesh_dir}")
print(f"Visualization image: {viz_path}")
print("\nYou can:")
print("  - Open the STL files in any 3D viewer (Blender, MeshLab, etc.)")
print("  - View the PNG visualization image")
print("="*60)

