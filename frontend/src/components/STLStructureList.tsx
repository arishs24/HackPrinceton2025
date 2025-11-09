import React from 'react';
import * as THREE from 'three';
import type { STLFileInfo } from '../types';

// Generate a unique color based on index (same as in STLViewer)
function getColorForIndex(index: number): string {
  const hue = (index * 137.508) % 360; // Golden angle for better distribution
  const saturation = 0.6 + (index % 3) * 0.1; // Vary saturation
  const lightness = 0.5 + (index % 2) * 0.2; // Vary lightness
  const color = new THREE.Color().setHSL(hue / 360, saturation, lightness);
  return `#${color.getHexString()}`;
}

interface STLStructureListProps {
  stlFiles: STLFileInfo[];
  selectedStructure: string | null;
  onSelect: (structure: STLFileInfo) => void;
  isLoading?: boolean;
}

export const STLStructureList: React.FC<STLStructureListProps> = ({
  stlFiles,
  selectedStructure,
  onSelect,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="p-4">
        <div className="flex items-center space-x-2 text-gray-600">
          <div className="w-4 h-4 border-2 border-medical-blue border-t-transparent rounded-full animate-spin"></div>
          <span className="text-sm">Loading structures...</span>
        </div>
      </div>
    );
  }

  if (stlFiles.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        <p className="text-sm">No structures available yet.</p>
        <p className="text-xs mt-1">Segmentation may still be processing...</p>
      </div>
    );
  }

  return (
    <div className="p-2">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 px-2">
        Brain Structures ({stlFiles.length})
      </h3>
      <div className="space-y-1 max-h-[600px] overflow-y-auto">
        {stlFiles.map((stlFile, index) => {
          const isSelected = selectedStructure === stlFile.filename;
          const structureColor = getColorForIndex(index);
          return (
            <button
              key={stlFile.filename}
              onClick={() => onSelect(stlFile)}
              className={`
                w-full text-left px-3 py-2 rounded-lg transition-all
                ${
                  isSelected
                    ? 'bg-medical-blue text-white shadow-md'
                    : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                }
              `}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 flex-1 min-w-0">
                  <div
                    className="w-3 h-3 rounded flex-shrink-0"
                    style={{ backgroundColor: structureColor }}
                    title={`Color: ${structureColor}`}
                  />
                  <span className="text-sm font-medium truncate">{stlFile.name}</span>
                </div>
                {isSelected && (
                  <svg
                    className="w-4 h-4 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </div>
              {stlFile.voxels > 0 && (
                <p className="text-xs mt-1 opacity-75">
                  {stlFile.voxels.toLocaleString()} voxels
                </p>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

