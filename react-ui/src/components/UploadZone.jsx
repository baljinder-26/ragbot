import { useRef, useState } from 'react';
import './UploadZone.css';

export default function UploadZone({ onUpload, uploading }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleFiles = (files) => {
    const pdfs = Array.from(files).filter((f) => f.type === 'application/pdf');
    if (pdfs.length > 0) onUpload(pdfs);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  return (
    <div
      className={`upload-zone ${dragging ? 'dragging' : ''} ${uploading ? 'uploading' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => !uploading && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        multiple
        hidden
        onChange={(e) => handleFiles(e.target.files)}
      />

      {uploading ? (
        <div className="upload-uploading">
          <div className="upload-spinner"></div>
          <p>Processing PDF…</p>
        </div>
      ) : (
        <>
          <div className="upload-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
              <line x1="12" y1="18" x2="12" y2="12" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
              <polyline points="9 15 12 12 15 15" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="upload-text">
            <p className="upload-primary">{dragging ? 'Drop your PDF here' : 'Upload PDF'}</p>
            <p className="upload-secondary">Click or drag & drop</p>
          </div>
        </>
      )}
    </div>
  );
}
