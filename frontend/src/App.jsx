/**
 * Main Application Component
 */
import { useState } from 'react';
import Timer from './components/Timer';
import PasteDetection from './components/PasteDetection';
import PDFViewer from './components/PDFViewer';
import apiService from './services/api';
import './App.css';

function App() {
  const [fileId, setFileId] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [entities, setEntities] = useState([]);
  const [matches, setMatches] = useState([]);
  const [selectedEntity, setSelectedEntity] = useState('');
  const [selectedStrategy, setSelectedStrategy] = useState('exact');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePDFUpload = async (file) => {
    try {
      setLoading(true);
      setError(null);
      
      // Upload PDF
      const uploadResult = await apiService.uploadPDF(file);
      setFileId(uploadResult.file_id);
      setPdfFile(file);

      // Extract text
      const extractResult = await apiService.extractText(uploadResult.file_id);
      setExtractedText(extractResult.full_text);

      alert('PDF uploaded and text extracted successfully!');
    } catch (err) {
      setError(`Error uploading PDF: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleExtractEntities = async () => {
    try {
      setLoading(true);
      setError(null);

      const result = await apiService.extractNamedEntities(extractedText);
      
      // Flatten all entities from different categories
      const allEntities = Object.values(result.entities).flat();
      setEntities(allEntities);

      alert(`Extracted ${allEntities.length} entities!`);
    } catch (err) {
      setError(`Error extracting entities: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleMatchEntity = async () => {
    if (!selectedEntity) {
      alert('Please enter or select an entity to match');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const result = await apiService.matchEntity(
        fileId,
        selectedEntity,
        selectedStrategy,
        { threshold: 80.0, context_window: 3 }
      );

      setMatches(result.matches);
      alert(`Found ${result.match_count} matches!`);
    } catch (err) {
      setError(`Error matching entity: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTimeUp = () => {
    alert('Time is up! Please submit your results.');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>PDF Bounds Matching Challenge</h1>
        <p>Extract entities from PDFs and match them using sophisticated algorithms</p>
      </header>

      <div className="app-container">
        <div className="sidebar">
          <Timer onTimeUp={handleTimeUp} />
          <PasteDetection />
        </div>

        <div className="main-content">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="section">
            <h2>1. Upload PDF</h2>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => handlePDFUpload(e.target.files[0])}
              disabled={loading}
            />
          </div>

          {extractedText && (
            <>
              <div className="section">
                <h2>2. Extract Entities (LLM)</h2>
                <button onClick={handleExtractEntities} disabled={loading}>
                  {loading ? 'Extracting...' : 'Extract Entities'}
                </button>
                
                {entities.length > 0 && (
                  <div className="entities-list">
                    <h3>Extracted Entities ({entities.length}):</h3>
                    <div className="entity-chips">
                      {entities.map((entity, index) => (
                        <span
                          key={index}
                          className="entity-chip"
                          onClick={() => setSelectedEntity(entity)}
                        >
                          {entity}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="section">
                <h2>3. Match Entity</h2>
                <input
                  type="text"
                  value={selectedEntity}
                  onChange={(e) => setSelectedEntity(e.target.value)}
                  placeholder="Enter entity to match"
                  className="entity-input"
                />
                
                <select
                  value={selectedStrategy}
                  onChange={(e) => setSelectedStrategy(e.target.value)}
                  className="strategy-select"
                >
                  <option value="exact">Exact Match</option>
                  <option value="fuzzy">Fuzzy Match</option>
                  <option value="contextual">Contextual Match</option>
                </select>

                <button onClick={handleMatchEntity} disabled={loading || !selectedEntity}>
                  {loading ? 'Matching...' : 'Find Matches'}
                </button>
              </div>
            </>
          )}

          <div className="section">
            <h2>4. PDF Viewer</h2>
            <PDFViewer pdfFile={pdfFile} matches={matches} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
