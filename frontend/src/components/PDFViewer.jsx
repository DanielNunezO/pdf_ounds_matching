/**
 * PDF Viewer Component with Bounds Visualization
 * 
 * Displays PDF and highlights matched text bounds
 */
import { useState, useEffect } from 'react';

const PDFViewer = ({ pdfFile, matches }) => {
  const [currentPage, setCurrentPage] = useState(0);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [totalPages, setTotalPages] = useState(1);

  // Load PDF file
  const handleFileLoad = (file) => {
    if (file) {
      // Revoke previous URL to prevent memory leak
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
      
      const url = URL.createObjectURL(file);
      setPdfUrl(url);
      // Note: In a real implementation, we'd use a PDF library to get actual page count
      setTotalPages(10); // Placeholder - should be from PDF metadata
    }
  };

  // Clean up blob URL on unmount
  useEffect(() => {
    return () => {
      if (pdfUrl) {
        URL.revokeObjectURL(pdfUrl);
      }
    };
  }, [pdfUrl]);

  // Render matches as overlays
  // Note: This is a simplified visualization. In production, you'd need to:
  // 1. Use a proper PDF library (like react-pdf or pdf.js)
  // 2. Transform PDF coordinates to viewport coordinates
  // 3. Handle zoom and scaling
  const renderMatches = () => {
    if (!matches || matches.length === 0) return null;

    return matches
      .filter((match) => match.match.page === currentPage)
      .map((match, index) => {
        const { x0, y0, x1, y1 } = match.match;
        const confidence = match.confidence;
        
        // Calculate color based on confidence
        const opacity = confidence / 100 * 0.5 + 0.3; // 0.3 to 0.8 opacity
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
            <span style={styles.pageNumber}>Page {currentPage + 1} / {totalPages}</span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
              disabled={currentPage >= totalPages - 1}
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
          <p style={styles.note}>
            Note: Match coordinates shown are from PDF space. 
            For accurate visualization, use a PDF.js-based viewer in production.
          </p>
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
  note: {
    marginTop: '10px',
    padding: '10px',
    fontSize: '12px',
    color: '#888',
    fontStyle: 'italic',
    textAlign: 'center',
  },
};

export default PDFViewer;
