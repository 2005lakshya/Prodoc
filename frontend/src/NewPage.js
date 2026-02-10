import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from './folder_hover';

function NewPage() {
  const [file, setFile] = React.useState(null);
  const [isDragging, setIsDragging] = React.useState(false);
  const [showPreview, setShowPreview] = React.useState(false);
  const fileInputRef = React.useRef(null);
  const navigate = useNavigate();

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div style={{
      padding: '20px',
      textAlign: 'center',
      backgroundColor: 'transparent',
      color: 'white',
      minHeight: '100vh',
      boxSizing: 'border-box',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'flex-start',
      paddingTop: '50px'
    }}>
      <img src="/logo.png" alt="Logo" style={{ width: '150px', marginBottom: '10px' }} />
      <h1 style={{
        fontSize: '2.5rem',
        margin: '0 0 10px 0',
        background: 'linear-gradient(45deg, #4CAF50, #69f0ae)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        textShadow: '0 0 20px rgba(76, 175, 80, 0.3)'
      }}>PRO DOC</h1>
      <p style={{
        fontSize: '1rem',
        margin: '0 0 40px 0',
        background: 'linear-gradient(90deg, #e8f5e9, #b9f6ca)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        fontWeight: 'bold',
        opacity: 0.9
      }}>Explore the doc world</p>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
        style={{
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: '24px',
          backgroundColor: isDragging ? 'rgba(255, 255, 255, 0.15)' : 'rgba(255, 255, 255, 0.05)',
          padding: '40px',
          marginTop: '30px',
          cursor: 'pointer',
          width: '85%',
          maxWidth: '600px',
          transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
          color: 'white',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          boxShadow: isDragging
            ? '0 12px 40px rgba(0, 0, 0, 0.4), inset 0 0 0 1px rgba(255, 255, 255, 0.3)'
            : '0 8px 32px 0 rgba(0, 0, 0, 0.3), inset 0 0 0 1px rgba(255, 255, 255, 0.1)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          borderTop: '1px solid rgba(255, 255, 255, 0.3)',
          borderLeft: '1px solid rgba(255, 255, 255, 0.3)'
        }}
      >
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          accept="application/pdf"
          onChange={handleFileChange}
        />

        {file ? (
          <div style={{ position: 'relative' }}>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setFile(null);
              }}
              style={{
                position: 'absolute',
                top: '-20px',
                right: '-20px',
                background: '#ff5252',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                width: '30px',
                height: '30px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                zIndex: 10
              }}
              title="Remove file"
            >
              X
            </button>
            <p style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#69f0ae' }}>
              File Selected:
            </p>
            <p style={{ margin: '10px 0' }}>{file.name}</p>
            <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginTop: '20px' }}>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setShowPreview(true);
                }}
                style={{
                  padding: '12px 30px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '25px',
                  color: 'white',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  backdropFilter: 'blur(5px)'
                }}
              >
                Preview
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  navigate('/analysis', { state: { file } });
                }}
                style={{
                  padding: '12px 30px',
                  background: 'linear-gradient(45deg, #388E3C, #4CAF50)',
                  border: 'none',
                  borderRadius: '25px',
                  color: 'white',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  boxShadow: '0 4px 15px rgba(56, 142, 60, 0.4)',
                  transition: 'transform 0.2s, box-shadow 0.2s'
                }}
                onMouseOver={(e) => {
                  e.target.style.transform = 'scale(1.05)';
                  e.target.style.boxShadow = '0 6px 20px rgba(56, 142, 60, 0.6)';
                }}
                onMouseOut={(e) => {
                  e.target.style.transform = 'scale(1)';
                  e.target.style.boxShadow = '0 4px 15px rgba(56, 142, 60, 0.4)';
                }}
              >
                Analyze
              </button>
            </div>
          </div>
        ) : (
          <div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <Card />
          </div>
        )}
      </div>

      {showPreview && file && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000,
            backdropFilter: 'blur(5px)'
          }}
          onClick={() => setShowPreview(false)}
        >
          <div
            style={{
              position: 'relative',
              width: '80%',
              maxWidth: '800px',
              height: '80%',
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              borderRadius: '20px',
              padding: '20px',
              display: 'flex',
              flexDirection: 'column',
              boxShadow: '0 8px 32px 0 rgba(31, 135, 38, 0.2)',
              border: 'none',
              backdropFilter: 'blur(15px)',
              WebkitBackdropFilter: 'blur(15px)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowPreview(false)}
              style={{
                alignSelf: 'flex-end',
                background: 'transparent',
                border: 'none',
                color: 'white',
                fontSize: '1.5rem',
                cursor: 'pointer',
                marginBottom: '10px'
              }}
            >
              ✕
            </button>
            <div style={{ flex: 1, overflow: 'auto', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              {file.type.startsWith('image/') ? (
                <img
                  src={URL.createObjectURL(file)}
                  alt="Preview"
                  style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                />
              ) : (
                <iframe
                  src={URL.createObjectURL(file)}
                  style={{ width: '100%', height: '100%', border: 'none' }}
                  title="PDF Preview"
                />
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default NewPage;