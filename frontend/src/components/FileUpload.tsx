import React, { useCallback, useState } from 'react';
import { uploadScan } from '../utils/api';

interface FileUploadProps {
  onUploadSuccess: (caseId: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    
    // Validate file types
    const validTypes = ['.dcm', '.dicom', '.nii', '.nii.gz'];
    const invalidFiles = fileArray.filter(
      file => !validTypes.some(ext => file.name.toLowerCase().endsWith(ext))
    );
    
    if (invalidFiles.length > 0) {
      setError(`Invalid file type. Please upload DICOM (.dcm) or NIfTI (.nii) files.`);
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const response = await uploadScan(fileArray);
      onUploadSuccess(response.case_id);
    } catch (err: any) {
      setError(err.message || 'Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  }, [handleFiles]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files);
    }
  }, [handleFiles]);

  return (
    <div className="space-y-3">
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          border-2 border-dashed rounded-lg p-6 text-center transition-colors
          ${isDragging ? 'border-medical-blue bg-blue-50' : 'border-gray-300 bg-gray-50'}
          ${isUploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-medical-blue'}
        `}
      >
        {isUploading ? (
          <div className="flex flex-col items-center space-y-2">
            <div className="w-8 h-8 border-2 border-medical-blue border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm text-gray-600">Uploading...</p>
          </div>
        ) : (
          <>
            <svg
              className="w-12 h-12 mx-auto text-gray-400 mb-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="text-sm text-gray-600 mb-2">
              Drag and drop DICOM files here, or
            </p>
            <label className="text-sm text-medical-blue font-medium cursor-pointer hover:underline">
              click to browse
              <input
                type="file"
                multiple
                accept=".dcm,.dicom,.nii,.nii.gz"
                onChange={handleFileInput}
                className="hidden"
                disabled={isUploading}
              />
            </label>
            <p className="text-xs text-gray-500 mt-2">
              Supports .dcm, .dicom, .nii, .nii.gz
            </p>
          </>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}
    </div>
  );
};

