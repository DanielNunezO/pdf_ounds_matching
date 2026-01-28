/**
 * Paste Detection Component
 * 
 * Tracks paste events and displays statistics
 */
import { useState, useEffect } from 'react';

const PasteDetection = () => {
  const [pasteCount, setPasteCount] = useState(0);
  const [pasteHistory, setPasteHistory] = useState([]);

  useEffect(() => {
    const handlePaste = (event) => {
      const timestamp = new Date().toLocaleTimeString();
      const pastedText = event.clipboardData?.getData('text') || '';
      const truncated = pastedText.substring(0, 50) + (pastedText.length > 50 ? '...' : '');
      
      setPasteCount((prev) => prev + 1);
      setPasteHistory((prev) => [
        ...prev,
        { timestamp, text: truncated, length: pastedText.length }
      ].slice(-10)); // Keep last 10 pastes
    };

    document.addEventListener('paste', handlePaste);
    return () => document.removeEventListener('paste', handlePaste);
  }, []);

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Paste Detection</h3>
      <div style={styles.counter}>
        Total Pastes: <strong>{pasteCount}</strong>
      </div>
      
      {pasteHistory.length > 0 && (
        <div style={styles.history}>
          <h4 style={styles.historyTitle}>Recent Pastes:</h4>
          <ul style={styles.list}>
            {pasteHistory.map((paste, index) => (
              <li key={index} style={styles.listItem}>
                <span style={styles.timestamp}>{paste.timestamp}</span>
                <span style={styles.text}>{paste.text}</span>
                <span style={styles.length}>({paste.length} chars)</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '15px',
    border: '1px solid #444',
    borderRadius: '8px',
    backgroundColor: '#2a2a2a',
    marginTop: '20px',
  },
  title: {
    margin: '0 0 10px 0',
    color: '#fff',
    fontSize: '18px',
  },
  counter: {
    fontSize: '16px',
    color: '#ccc',
    marginBottom: '15px',
  },
  history: {
    marginTop: '15px',
  },
  historyTitle: {
    margin: '0 0 10px 0',
    color: '#fff',
    fontSize: '14px',
  },
  list: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  listItem: {
    padding: '8px',
    marginBottom: '5px',
    backgroundColor: '#1a1a1a',
    borderRadius: '4px',
    fontSize: '12px',
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
  },
  timestamp: {
    color: '#4CAF50',
    fontWeight: 'bold',
    minWidth: '80px',
  },
  text: {
    color: '#ccc',
    flex: 1,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  length: {
    color: '#888',
    fontSize: '11px',
  },
};

export default PasteDetection;
