import numpy as np
from app.models.schemas import SimulationResponse, SimulationMetrics, MeshData
from app.services.segmentation_engine import generate_mock_brain_mesh


def perform_tumor_removal_simulation(case_id: str, remove_region: str, skull_opening_size: float):
    """
    Simulate the biomechanical effects of tumor removal
    Uses a simplified distance-based deformation model
    """
    # Get original mesh
    original_mesh = generate_mock_brain_mesh()

    vertices = np.array(original_mesh.vertices)
    labels = np.array(original_mesh.labels)
    faces = original_mesh.faces
    colors = np.array(original_mesh.colors)

    # Find tumor center (label 3)
    tumor_vertices = vertices[labels == 3]

    if len(tumor_vertices) == 0:
        # Fallback: create artificial tumor center
        tumor_center = np.array([2.0, 2.0, 2.0])
    else:
        tumor_center = np.mean(tumor_vertices, axis=0)

    # Simulation parameters
    max_displacement = 0.5  # Maximum displacement in arbitrary units
    decay_factor = 3.0      # How quickly displacement decreases with distance

    # Calculate displacement for each vertex
    displacements = []
    stress_values = []
    deformed_vertices = vertices.copy()

    for i, vertex in enumerate(vertices):
        # Skip skull vertices (label 0)
        if labels[i] == 0:
            displacements.append(0.0)
            stress_values.append(0.0)
            continue

        # Calculate distance from tumor center
        distance = np.linalg.norm(vertex - tumor_center)

        # Calculate displacement using exponential decay
        displacement_magnitude = max_displacement * np.exp(-distance / decay_factor)

        # Direction: towards tumor center (tissue collapses inward)
        direction = (tumor_center - vertex)
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
        else:
            direction = np.zeros(3)

        # Apply displacement
        displacement_vector = direction * displacement_magnitude
        deformed_vertices[i] = vertex + displacement_vector

        # Calculate pseudo-stress (proportional to displacement)
        stress = displacement_magnitude * 3.75  # Arbitrary stress factor
        stress_values.append(float(stress))
        displacements.append(float(displacement_magnitude))

    # Update colors for tumor region (make it transparent/removed)
    new_colors = colors.copy()
    for i, label in enumerate(labels):
        if label == 3:  # Tumor
            new_colors[i] = [0.3, 0.3, 0.3]  # Dark grey to show removed area

    # Calculate metrics
    max_disp = float(np.max(displacements))
    avg_stress = float(np.mean([s for s in stress_values if s > 0.1]))  # Exclude very low stress

    # Find vulnerable regions (high stress areas)
    vulnerable_regions = []
    if avg_stress > 1.0:
        vulnerable_regions.append("parietal_lobe")
    if max_disp > 0.3:
        vulnerable_regions.append("frontal_cortex")

    # Calculate affected volume (approximate)
    affected_count = sum(1 for d in displacements if d > 0.05)
    affected_volume = affected_count * 0.5  # Arbitrary volume per vertex

    metrics = SimulationMetrics(
        max_displacement_mm=max_disp * 10,  # Convert to mm
        avg_stress_kpa=avg_stress,
        affected_volume_cm3=affected_volume,
        vulnerable_regions=vulnerable_regions
    )

    deformed_mesh = MeshData(
        vertices=deformed_vertices.tolist(),
        faces=faces,
        labels=labels.tolist(),
        colors=new_colors.tolist()
    )

    return SimulationResponse(
        deformed_mesh=deformed_mesh,
        metrics=metrics,
        heatmap_data=stress_values,
        case_id=case_id
    )
