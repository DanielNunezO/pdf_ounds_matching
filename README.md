# PDF Bounds Matching Challenge

A sophisticated PDF text matching challenge repository with Python 3.10+ backend and Node.js 18+ frontend. This application uses Strategy and Factory design patterns to locate extracted entities in PDFs using advanced text matching algorithms.

## Features

### Backend (Python 3.10+)
- **PDF Text Extraction**: Extract text with bounding box coordinates using pdfplumber
- **Multi-Strategy Matching Engine**:
  - **Exact Match**: Case-insensitive exact string matching
  - **Fuzzy Match**: Levenshtein distance-based matching with confidence scores
  - **Contextual Match**: Multi-word entity matching with surrounding context
- **LLM Integration**: Entity extraction using OpenAI's GPT models
- **RESTful API**: FastAPI-based backend with comprehensive endpoints
- **Design Patterns**:
  - Strategy Pattern for matching algorithms
  - Factory Pattern for strategy instantiation

### Frontend (Node.js 18+)
- **PDF Viewer**: Client-side PDF viewing with bounds visualization
- **30-Minute Timer**: Countdown timer for challenge tracking
- **Paste Detection**: Tracks and logs paste events
- **Interactive UI**: 
  - Upload and process PDFs
  - Extract entities using LLM
  - Match entities with selectable strategies
  - Visualize matches with confidence-based highlighting

## Architecture

```
pdf_ounds_matching/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── pdf_extractor.py     # PDF text extraction
│   │   ├── matching_strategies.py # Strategy pattern implementation
│   │   ├── strategy_factory.py  # Factory pattern implementation
│   │   └── llm_extractor.py     # LLM entity extraction
│   ├── tests/                   # Backend tests
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment configuration
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Timer.jsx       # 30-min timer component
│   │   │   ├── PasteDetection.jsx # Paste tracking
│   │   │   └── PDFViewer.jsx   # PDF viewer with bounds
│   │   ├── services/
│   │   │   └── api.js          # API service
│   │   ├── App.jsx             # Main application
│   │   └── main.jsx            # Entry point
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Vite configuration
└── README.md
```

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher
- **OpenAI API Key**: For entity extraction (optional but recommended)

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

6. Run the backend server:
```bash
cd app
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage

### 1. Start Both Servers

Make sure both backend (port 8000) and frontend (port 3000) are running.

### 2. Upload a PDF

- Click "Choose File" in the "Upload PDF" section
- Select a PDF file from your computer
- The application will automatically extract text with position information

### 3. Extract Entities (Optional)

- Click "Extract Entities" to use LLM for automatic entity extraction
- Note: Requires OpenAI API key to be configured
- Extracted entities will appear as clickable chips

### 4. Match Entities

- Enter an entity manually or click an extracted entity chip
- Select a matching strategy:
  - **Exact**: For precise word matching
  - **Fuzzy**: For handling typos and variations
  - **Contextual**: For multi-word entities with context
- Click "Find Matches" to locate the entity in the PDF

### 5. View Results

- Matched text will be highlighted in the PDF viewer
- Color indicates confidence: Green (high), Orange (medium), Red (low)
- Hover over highlights to see confidence scores

### 6. Track Your Progress

- **Timer**: 30-minute countdown for the challenge
- **Paste Detection**: Monitors clipboard activity

## API Documentation

### Endpoints

#### `POST /api/upload-pdf`
Upload a PDF file for processing.

**Request**: Multipart form data with PDF file

**Response**:
```json
{
  "file_id": "string",
  "filename": "string",
  "message": "PDF uploaded successfully"
}
```

#### `GET /api/extract-text/{file_id}`
Extract text with bounding boxes from uploaded PDF.

**Response**:
```json
{
  "file_id": "string",
  "full_text": "string",
  "text_bounds": [
    {
      "text": "string",
      "x0": 0.0,
      "y0": 0.0,
      "x1": 0.0,
      "y1": 0.0,
      "page": 0
    }
  ],
  "total_words": 0
}
```

#### `POST /api/extract-entities`
Extract entities from text using LLM.

**Request**:
```json
{
  "text": "string",
  "entity_types": ["PERSON", "ORGANIZATION"] // optional
}
```

**Response**:
```json
{
  "entities": ["entity1", "entity2"],
  "count": 2
}
```

#### `POST /api/match/{file_id}`
Match entity in PDF using specified strategy.

**Request**:
```json
{
  "entity": "string",
  "strategy": "exact|fuzzy|contextual",
  "threshold": 80.0,
  "context_window": 3
}
```

**Response**:
```json
{
  "file_id": "string",
  "entity": "string",
  "strategy": "string",
  "matches": [
    {
      "match": {
        "text": "string",
        "x0": 0.0,
        "y0": 0.0,
        "x1": 0.0,
        "y1": 0.0,
        "page": 0
      },
      "confidence": 100.0,
      "context": "optional context string"
    }
  ],
  "match_count": 1
}
```

#### `GET /api/strategies`
Get available matching strategies with descriptions.

#### `DELETE /api/cleanup/{file_id}`
Clean up uploaded PDF file.

## Testing

### Backend Tests

```bash
cd backend
pytest
```

Run specific test file:
```bash
pytest tests/test_matching_strategies.py
```

Run with coverage:
```bash
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Design Patterns

### Strategy Pattern

The matching engine uses the Strategy pattern to encapsulate different matching algorithms:

```python
# Strategy interface
class MatchingStrategy(ABC):
    @abstractmethod
    def match(self, entity, text_bounds):
        pass

# Concrete strategies
class ExactMatchingStrategy(MatchingStrategy):
    def match(self, entity, text_bounds):
        # Exact matching logic
        
class FuzzyMatchingStrategy(MatchingStrategy):
    def match(self, entity, text_bounds):
        # Fuzzy matching logic
```

### Factory Pattern

The Factory pattern creates strategy instances based on type:

```python
class MatchingStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type, **kwargs):
        strategies = {
            'exact': ExactMatchingStrategy,
            'fuzzy': FuzzyMatchingStrategy,
            'contextual': ContextualMatchingStrategy
        }
        return strategies[strategy_type](**kwargs)
```

## Technologies Used

### Backend
- **FastAPI**: Modern web framework for building APIs
- **pdfplumber**: PDF text extraction with coordinates
- **rapidfuzz**: Fast fuzzy string matching
- **OpenAI API**: LLM-based entity extraction
- **pytest**: Testing framework

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **CSS**: Styling

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is created for educational purposes.

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError` when running tests
- **Solution**: Make sure you're in the backend directory and virtual environment is activated

**Issue**: OpenAI API errors
- **Solution**: Verify your API key is correctly set in `.env` file

### Frontend Issues

**Issue**: `ECONNREFUSED` when calling API
- **Solution**: Ensure backend server is running on port 8000

**Issue**: PDF not displaying
- **Solution**: Check browser console for errors; some browsers may block PDF loading

## Future Enhancements

- [ ] Add more matching strategies (semantic, phonetic)
- [ ] Support for multiple PDFs simultaneously
- [ ] User authentication and session management
- [ ] Results export functionality
- [ ] Advanced visualization options
- [ ] Support for scanned PDFs with OCR
- [ ] WebSocket for real-time updates
- [ ] Dockerization for easy deployment

## Contact

For questions or issues, please open an issue in the repository.
