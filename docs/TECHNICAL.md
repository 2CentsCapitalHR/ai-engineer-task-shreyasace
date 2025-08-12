# 📚 Technical Documentation

## Architecture Overview

### System Design
The ADGM Corporate Agent Pro follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Presentation  │    │   Business      │    │   Data          │
│   Layer         │    │   Logic Layer   │    │   Layer         │
│                 │    │                 │    │                 │
│ • Streamlit UI  │◄──►│ • Document      │◄──►│ • Reference     │
│ • Web Interface │    │   Classification│    │   Documents     │
│ • User Actions  │    │ • Validation    │    │ • Rules Engine  │
│                 │    │ • Report Gen    │    │ • Knowledge DB  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

#### 1. Document Classifier (`src/core/classify.py`)
- **Purpose**: Identify ADGM document types
- **Technology**: Rule-based classification with AI enhancement
- **Input**: Raw document content
- **Output**: Document type, confidence score, metadata

#### 2. Validation Engine (`src/core/validate.py`)
- **Purpose**: Validate document compliance with ADGM rules
- **Technology**: Rule-based validation with pattern matching
- **Input**: Classified document
- **Output**: Validation results, compliance score, issues

#### 3. Report Generator (`src/core/report.py`)
- **Purpose**: Generate professional reports
- **Technology**: Multiple format support (Word, PDF, HTML)
- **Input**: Analysis results
- **Output**: Formatted reports with branding

#### 4. RAG System (`src/rag/`)
- **Purpose**: Retrieve relevant information from knowledge base
- **Technology**: Semantic search and retrieval
- **Input**: Query or document context
- **Output**: Relevant reference information

## API Reference

### Core Functions

#### Document Classification
```python
def classify_document(content: str) -> ClassificationResult:
    """
    Classify ADGM document type
    
    Args:
        content (str): Raw document text
        
    Returns:
        ClassificationResult: Classification with confidence score
    """
```

#### Document Validation
```python
def validate_document(doc: Document, rules: RulePack) -> ValidationResult:
    """
    Validate document against ADGM compliance rules
    
    Args:
        doc (Document): Classified document
        rules (RulePack): ADGM compliance rules
        
    Returns:
        ValidationResult: Validation results and recommendations
    """
```

#### Report Generation
```python
def generate_report(results: AnalysisResult, format: str) -> bytes:
    """
    Generate formatted report
    
    Args:
        results (AnalysisResult): Analysis results
        format (str): Report format ('word', 'pdf', 'html')
        
    Returns:
        bytes: Generated report content
    """
```

## Data Models

### Document Model
```python
@dataclass
class Document:
    content: str
    metadata: Dict[str, Any]
    doc_type: Optional[str] = None
    confidence: Optional[float] = None
    
class ClassificationResult:
    doc_type: str
    confidence: float
    metadata: Dict[str, Any]
    
class ValidationResult:
    is_valid: bool
    compliance_score: float
    issues: List[ValidationIssue]
    recommendations: List[str]
```

### Configuration Model
```python
@dataclass
class RulePack:
    name: str
    version: str
    rules: List[Rule]
    
@dataclass
class Rule:
    id: str
    name: str
    description: str
    pattern: str
    severity: str  # 'error', 'warning', 'info'
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Document all public functions with docstrings
- Maximum line length: 100 characters

### Testing
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_classify.py::test_document_classification
```

### Adding New Document Types
1. Update `src/rules/rulepacks.yaml`
2. Add classification patterns in `src/core/classify.py`
3. Create validation rules in `src/core/validate.py`
4. Add tests in `tests/`

### Adding New Report Formats
1. Create new generator in `src/core/`
2. Update `generate_report()` function
3. Add format option to UI
4. Test with sample documents

## Deployment

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export STREAMLIT_ENV=production
export DEBUG_MODE=false

# Run with gunicorn for production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

### Environment Variables
```bash
# Application settings
STREAMLIT_PORT=8501
STREAMLIT_ENV=production
DEBUG_MODE=false

# File upload settings
MAX_UPLOAD_SIZE=50  # MB
UPLOAD_TIMEOUT=300  # seconds

# RAG settings
KNOWLEDGE_BASE_PATH=./references
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Security Considerations

### Data Privacy
- All document processing is done locally
- No data is sent to external services
- Temporary files are cleaned after processing
- User uploads are not stored permanently

### Input Validation
- File type validation (DOCX, PDF, TXT only)
- File size limits (50MB default)
- Content sanitization for malicious inputs
- Path traversal protection

### Access Control
- Session-based state management
- No persistent user data storage
- Secure file handling
- Input validation and sanitization

## Performance Optimization

### Memory Management
- Process documents in chunks for large files
- Clear session state after analysis
- Implement garbage collection for temporary files
- Monitor memory usage during batch processing

### Caching Strategy
```python
# Cache expensive operations
@st.cache_data
def load_knowledge_base():
    """Cache knowledge base loading"""
    pass

@st.cache_data
def classify_document_cached(content_hash: str):
    """Cache classification results"""
    pass
```

### Scalability
- Use streaming for large file uploads
- Implement batch processing for multiple documents
- Consider async processing for I/O operations
- Monitor resource usage and set limits

## Troubleshooting

### Common Issues

#### Memory Errors
```bash
# Increase memory limit
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200

# Process files in smaller batches
# Restart application if processing many large files
```

#### Performance Issues
```bash
# Enable caching
export STREAMLIT_CACHE_ENABLED=true

# Use SSD storage for better I/O performance
# Monitor CPU and memory usage
```

#### Module Import Errors
```bash
# Ensure PYTHONPATH is set correctly
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify all dependencies are installed
pip install -r requirements.txt --force-reinstall
```

### Debugging

#### Enable Debug Mode
```python
# Set debug mode in app.py
DEBUG_MODE = True

# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Performance Profiling
```python
# Profile specific functions
import cProfile
cProfile.run('your_function()')

# Memory profiling
from memory_profiler import profile
@profile
def your_function():
    pass
```

## Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd shreyas-assignment

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # if exists

# Pre-commit hooks
pre-commit install
```

### Testing Guidelines
- Write tests for all new features
- Maintain >90% code coverage
- Test with various document types
- Include integration tests
- Test UI components with sample data

### Code Review Process
1. Create feature branch from main
2. Implement changes with tests
3. Update documentation
4. Submit pull request
5. Address review feedback
6. Merge after approval

## Changelog

### Version 1.0.0 (Current)
- Initial release with core functionality
- Document classification and validation
- Multi-format report generation
- Beautiful web interface
- ADGM compliance rules
- RAG-based knowledge retrieval

### Planned Features
- [ ] Batch processing improvements
- [ ] Additional document types
- [ ] API endpoints
- [ ] User authentication
- [ ] Document comparison
- [ ] Advanced analytics dashboard
