import React, { useState } from 'react';
import { useSTLViewer } from '../hooks/useSTLViewer';
import { FileUpload } from '../components/FileUpload';
import { STLViewer } from '../components/STLViewer';
import { STLStructureList } from '../components/STLStructureList';

export function NeuroSimPage() {
  const [caseId, setCaseId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const {
    stlFiles,
    selectedStructure,
    selectedCoordinates,
    feaResults,
    isLoadingFEA,
    error,
    selectStructure,
    runFEASimulation,
    feaParams,
    updateFEAParams,
    isPolling,
  } = useSTLViewer(caseId);

  const handleSegmentAndDisplay = async () => {
    setIsLoading(true);
    // Generate a dummy case ID for loading STL files
    const dummyCaseId = 'display-all';
    setCaseId(dummyCaseId);
    // Reset poll count
    (window as any).__stlPollCount = 0;
    
    // Simulate loading delay (3 seconds)
    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  };

  const handleUploadSuccess = (uploadedCaseId: string) => {
    setCaseId(uploadedCaseId);
    // Reset poll count when new upload
    (window as any).__stlPollCount = 0;
  };


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
            <h1 className="text-2xl font-serif font-semibold text-navy-deep tracking-[-0.02em]">Synovia</h1>
            <p className="text-xs text-gray-500">AI-Powered Surgical Planning</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {(isLoading || isPolling) && stlFiles.length === 0 && (
            <div className="flex items-center space-x-2 bg-blue-50 px-3 py-1.5 rounded-lg">
              <div className="w-2 h-2 bg-medical-blue rounded-full animate-pulse"></div>
              <span className="text-sm text-medical-blue font-medium">Segmenting Brain Structures...</span>
            </div>
          )}
          {!isPolling && stlFiles.length > 0 && (
            <div className="flex items-center space-x-2 bg-green-50 px-3 py-1.5 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-green-700 font-medium">{stlFiles.length} Structures Ready</span>
            </div>
          )}
          {selectedStructure && feaResults && (
            <div className="flex items-center space-x-2 bg-green-50 px-3 py-1.5 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-green-700 font-medium">FEA Complete</span>
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
        <div className="w-[280px] bg-white border-r border-gray-200 overflow-y-auto flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Segment and Display</h3>
            <button
              onClick={handleSegmentAndDisplay}
              disabled={isLoading || isPolling}
              className="w-full btn-primary text-sm mb-3"
            >
              {isLoading || isPolling ? (
                <span className="flex items-center justify-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Loading STL Files...</span>
                </span>
              ) : (
                <span className="flex items-center justify-center space-x-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  <span>Segment and Display</span>
                </span>
              )}
            </button>
            <div className="text-xs text-gray-500 mb-3">Or upload a new scan:</div>
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>

          {caseId && (
            <>
              <div className="flex-1 overflow-y-auto">
                <STLStructureList
                  stlFiles={stlFiles}
                  selectedStructure={selectedStructure?.filename || null}
                  onSelect={selectStructure}
                  isLoading={(isLoading || isPolling) && stlFiles.length === 0}
                />
              </div>

              {selectedStructure && (
                <div className="p-4 border-t border-gray-200 bg-gray-50 space-y-3">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-2">
                    <p className="text-xs text-blue-800 font-medium mb-1">Selected Region</p>
                    <p className="text-xs text-blue-700">{selectedStructure.name}</p>
                    {feaParams.coordinates && (
                      <p className="text-xs text-blue-600 mt-1">
                        Coordinates: ({feaParams.coordinates.x.toFixed(2)}, {feaParams.coordinates.y.toFixed(2)}, {feaParams.coordinates.z.toFixed(2)})
                      </p>
                    )}
                  </div>

                  {/* Parameter Controls */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-semibold text-gray-700">Simulation Parameters</h4>
                    
                    <div>
                      <label className="text-xs text-gray-600">Volume to Remove</label>
                      <input
                        type="text"
                        value={feaParams.volume_to_remove || 'variable'}
                        onChange={(e) => updateFEAParams({ volume_to_remove: e.target.value })}
                        className="w-full px-2 py-1 text-xs border border-gray-300 rounded mt-1"
                        placeholder="e.g., 4cm³"
                      />
                    </div>
                    
                    <div>
                      <label className="text-xs text-gray-600">Patient Age</label>
                      <input
                        type="number"
                        value={feaParams.patient_age || 45}
                        onChange={(e) => updateFEAParams({ patient_age: parseInt(e.target.value) || 45 })}
                        className="w-full px-2 py-1 text-xs border border-gray-300 rounded mt-1"
                        min="1"
                        max="100"
                      />
                    </div>
                    
                    <div>
                      <label className="text-xs text-gray-600">Procedure Type</label>
                      <select
                        value={feaParams.procedure_type || 'tumor resection'}
                        onChange={(e) => updateFEAParams({ procedure_type: e.target.value })}
                        className="w-full px-2 py-1 text-xs border border-gray-300 rounded mt-1"
                      >
                        <option value="tumor resection">Tumor Resection</option>
                        <option value="biopsy">Biopsy</option>
                        <option value="epilepsy surgery">Epilepsy Surgery</option>
                        <option value="resection">General Resection</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="text-xs text-gray-600">Reason</label>
                      <input
                        type="text"
                        value={feaParams.reason || 'low-grade glioma'}
                        onChange={(e) => updateFEAParams({ reason: e.target.value })}
                        className="w-full px-2 py-1 text-xs border border-gray-300 rounded mt-1"
                        placeholder="e.g., low-grade glioma"
                      />
                    </div>
                  </div>

                  <button
                    onClick={runFEASimulation}
                    disabled={isLoadingFEA}
                    className="w-full btn-primary text-sm"
                  >
                    {isLoadingFEA ? (
                      <span className="flex items-center justify-center space-x-2">
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Analyzing...</span>
                      </span>
                    ) : (
                      <span className="flex items-center justify-center space-x-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        <span>Re-run Analysis</span>
                      </span>
                    )}
                  </button>
                  
                  {feaResults && (
                    <div className="mt-3 p-3 bg-white rounded-lg">
                      <h4 className="text-xs font-semibold text-gray-700 mb-2">Quick Summary</h4>
                      <div className="space-y-1 text-xs">
                        <div>
                          <span className="text-gray-600">Max Stress:</span>
                          <span className="ml-2 font-medium text-gray-800">
                            {feaResults.fea_results.max_stress_kpa.toFixed(1)} kPa
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-600">Affected Regions:</span>
                          <span className="ml-2 font-medium text-gray-800">
                            {feaResults.fea_results.affected_regions.length}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>

        {/* CENTER PANEL - 3D STL Viewer */}
        <div className="flex-1 bg-dark-bg relative">
          {!caseId ? (
            <div className="h-full flex items-center justify-center p-12">
              <div className="text-center max-w-md animate-fade-in">
                <div className="w-20 h-20 bg-gradient-to-br from-medical-blue/20 to-mint-accent/20 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <svg className="w-10 h-10 text-medical-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <h2 className="text-3xl font-serif font-semibold text-white mb-3 tracking-[-0.02em]">Welcome to Synovia</h2>
                <p className="text-gray-400 mb-8">
                  Click "Segment and Display" to load all brain structures from STL files, or upload a new scan.
                </p>
                <button
                  onClick={handleSegmentAndDisplay}
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
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                      </svg>
                      <span>Segment and Display</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          ) : (isLoading || isPolling) && stlFiles.length === 0 ? (
            <div className="h-full flex items-center justify-center p-12">
              <div className="text-center max-w-md">
                <div className="w-16 h-16 border-4 border-medical-blue border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <h3 className="text-xl font-semibold text-white mb-2">Segmenting Brain Structures...</h3>
                <p className="text-gray-400 mb-4">
                  Loading brain structures from STL files. This may take a few seconds...
                </p>
                {isPolling && (
                  <div className="mt-4 p-3 bg-blue-500/20 rounded-lg">
                    <p className="text-sm text-blue-300">Loading STL files...</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <STLViewer
              stlFiles={stlFiles}
              caseId={caseId}
              selectedStructure={selectedStructure?.filename || null}
              selectedCoordinates={selectedCoordinates}
              onStructureSelect={selectStructure}
              feaResults={feaResults ? {
                affectedRegions: feaResults.fea_results.affected_regions,
                stressDistribution: feaResults.fea_results.stress_distribution,
                max_stress_kpa: feaResults.fea_results.max_stress_kpa,
              } : undefined}
            />
          )}
        </div>

        {/* RIGHT PANEL - FEA Insights (320px) */}
        <div className="w-[320px] bg-white border-l border-gray-200 overflow-y-auto">
          {feaResults ? (
            <div className="p-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">FEA Analysis</h3>
              
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">Stress Distribution</h4>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-red-600 font-medium">High Stress:</span>
                      <ul className="ml-4 mt-1 text-gray-600">
                        {feaResults.fea_results.stress_distribution.high_stress.map((region, i) => (
                          <li key={i}>• {region}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <span className="text-orange-600 font-medium">Moderate Stress:</span>
                      <ul className="ml-4 mt-1 text-gray-600">
                        {feaResults.fea_results.stress_distribution.moderate_stress.map((region, i) => (
                          <li key={i}>• {region}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">Affected Regions</h4>
                  <ul className="space-y-1 text-sm text-gray-600">
                    {feaResults.fea_results.affected_regions.map((region, i) => (
                      <li key={i} className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-medical-blue rounded-full"></div>
                        <span>{region}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {feaResults.recommendations && feaResults.recommendations.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">Recommendations</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      {feaResults.recommendations.slice(0, 3).map((rec, i) => (
                        <li key={i} className="flex items-start space-x-2">
                          <span className="text-medical-blue mt-1">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="p-4 text-center text-gray-500">
              <p className="text-sm">Select a structure and run FEA to see analysis results here.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
