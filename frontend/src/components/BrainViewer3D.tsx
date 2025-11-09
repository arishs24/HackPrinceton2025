import React, { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';
import * as THREE from 'three';
import type { MeshData } from '../types';

interface BrainViewer3DProps {
  meshData: MeshData;
  title?: string;
  showHeatmap?: boolean;
  heatmapData?: number[];
}

export const BrainViewer3D: React.FC<BrainViewer3DProps> = ({
  meshData,
  title,
  showHeatmap = false,
  heatmapData = [],
}) => {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    
    // Convert vertices to Float32Array
    const vertices = new Float32Array(
      meshData.vertices.flat()
    );
    
    // Convert faces to Uint32Array
    const indices = new Uint32Array(
      meshData.faces.flat()
    );
    
    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geo.setIndex(new THREE.BufferAttribute(indices, 1));
    geo.computeVertexNormals();
    
    // Set colors
    if (meshData.colors && meshData.colors.length > 0) {
      const colors = new Float32Array(meshData.colors.flat());
      geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    } else if (showHeatmap && heatmapData.length > 0) {
      // Apply heatmap colors
      const colors = new Float32Array(meshData.vertices.length * 3);
      const minStress = Math.min(...heatmapData);
      const maxStress = Math.max(...heatmapData);
      const range = maxStress - minStress || 1;
      
      for (let i = 0; i < heatmapData.length; i++) {
        const normalized = (heatmapData[i] - minStress) / range;
        // Blue (low) to Red (high)
        const r = normalized;
        const g = 0;
        const b = 1 - normalized;
        
        colors[i * 3] = r;
        colors[i * 3 + 1] = g;
        colors[i * 3 + 2] = b;
      }
      geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    }
    
    return geo;
  }, [meshData, showHeatmap, heatmapData]);

  return (
    <div className="h-full w-full relative">
      {title && (
        <div className="absolute top-4 left-4 z-10 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-lg shadow-lg">
          <h3 className="text-sm font-semibold text-gray-800">{title}</h3>
        </div>
      )}
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <pointLight position={[-10, -10, -10]} intensity={0.3} />
        
        <mesh geometry={geometry}>
          <meshStandardMaterial
            vertexColors={true}
            side={THREE.DoubleSide}
          />
        </mesh>
        
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={2}
          maxDistance={10}
        />
        
        <Grid args={[10, 10]} cellColor="#6b7280" sectionColor="#9ca3af" />
        <axesHelper args={[2]} />
      </Canvas>
    </div>
  );
};

