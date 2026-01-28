# API Reference

Complete API reference for the PDF Bounds Matching backend.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### `GET /`

Check if the API is running.

**Response:**
```json
{
  "message": "PDF Bounds Matching API",
  "status": "running",
  "version": "1.0.0"
}
```

---

### Upload PDF

#### `POST /api/upload-pdf`

Upload a PDF file for processing.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: File with key `file`

**Response:**
```json
{
  "file_id": "tmp2x8yz9ab",
  "filename": "document.pdf",
  "message": "PDF uploaded successfully"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid file (not a PDF)
- `500`: Server error

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/upload-pdf \
  -F "file=@document.pdf"
```

---

### Extract Text

#### `GET /api/extract-text/{file_id}`

Extract text with bounding boxes from uploaded PDF.

**Parameters:**
- `file_id` (path): The file ID returned from upload

**Response:**
```json
{
  "file_id": "tmp2x8yz9ab",
  "full_text": "Complete text content...",
  "text_bounds": [
    {
      "text": "Hello",
      "x0": 10.5,
      "y0": 20.3,
      "x1": 35.7,
      "y1": 28.9,
      "page": 0
    }
  ],
  "total_words": 1234
}
```

**Status Codes:**
- `200`: Success
- `404`: File not found
- `500`: Extraction error

**Example (curl):**
```bash
curl http://localhost:8000/api/extract-text/tmp2x8yz9ab
```

---

### Extract Entities

#### `POST /api/extract-entities`

Extract entities from text using LLM.

**Request Body:**
```json
{
  "text": "John Doe works at Acme Corp in New York.",
  "entity_types": ["PERSON", "ORGANIZATION", "LOCATION"]
}
```

**Parameters:**
- `text` (required): Text to extract entities from
- `entity_types` (optional): Types of entities to extract

**Response:**
```json
{
  "entities": [
    "John Doe",
    "Acme Corp",
    "New York"
  ],
  "count": 3
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request or API key not configured
- `500`: LLM error

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/extract-entities \
  -H "Content-Type: application/json" \
  -d '{"text": "John Doe works at Acme Corp."}'
```

---

### Extract Named Entities

#### `POST /api/extract-named-entities`

Extract categorized named entities from text.

**Request Body:**
```json
{
  "text": "John Doe works at Acme Corp in New York on January 1, 2024."
}
```

**Response:**
```json
{
  "entities": {
    "PERSON": ["John Doe"],
    "ORGANIZATION": ["Acme Corp"],
    "LOCATION": ["New York"],
    "DATE": ["January 1, 2024"]
  },
  "total_count": 4
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request or API key not configured
- `500`: LLM error

---

### Match Entity

#### `POST /api/match/{file_id}`

Match an entity in the PDF using a specified strategy.

**Parameters:**
- `file_id` (path): The file ID returned from upload

**Request Body:**
```json
{
  "entity": "machine learning",
  "strategy": "fuzzy",
  "threshold": 80.0,
  "context_window": 3
}
```

**Request Parameters:**
- `entity` (required): Entity text to match
- `strategy` (required): One of `exact`, `fuzzy`, `contextual`
- `threshold` (optional): Minimum confidence (0-100), default 80.0
- `context_window` (optional): Context window size, default 3

**Response:**
```json
{
  "file_id": "tmp2x8yz9ab",
  "entity": "machine learning",
  "strategy": "fuzzy",
  "matches": [
    {
      "match": {
        "text": "machine learning",
        "x0": 45.2,
        "y0": 100.5,
        "x1": 120.8,
        "y1": 115.3,
        "page": 0
      },
      "confidence": 100.0,
      "context": "... artificial intelligence and machine learning are transforming ..."
    }
  ],
  "match_count": 1
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid strategy or parameters
- `404`: File not found
- `500`: Matching error

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/match/tmp2x8yz9ab \
  -H "Content-Type: application/json" \
  -d '{
    "entity": "machine learning",
    "strategy": "fuzzy",
    "threshold": 80.0
  }'
```

---

### Get Strategies

#### `GET /api/strategies`

Get available matching strategies with descriptions.

**Response:**
```json
{
  "strategies": [
    {
      "name": "exact",
      "description": "Exact string matching",
      "parameters": []
    },
    {
      "name": "fuzzy",
      "description": "Fuzzy matching using Levenshtein distance",
      "parameters": [
        {
          "name": "threshold",
          "type": "float",
          "default": 80.0,
          "description": "Minimum confidence score (0-100)"
        }
      ]
    },
    {
      "name": "contextual",
      "description": "Contextual matching considering surrounding text",
      "parameters": [
        {
          "name": "threshold",
          "type": "float",
          "default": 70.0,
          "description": "Minimum confidence score (0-100)"
        },
        {
          "name": "context_window",
          "type": "int",
          "default": 3,
          "description": "Number of surrounding words to consider"
        }
      ]
    }
  ]
}
```

**Example (curl):**
```bash
curl http://localhost:8000/api/strategies
```

---

### Clean Up PDF

#### `DELETE /api/cleanup/{file_id}`

Remove uploaded PDF file from server.

**Parameters:**
- `file_id` (path): The file ID to remove

**Response:**
```json
{
  "message": "PDF file cleaned up successfully"
}
```

**Status Codes:**
- `200`: Success
- `404`: File not found
- `500`: Cleanup error

**Example (curl):**
```bash
curl -X DELETE http://localhost:8000/api/cleanup/tmp2x8yz9ab
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with:
- Try-it-out functionality
- Request/response examples
- Schema definitions
- Authentication (if configured)

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error description here"
}
```

Common HTTP status codes:
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error (server-side error)

## Rate Limiting

Currently, there are no rate limits. In production:
- Consider implementing rate limiting
- Monitor OpenAI API usage
- Add authentication for security

## CORS

The API allows cross-origin requests from all origins (`*`). In production:
- Configure specific allowed origins
- Enable credentials if needed
- Add proper security headers
