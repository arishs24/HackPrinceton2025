import React, { useState } from 'react';
import { useSimulation } from '../hooks/useSimulation';
import { FileUpload } from '../components/FileUpload';
import { BrainViewer3D } from '../components/BrainViewer3D';
import { SimulationControls } from '../components/SimulationControls';
import { GeminiInsights } from '../components/GeminiInsights';
import { ComparisonView } from '../components/ComparisonView';

export function NeuroSimPage() {
  const {
    originalMesh,
    deformedMesh,
    metrics,
    heatmapData,
    isLoading,
    error,
    isSimulated,
    loadSample,
    segment,
    simulate,
  } = useSimulation();

  const [showComparison, setShowComparison] = useState(false);

  const simulationData = isSimulated && deformedMesh && metrics
    ? {
        deformed_mesh: deformedMesh,
        metrics: metrics,
        heatmap_data: heatmapData,
        case_id: 'current',
      }
    : null;

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between z-20">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-br from-medical-blue to-mint-accent rounded-lg flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-serif font-semibold text-navy-deep tracking-[-0.02em]">NeuroSim</h1>
            <p className="text-xs text-gray-500">AI-Powered Surgical Planning</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {isLoading && (
            <div className="flex items-center space-x-2 bg-blue-50 px-3 py-1.5 rounded-lg">
              <div className="w-2 h-2 bg-medical-blue rounded-full animate-pulse"></div>
              <span className="text-sm text-medical-blue font-medium">Processing...</span>
            </div>
          )}
          {isSimulated && (
            <div className="flex items-center space-x-2 bg-green-50 px-3 py-1.5 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-green-700 font-medium">Simulation Complete</span>
            </div>
          )}
        </div>
      </nav>

      {/* Error Toast */}
      {error && (
        <div className="fixed top-20 right-6 z-50 animate-slide-up">
          <div className="bg-red-50 border border-red-200 rounded-lg px-4 py-3 shadow-lg max-w-md">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-red-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Content - Three Column Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT PANEL - Controls (280px) */}
        <div className="w-[280px] bg-white border-r border-gray-200 overflow-y-auto">
          <div className="p-4 space-y-4">
            <SimulationControls
              onLoadSample={loadSample}
              onSimulate={simulate}
              isLoading={isLoading}
              hasData={!!originalMesh}
              isSimulated={isSimulated}
              metrics={metrics}
            />

            <div className="border-t border-gray-200 pt-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Upload Scan</h3>
              <FileUpload onUploadSuccess={segment} />
            </div>

            {isSimulated && metrics && (
              <div className="border-t border-gray-200 pt-4">
                <button
                  onClick={() => setShowComparison(!showComparison)}
                  className="w-full btn-secondary text-sm"
                >
                  {showComparison ? 'Hide' : 'Show'} Comparison
                </button>
              </div>
            )}
          </div>
        </div>

        {/* CENTER PANEL - 3D Viewer (Flexible) */}
        <div className="flex-1 bg-dark-bg relative">
          {!originalMesh ? (
            <div className="h-full flex items-center justify-center p-12">
              <div className="text-center max-w-md animate-fade-in">
                <div className="w-20 h-20 bg-gradient-to-br from-medical-blue/20 to-mint-accent/20 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <svg className="w-10 h-10 text-medical-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <h2 className="text-3xl font-serif font-semibold text-white mb-3 tracking-[-0.02em]">Welcome to NeuroSim</h2>
                <p className="text-gray-400 mb-8">
                  Load a sample brain scan or upload your own medical imaging data to begin simulation
                </p>
                <button
                  onClick={loadSample}
                  disabled={isLoading}
                  className="btn-primary inline-flex items-center space-x-2"
                >
                  {isLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Loading...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      <span>Load Sample Brain</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          ) : showComparison && isSimulated && deformedMesh ? (
            <ComparisonView
              originalMesh={originalMesh}
              deformedMesh={deformedMesh}
              heatmapData={heatmapData}
            />
          ) : (
            <div className="h-full">
              <BrainViewer3D
                meshData={isSimulated && deformedMesh ? deformedMesh : originalMesh}
                title={isSimulated ? "Post-Resection Simulation" : "Brain Segmentation"}
                showHeatmap={isSimulated}
                heatmapData={heatmapData}
              />
            </div>
          )}
        </div>

        {/* RIGHT PANEL - Insights (320px) */}
        <div className="w-[320px] bg-white border-l border-gray-200 overflow-y-auto">
          <GeminiInsights simulationData={simulationData} />
        </div>
      </div>
    </div>
  );
}
