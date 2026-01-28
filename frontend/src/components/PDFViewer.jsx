/**
 * PDF Viewer Component with Bounds Visualization
 * 
 * Displays PDF and highlights matched text bounds
 */
import { useState } from 'react';

const PDFViewer = ({ pdfFile, matches }) => {
  const [currentPage, setCurrentPage] = useState(0);
  const [pdfUrl, setPdfUrl] = useState(null);

  // Load PDF file
  const handleFileLoad = (file) => {
    if (file) {
      const url = URL.createObjectURL(file);
      setPdfUrl(url);
    }
  };

  // Render matches as overlays
  const renderMatches = () => {
    if (!matches || matches.length === 0) return null;

    return matches
      .filter((match) => match.match.page === currentPage)
      .map((match, index) => {
        const { x0, y0, x1, y1 } = match.match;
        const confidence = match.confidence;
        
        // Calculate color based on confidence
        const opacity = confidence / 200 + 0.3; // 0.3 to 0.8 opacity
        const color = confidence >= 90 ? 'green' : confidence >= 70 ? 'orange' : 'red';
        
        return (
          <div
            key={index}
            style={{
              ...styles.highlight,
              left: `${x0}px`,
              top: `${y0}px`,
              width: `${x1 - x0}px`,
              height: `${y1 - y0}px`,
              backgroundColor: color,
              opacity: opacity,
            }}
            title={`Confidence: ${confidence.toFixed(1)}%`}
          />
        );
      });
  };

  return (
    <div style={styles.container}>
      <div style={styles.controls}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => handleFileLoad(e.target.files[0])}
          style={styles.fileInput}
        />
        
        {pdfUrl && (
          <div style={styles.pageControls}>
            <button
              onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
              disabled={currentPage === 0}
              style={styles.button}
            >
              Previous
            </button>
            <span style={styles.pageNumber}>Page {currentPage + 1}</span>
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              style={styles.button}
            >
              Next
            </button>
          </div>
        )}
      </div>

      {pdfUrl ? (
        <div style={styles.pdfContainer}>
          <div style={styles.pageWrapper}>
            <iframe
              src={`${pdfUrl}#page=${currentPage + 1}`}
              style={styles.iframe}
              title="PDF Viewer"
            />
            <div style={styles.overlayContainer}>
              {renderMatches()}
            </div>
          </div>
        </div>
      ) : (
        <div style={styles.placeholder}>
          <p>Please upload a PDF file to begin</p>
        </div>
      )}

      {matches && matches.length > 0 && (
        <div style={styles.matchInfo}>
          <h4>Match Information</h4>
          <p>Total matches: {matches.length}</p>
          <p>Matches on current page: {matches.filter(m => m.match.page === currentPage).length}</p>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    width: '100%',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  controls: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px',
    backgroundColor: '#2a2a2a',
    borderRadius: '8px',
    marginBottom: '20px',
  },
  fileInput: {
    padding: '8px',
    fontSize: '14px',
  },
  pageControls: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
  },
  button: {
    padding: '8px 16px',
    fontSize: '14px',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#4CAF50',
    color: 'white',
  },
  pageNumber: {
    color: '#fff',
    fontSize: '14px',
    minWidth: '80px',
    textAlign: 'center',
  },
  pdfContainer: {
    position: 'relative',
    backgroundColor: '#1a1a1a',
    borderRadius: '8px',
    overflow: 'hidden',
    minHeight: '600px',
  },
  pageWrapper: {
    position: 'relative',
    width: '100%',
    height: '600px',
  },
  iframe: {
    width: '100%',
    height: '100%',
    border: 'none',
  },
  overlayContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    pointerEvents: 'none',
  },
  highlight: {
    position: 'absolute',
    border: '2px solid yellow',
    pointerEvents: 'all',
    cursor: 'pointer',
  },
  placeholder: {
    textAlign: 'center',
    padding: '100px 20px',
    color: '#888',
    backgroundColor: '#1a1a1a',
    borderRadius: '8px',
  },
  matchInfo: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#2a2a2a',
    borderRadius: '8px',
    color: '#fff',
  },
};

export default PDFViewer;
