# Contributing Guide

Thank you for your interest in contributing to the PDF Bounds Matching Challenge!

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pdf_ounds_matching.git
   cd pdf_ounds_matching
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for classes and functions
- Keep functions focused and small
- Maximum line length: 100 characters

**Example:**
```python
def match(self, entity: str, text_bounds: List[TextBound]) -> List[MatchResult]:
    """
    Find matches for an entity in the extracted text bounds.
    
    Args:
        entity: The entity text to match
        text_bounds: List of text bounds from PDF
        
    Returns:
        List of MatchResult objects
    """
    pass
```

### JavaScript/React (Frontend)

- Use ES6+ features
- Prefer functional components with hooks
- Use meaningful variable names
- Add comments for complex logic
- Keep components focused and reusable

**Example:**
```javascript
/**
 * Timer Component
 * 
 * 30-minute countdown timer for the challenge
 */
const Timer = ({ onTimeUp }) => {
  // Component implementation
};
```

## Testing

### Backend Tests

Run all tests:
```bash
cd backend
source venv/bin/activate
pytest -v
```

Run specific test:
```bash
pytest tests/test_matching_strategies.py -v
```

Run with coverage:
```bash
pytest --cov=app tests/
```

### Writing Tests

- Write tests for new features
- Follow existing test patterns
- Use descriptive test names
- Test edge cases

**Example:**
```python
def test_exact_match_case_insensitive(self, sample_text_bounds):
    """Test that exact matching is case-insensitive."""
    strategy = ExactMatchingStrategy()
    results = strategy.match("hello", sample_text_bounds)
    
    assert len(results) == 2
    assert all(r.confidence == 100.0 for r in results)
```

## Adding New Features

### New Matching Strategy

1. Create strategy class in `backend/app/matching_strategies.py`:
   ```python
   class MyNewStrategy(MatchingStrategy):
       def match(self, entity, text_bounds):
           # Implementation
           pass
   ```

2. Register in factory `backend/app/strategy_factory.py`:
   ```python
   strategies = {
       'exact': ExactMatchingStrategy,
       'fuzzy': FuzzyMatchingStrategy,
       'contextual': ContextualMatchingStrategy,
       'mynew': MyNewStrategy  # Add here
   }
   ```

3. Add tests in `backend/tests/test_matching_strategies.py`

4. Update API documentation

### New Frontend Component

1. Create component in `frontend/src/components/`:
   ```javascript
   const MyComponent = () => {
     // Component code
   };
   export default MyComponent;
   ```

2. Import and use in `App.jsx`:
   ```javascript
   import MyComponent from './components/MyComponent';
   ```

3. Add styles in `App.css` or inline

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**
   ```bash
   # Backend
   cd backend && pytest -v
   
   # Manual testing
   python app/main.py  # Test backend
   cd ../frontend && npm run dev  # Test frontend
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

6. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Provide clear description
   - Reference any related issues

## Pull Request Guidelines

- **Title**: Clear and descriptive
- **Description**: 
  - What changes were made
  - Why these changes were needed
  - How to test the changes
- **Tests**: Include tests for new features
- **Documentation**: Update docs if needed
- **One feature per PR**: Keep PRs focused

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, Node version)

**Template:**
```markdown
**Bug Description:**
Brief description of what's wrong

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10.5
- Node: 18.16.0
```

### Feature Requests

Include:
- Clear description of the feature
- Use case/motivation
- Proposed implementation (optional)
- Examples (if applicable)

## Areas for Contribution

### Backend

- [ ] Add more matching strategies (semantic, phonetic)
- [ ] Implement caching for PDF extraction
- [ ] Add support for scanned PDFs with OCR
- [ ] Improve error handling
- [ ] Add authentication/authorization
- [ ] Performance optimization

### Frontend

- [ ] Improve PDF viewer (zoom, pan)
- [ ] Add results export (JSON, CSV)
- [ ] Better mobile responsiveness
- [ ] Add keyboard shortcuts
- [ ] Implement undo/redo
- [ ] Add dark/light theme toggle

### Documentation

- [ ] Video tutorials
- [ ] More code examples
- [ ] Architecture diagrams
- [ ] Performance benchmarks
- [ ] Deployment guides

### Testing

- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Performance tests
- [ ] Frontend unit tests

## Code Review

All contributions will be reviewed for:
- Code quality and style
- Test coverage
- Documentation
- Performance
- Security

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Read the documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
