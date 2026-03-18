// src/components/UploadZone.jsx
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileText } from 'lucide-react';
import './UploadZone.css';

export default function UploadZone({ onUpload, loading }) {
  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    accept: { 'text/csv': ['.csv'] },
    maxFiles: 1,
    onDropAccepted: (files) => onUpload(files[0]),
    disabled: loading,
  });

  const file = acceptedFiles[0];

  return (
    <div
      {...getRootProps()}
      className={`upload-zone glass-card ${isDragActive ? 'upload-zone--active' : ''} ${loading ? 'upload-zone--loading' : ''}`}
    >
      <input {...getInputProps()} />

      {loading ? (
        <div className="upload-zone__loading">
          <div className="spinner" />
          <span>Analyzing your expenses…</span>
        </div>
      ) : isDragActive ? (
        <div className="upload-zone__inner">
          <UploadCloud size={42} className="upload-zone__icon upload-zone__icon--active" />
          <p className="upload-zone__title">Drop it here!</p>
        </div>
      ) : file ? (
        <div className="upload-zone__inner">
          <FileText size={36} className="upload-zone__icon" />
          <p className="upload-zone__title">{file.name}</p>
          <p className="upload-zone__sub">Click or drag another file to replace</p>
        </div>
      ) : (
        <div className="upload-zone__inner">
          <UploadCloud size={42} className="upload-zone__icon" />
          <p className="upload-zone__title">Drag & drop your CSV here</p>
          <p className="upload-zone__sub">Or click to browse — supports any bank export format</p>
          <div className="upload-zone__hint">
            Required columns: <code>date</code>, <code>amount</code>, <code>description</code>
          </div>
        </div>
      )}
    </div>
  );
}
