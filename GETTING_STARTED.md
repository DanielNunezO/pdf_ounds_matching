# Getting Started Guide

This guide will help you get the PDF Bounds Matching Challenge application up and running quickly.

## Quick Start

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional - needed for LLM features)
cp .env.example .env
# Edit .env and add your OpenAI API key if you want to use entity extraction

# Run the backend
cd app
python main.py
```

The backend API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation.

### 2. Frontend Setup (5 minutes)

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Your First PDF Match

1. **Start both servers** (backend on port 8000, frontend on port 3000)

2. **Open the application** in your browser at `http://localhost:3000`

3. **Upload a PDF**:
   - Click "Choose File" 
   - Select any PDF document
   - The text will be automatically extracted

4. **Try matching**:
   - Enter a word that appears in your PDF (e.g., "the", "and")
   - Select "Exact Match" strategy
   - Click "Find Matches"
   - See the results highlighted in the PDF viewer

5. **Try LLM extraction** (optional, requires OpenAI API key):
   - Click "Extract Entities"
   - The LLM will identify entities in your document
   - Click any entity chip to search for it

## Testing Without a PDF

If you don't have a PDF handy, you can:

1. Create a simple text document in Microsoft Word or Google Docs
2. Save/Export it as a PDF
3. Upload it to the application

Or use the API directly:

```bash
# Test the backend API
curl http://localhost:8000/
curl http://localhost:8000/api/strategies
```

## Common Issues

### Backend won't start
- **Python version**: Ensure you're using Python 3.10 or higher
- **Dependencies**: Make sure all packages installed without errors
- **Port conflict**: Make sure port 8000 is not in use

### Frontend won't start
- **Node version**: Ensure you're using Node.js 18 or higher
- **Dependencies**: Try deleting `node_modules` and running `npm install` again
- **Port conflict**: Make sure port 3000 is not in use

### "Cannot connect to API" error
- Make sure the backend is running on port 8000
- Check browser console for CORS errors
- Verify the backend URL in `frontend/src/services/api.js`

### OpenAI API errors
- Verify your API key is correct in `.env`
- Check that you have available credits in your OpenAI account
- You can skip entity extraction and manually enter entities if needed

## Next Steps

- Read the [README.md](../README.md) for detailed documentation
- Explore the API at `http://localhost:8000/docs`
- Check out the [Design Patterns](#design-patterns-used) section in the README
- Run the tests: `cd backend && pytest -v`

## Tips

- Start the timer before you begin working
- The paste detection tracks clipboard usage automatically
- Try different matching strategies:
  - **Exact**: Best for precise matches
  - **Fuzzy**: Handles typos and variations
  - **Contextual**: Good for multi-word phrases

Enjoy exploring the PDF Bounds Matching Challenge!
