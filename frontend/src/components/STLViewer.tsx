import React, { useRef, useEffect, useState, useMemo, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Text } from '@react-three/drei';
import * as THREE from 'three';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
import type { STLFileInfo } from '../types';

interface STLViewerProps {
  stlFiles: STLFileInfo[];
  caseId: string;
  selectedStructure: string | null;
  selectedCoordinates?: { x: number; y: number; z: number };
  onStructureSelect: (structure: STLFileInfo, coordinates?: { x: number; y: number; z: number }) => void;
  feaResults?: {
    affectedRegions: string[];
    stressDistribution: {
      high_stress: string[];
      moderate_stress: string[];
      low_stress: string[];
    };
    max_stress_kpa?: number;
  };
}

// Generate a unique color based on index
function getColorForIndex(index: number): THREE.Color {
  const hue = (index * 137.508) % 360; // Golden angle for better distribution
  const saturation = 0.6 + (index % 3) * 0.1; // Vary saturation
  const lightness = 0.5 + (index % 2) * 0.2; // Vary lightness
  return new THREE.Color().setHSL(hue / 360, saturation, lightness);
}

// Component to load and display a single STL file
function STLMesh({
  url,
  name,
  isSelected,
  isAffected,
  stressLevel,
  onSelect,
  clickCoordinates,
  index,
  showLabel,
  onBboxUpdate,
  maxStressKpa,
}: {
  url: string;
  name: string;
  isSelected: boolean;
  isAffected: boolean;
  stressLevel: 'high' | 'moderate' | 'low' | 'none';
  onSelect: (coordinates?: THREE.Vector3) => void;
  index: number;
  showLabel: boolean;
  clickCoordinates?: THREE.Vector3;
  onBboxUpdate?: (bbox: THREE.Box3) => void;
  maxStressKpa?: number;
}) {
  const [geometry, setGeometry] = useState<THREE.BufferGeometry | null>(null);
  const [bbox, setBbox] = useState<THREE.Box3 | null>(null);
  const meshRef = useRef<THREE.Mesh>(null);
  const groupRef = useRef<THREE.Group>(null);

  useEffect(() => {
    const loader = new STLLoader();
    loader.load(
      url,
      (loadedGeometry) => {
        // DON'T center - keep original anatomical position
        // Just compute normals for proper lighting
        loadedGeometry.computeVertexNormals();
        
        // Calculate bounding box for label positioning (without centering)
        const box = new THREE.Box3().setFromBufferAttribute(loadedGeometry.attributes.position);
        setBbox(box);
        setGeometry(loadedGeometry);
        
        console.log(`Loaded ${name}:`, {
          min: box.min.toArray(),
          max: box.max.toArray(),
          size: box.getSize(new THREE.Vector3()).toArray()
        });
        
        // Notify parent of bounding box
        if (onBboxUpdate) {
          onBboxUpdate(box);
        }
      },
      undefined,
      (error) => {
        console.error(`Error loading STL ${name} from ${url}:`, error);
      }
    );
  }, [url, name, onBboxUpdate]);

  // Determine base color based on selection, stress, or unique color
  const color = useMemo(() => {
    // Priority 1: Stress-based coloring (red/orange for high/moderate stress)
    if (isAffected && stressLevel !== 'none') {
      if (stressLevel === 'high') {
        return new THREE.Color(1, 0.1, 0.1); // Bright red for high stress
      } else if (stressLevel === 'moderate') {
        return new THREE.Color(1, 0.4, 0.1); // Orange for moderate stress
      } else if (stressLevel === 'low') {
        return new THREE.Color(1, 0.7, 0.2); // Yellow-orange for low stress
      }
    }
    
    // Priority 2: Selected/clicked structures get green highlight
    if (isSelected) {
      return new THREE.Color(0.2, 1, 0.3); // Bright green for selected
    }
    
    // Default: Use unique color for each structure
    return getColorForIndex(index);
  }, [isSelected, isAffected, stressLevel, index]);

  // Calculate vertex colors based on distance from click point and stress distribution
  const vertexColors = useMemo(() => {
    if (!geometry) return null;
    
    const positions = geometry.attributes.position;
    const colors = new Float32Array(positions.count * 3);
    
    // If click coordinates exist, create green gradient from click point
    if (clickCoordinates) {
      const maxDistance = 4.0; // Distance for gradient falloff
      
      for (let i = 0; i < positions.count; i++) {
        const x = positions.getX(i);
        const y = positions.getY(i);
        const z = positions.getZ(i);
        const vertexPos = new THREE.Vector3(x, y, z);
        
        const distance = vertexPos.distanceTo(clickCoordinates);
        const normalizedDistance = Math.min(distance / maxDistance, 1.0);
        
        // Create gradient: bright green at click point, fading to structure color
        const clickColor = new THREE.Color(0.2, 1, 0.3); // Green for click point
        const baseColor = color;
        
        // Interpolate between click color and base color
        const finalColor = new THREE.Color().lerpColors(clickColor, baseColor, normalizedDistance);
        
        colors[i * 3] = finalColor.r;
        colors[i * 3 + 1] = finalColor.g;
        colors[i * 3 + 2] = finalColor.b;
      }
    } else if (isAffected && stressLevel !== 'none') {
      // Apply stress-based gradient across the structure
      // Calculate center of geometry for stress gradient
      const center = bbox ? bbox.getCenter(new THREE.Vector3()) : new THREE.Vector3(0, 0, 0);
      const size = bbox ? bbox.getSize(new THREE.Vector3()) : new THREE.Vector3(1, 1, 1);
      const maxDim = Math.max(size.x, size.y, size.z);
      
      // Stress colors - more intense for better visibility
      let stressColor: THREE.Color;
      if (stressLevel === 'high') {
        stressColor = new THREE.Color(1, 0.05, 0.05); // Bright red
      } else if (stressLevel === 'moderate') {
        stressColor = new THREE.Color(1, 0.35, 0.05); // Orange-red
      } else {
        stressColor = new THREE.Color(1, 0.6, 0.1); // Orange-yellow
      }
      
      for (let i = 0; i < positions.count; i++) {
        const x = positions.getX(i);
        const y = positions.getY(i);
        const z = positions.getZ(i);
        const vertexPos = new THREE.Vector3(x, y, z);
        
        // Distance from center determines stress intensity
        const distanceFromCenter = vertexPos.distanceTo(center);
        const normalizedDist = Math.min(distanceFromCenter / (maxDim * 0.5), 1.0);
        
        // Higher stress at edges, lower at center
        const stressIntensity = 1.0 - normalizedDist * 0.5;
        const finalColor = new THREE.Color().lerpColors(color, stressColor, stressIntensity * 0.6);
        
        colors[i * 3] = finalColor.r;
        colors[i * 3 + 1] = finalColor.g;
        colors[i * 3 + 2] = finalColor.b;
      }
    } else {
      // No special coloring, use base color
      return null;
    }
    
    return new THREE.BufferAttribute(colors, 3);
  }, [geometry, clickCoordinates, color, isAffected, stressLevel, bbox]);

  // Apply vertex colors if available
  useEffect(() => {
    if (geometry && vertexColors) {
      geometry.setAttribute('color', vertexColors);
    } else if (geometry && !clickCoordinates && !isAffected) {
      // Remove vertex colors if no click point and no stress
      geometry.deleteAttribute('color');
    }
  }, [geometry, vertexColors, clickCoordinates, isAffected]);

  // Log when geometry is ready (must be before conditional return)
  useEffect(() => {
    if (geometry) {
      console.log(`Rendering mesh for ${name}`);
    }
  }, [geometry, name]);

  if (!geometry) {
    return null; // Don't render until geometry is loaded
  }

  // Calculate label position (top center of bounding box, preserving anatomical position)
  const labelPosition = bbox 
    ? new THREE.Vector3(
        (bbox.min.x + bbox.max.x) / 2,
        bbox.max.y + (bbox.max.y - bbox.min.y) * 0.1,
        (bbox.min.z + bbox.max.z) / 2
      )
    : new THREE.Vector3(0, 0.1, 0);

  return (
    <group ref={groupRef}>
      <mesh
        ref={meshRef}
        geometry={geometry}
        onClick={(e) => {
          e.stopPropagation();
          // Get click coordinates in world space, then convert to local space
          const point = e.point.clone();
          // Transform to local space of the mesh
          if (meshRef.current) {
            meshRef.current.worldToLocal(point);
          }
          onSelect(point);
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          if (e.intersections.length > 0) {
            document.body.style.cursor = 'pointer';
          }
        }}
        onPointerOut={() => {
          document.body.style.cursor = 'default';
        }}
      >
        <meshStandardMaterial
          color={color}
          opacity={isSelected ? 1.0 : 0.8}
          transparent={!isSelected}
          metalness={0.3}
          roughness={0.7}
          emissive={isSelected ? new THREE.Color(0x222222) : new THREE.Color(0x000000)}
          emissiveIntensity={isSelected ? 0.2 : 0}
          vertexColors={!!vertexColors}
        />
      </mesh>
      
      {/* Highlight sphere at click coordinates - green */}
      {clickCoordinates && (
        <mesh position={clickCoordinates}>
          <sphereGeometry args={[0.15, 16, 16]} />
          <meshStandardMaterial
            color="#33ff55"
            emissive="#33ff55"
            emissiveIntensity={0.8}
          />
        </mesh>
      )}
      {showLabel && bbox && (
        <>
          <Text
            position={labelPosition}
            fontSize={0.05}
            color={isSelected ? "#33ff55" : isAffected && stressLevel !== 'none' ? (stressLevel === 'high' ? "#ff3333" : "#ff8800") : "#ffffff"}
            anchorX="center"
            anchorY="bottom"
            outlineWidth={0.01}
            outlineColor="#000000"
          >
            {name}
          </Text>
          {/* Show stress information if available */}
          {isAffected && stressLevel !== 'none' && maxStressKpa && (
            <Text
              position={[labelPosition[0], labelPosition[1] - 0.08, labelPosition[2]]}
              fontSize={0.04}
              color={stressLevel === 'high' ? "#ff3333" : stressLevel === 'moderate' ? "#ff8800" : "#ffaa00"}
              anchorX="center"
              anchorY="bottom"
              outlineWidth={0.01}
              outlineColor="#000000"
            >
              Stress: {maxStressKpa.toFixed(1)} kPa ({stressLevel.toUpperCase()})
            </Text>
          )}
        </>
      )}
    </group>
  );
}

export const STLViewer: React.FC<STLViewerProps> = ({
  stlFiles,
  caseId,
  selectedStructure,
  selectedCoordinates,
  onStructureSelect,
  feaResults,
}) => {
  const [loadedStructures, setLoadedStructures] = useState<Set<string>>(new Set());
  const [allBoundingBoxes, setAllBoundingBoxes] = useState<THREE.Box3 | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);

  // Determine stress level for each structure
  const getStressLevel = (structureName: string): 'high' | 'moderate' | 'low' | 'none' => {
    if (!feaResults) return 'none';
    
    const nameLower = structureName.toLowerCase();
    if (feaResults.stressDistribution.high_stress.some(r => nameLower.includes(r.toLowerCase()))) {
      return 'high';
    }
    if (feaResults.stressDistribution.moderate_stress.some(r => nameLower.includes(r.toLowerCase()))) {
      return 'moderate';
    }
    if (feaResults.stressDistribution.low_stress.some(r => nameLower.includes(r.toLowerCase()))) {
      return 'low';
    }
    return 'none';
  };

  // Check if structure is affected by FEA
  const isAffected = (structureName: string): boolean => {
    if (!feaResults) return false;
    const nameLower = structureName.toLowerCase();
    return feaResults.affectedRegions.some(r => nameLower.includes(r.toLowerCase()));
  };

  // Limit initial load to first 20 structures for performance, then load rest progressively
  const [maxVisible, setMaxVisible] = useState(20);
  const visibleFiles = stlFiles.slice(0, maxVisible);

  // Load more structures progressively
  useEffect(() => {
    if (maxVisible < stlFiles.length) {
      const timer = setTimeout(() => {
        setMaxVisible(prev => Math.min(prev + 10, stlFiles.length));
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [maxVisible, stlFiles.length]);

  // Collect all bounding boxes and calculate overall bounds
  const handleBboxUpdate = useCallback((bbox: THREE.Box3) => {
    setAllBoundingBoxes(prev => {
      if (!prev) return bbox.clone();
      // Manually expand the box to include the new bbox
      const combined = prev.clone();
      combined.min.x = Math.min(combined.min.x, bbox.min.x);
      combined.min.y = Math.min(combined.min.y, bbox.min.y);
      combined.min.z = Math.min(combined.min.z, bbox.min.z);
      combined.max.x = Math.max(combined.max.x, bbox.max.x);
      combined.max.y = Math.max(combined.max.y, bbox.max.y);
      combined.max.z = Math.max(combined.max.z, bbox.max.z);
      return combined;
    });
  }, []);

  // Auto-fit camera to view all structures
  useEffect(() => {
    if (allBoundingBoxes && cameraRef.current) {
      const center = allBoundingBoxes.getCenter(new THREE.Vector3());
      const size = allBoundingBoxes.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y, size.z);
      
      console.log('Auto-fitting camera:', { 
        center: center.toArray(), 
        size: size.toArray(), 
        maxDim 
      });
      
      // Position camera to view entire scene
      const distance = maxDim > 0 ? maxDim * 1.5 : 50;
      cameraRef.current.position.set(center.x, center.y, center.z + distance);
      cameraRef.current.lookAt(center);
      cameraRef.current.updateProjectionMatrix();
    }
  }, [allBoundingBoxes]);

  return (
    <div className="h-full w-full relative">
      <Canvas 
        camera={{ position: [0, 0, 100], fov: 50 }}
        onCreated={({ camera, scene }) => {
          cameraRef.current = camera as THREE.PerspectiveCamera;
          // Set background color to see if canvas is rendering
          scene.background = new THREE.Color(0x1a1a1a);
        }}
      >
        <ambientLight intensity={0.6} />
        <pointLight position={[60, 60, 60]} intensity={0.8} />
        <pointLight position={[-60, -60, -60]} intensity={0.4} />
        <directionalLight position={[0, 60, 30]} intensity={0.5} />

        {visibleFiles.map((stlFile, index) => {
          const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api';
          const baseUrl = API_BASE_URL.replace('/api', '');
          const stlUrl = `${baseUrl}/api/stl/${caseId}/${stlFile.filename}`;
          const isSelected = selectedStructure === stlFile.filename;
          const affected = isAffected(stlFile.name);
          const stressLevel = getStressLevel(stlFile.name);
          const hasClickPoint = isSelected && selectedCoordinates;

          return (
            <STLMesh
              key={stlFile.filename}
              url={stlUrl}
              name={stlFile.name}
              isSelected={isSelected}
              isAffected={affected}
              stressLevel={stressLevel}
              clickCoordinates={hasClickPoint ? new THREE.Vector3(selectedCoordinates.x, selectedCoordinates.y, selectedCoordinates.z) : undefined}
              onSelect={(coords) => {
                // Convert Three.js Vector3 to simple object for API
                const coordsObj = coords ? { x: coords.x, y: coords.y, z: coords.z } : undefined;
                onStructureSelect(stlFile, coordsObj);
              }}
              index={index}
              showLabel={isSelected || affected} // Show labels for selected or affected structures
              maxStressKpa={feaResults?.max_stress_kpa}
              onBboxUpdate={handleBboxUpdate}
            />
          );
        })}

        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={15}
          maxDistance={300}
          target={allBoundingBoxes ? allBoundingBoxes.getCenter(new THREE.Vector3()).toArray() : [0, 0, 0]}
        />

        <Grid args={[100, 100]} cellColor="#6b7280" sectionColor="#9ca3af" />
        <axesHelper args={[30]} />
      </Canvas>

      {maxVisible < stlFiles.length && (
        <div className="absolute top-4 right-4 bg-blue-500/90 text-white px-3 py-2 rounded-lg text-sm">
          Loading {maxVisible} of {stlFiles.length} structures...
        </div>
      )}

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm px-4 py-3 rounded-lg shadow-lg max-w-xs">
        <h4 className="text-sm font-semibold text-gray-800 mb-2">Legend</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-orange-500 rounded"></div>
            <span>Selected Structure</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-red-500 rounded"></div>
            <span>High Stress (FEA)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-orange-400 rounded"></div>
            <span>Moderate Stress (FEA)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-yellow-400 rounded"></div>
            <span>Low Stress (FEA)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded" style={{ background: 'linear-gradient(90deg, #ff0000, #00ff00, #0000ff)' }}></div>
            <span>Each structure has unique color</span>
          </div>
          <div className="mt-2 pt-2 border-t border-gray-300">
            <p className="text-xs text-gray-600">
              Click a structure to select it. Labels show on selected structures.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

