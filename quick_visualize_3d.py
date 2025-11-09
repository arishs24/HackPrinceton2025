"""
Quick 3D visualization - simplified version that won't get stuck
"""
import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# Use non-interactive backend
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

mesh_dir = r"C:\Users\arish\OneDrive\Documents\GitHub\prince\HackPrinceton2025\3d_meshes"

print("Loading 3D meshes...")

region_colors = {
    'csf': (0.2, 0.6, 1.0, 0.0),  # Completely transparent - don't show
    'gray': (0.8, 0.8, 0.8, 0.7),
    'white': (1.0, 1.0, 0.9, 0.7),
    'deep': (0.6, 0.4, 0.8, 0.8),
    'brainstem': (1.0, 0.4, 0.4, 0.8),
    'cerebellum': (0.4, 0.8, 0.4, 0.8),
    'thalamus': (1.0, 0.6, 0.2, 0.8),
    # Brain lobes
    'frontal': (1.0, 0.3, 0.3, 0.8),  # Red
    'temporal': (0.3, 0.8, 0.3, 0.8),  # Green
    'parietal': (0.3, 0.3, 1.0, 0.8),  # Blue
    'occipital': (1.0, 0.8, 0.3, 0.8),  # Yellow
}

meshes = []
colors = []
names = []

for fname in sorted(os.listdir(mesh_dir)):
    if not fname.endswith('.stl'):
        continue
    
    # Skip CSF completely
    if 'csf' in fname.lower() or 'cerebrospinal' in fname.lower():
        continue
    
    try:
        mesh = trimesh.load(os.path.join(mesh_dir, fname))
        
        # Simplify mesh if it's too complex (reduce vertices)
        if len(mesh.vertices) > 50000:
            print(f"  Simplifying {fname} ({len(mesh.vertices)} vertices)...")
            try:
                mesh = mesh.simplify_quadric_decimation(50000)
            except:
                # If simplification fails, just use original
                pass
        
        meshes.append(mesh)
        names.append(fname)
        
        # Get color - check for lobes first
        fname_lower = fname.lower()
        if 'frontal' in fname_lower:
            colors.append(region_colors['frontal'])
        elif 'temporal' in fname_lower:
            colors.append(region_colors['temporal'])
        elif 'parietal' in fname_lower:
            colors.append(region_colors['parietal'])
        elif 'occipital' in fname_lower:
            colors.append(region_colors['occipital'])
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
        
        print(f"  Loaded {fname} ({len(mesh.vertices)} vertices)")
    except Exception as e:
        print(f"  Error loading {fname}: {e}")
        continue

print(f"\nLoaded {len(meshes)} meshes\n")

if not meshes:
    print("No meshes to visualize!")
    exit(1)

# Create visualization with fewer views to speed up
print("Creating 3D visualization...")
fig = plt.figure(figsize=(12, 9))

# Just 2 views to make it faster
views = [
    (45, 45, "Isometric View"),
    (0, 0, "Top View"),
]

# Get combined bounds
all_verts = np.vstack([m.vertices for m in meshes])
center = all_verts.mean(axis=0)
max_range = (all_verts.max(axis=0) - all_verts.min(axis=0)).max() / 2.0

for idx, (elev, azim, title) in enumerate(views, 1):
    ax = fig.add_subplot(1, 2, idx, projection='3d')
    
    for mesh, color in zip(meshes, colors):
        # Sample faces if mesh is too complex
        if len(mesh.faces) > 20000:
            # Use every nth face
            step = len(mesh.faces) // 20000
            faces = mesh.faces[::step]
        else:
            faces = mesh.faces
        
        poly3d = Poly3DCollection(
            mesh.vertices[faces],
            alpha=color[3],
            facecolor=color[:3],
            edgecolor='none',
            linewidths=0
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
print("Saving visualization...")
plt.savefig(viz_path, dpi=100, bbox_inches='tight')
plt.close()

print(f"Saved: {viz_path}\n")
print("="*60)
print("SUCCESS! 3D Visualization Created")
print("="*60)
print(f"Visualization: {viz_path}")
print(f"Individual meshes: {mesh_dir}")
print(f"Combined mesh: combined_brain_mesh.stl")
print("\nYou can now:")
print("  - View the PNG image")
print("  - Open STL files in Blender, MeshLab, or any 3D viewer")
print("="*60)

