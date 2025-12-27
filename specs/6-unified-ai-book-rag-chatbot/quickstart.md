# Quickstart Guide: Unified AI/Spec-Driven Book with Integrated RAG Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Access to OpenAI API key
- Access to Neon Serverless Postgres (or local Postgres for development)
- Access to Qdrant Cloud (or local Qdrant for development)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database connection strings
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the documentation site
npm run build
```

### 4. Database Setup

```bash
# Run database migrations
cd backend
python -m alembic upgrade head
```

### 5. Environment Configuration

Create `.env` file in the backend directory with the following:

```env
OPENAI_API_KEY=your_openai_api_key
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key
SECRET_KEY=your_secret_key
DEBUG=true
```

## Running the Application

### 1. Start Backend API

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start Frontend Development Server

```bash
cd frontend
npm start
```

## Content Ingestion

### 1. Add Book Content

1. Add markdown files to the `frontend/docs/` directory following the module/chapter/section structure
2. Update the sidebar configuration in `frontend/sidebars.js`

### 2. Process Content for RAG

```bash
cd backend
python -m src.ingestion.process_content --module-path ../frontend/docs/module1
```

This will:
- Parse markdown content
- Split into semantically meaningful chunks
- Generate embeddings
- Store in Qdrant vector database
- Create metadata records in Postgres

## Testing the RAG Chatbot

1. Access the Docusaurus site at `http://localhost:3000`
2. Use the embedded chatbot interface
3. Ask questions related to the book content
4. Verify responses are sourced from the book content only (no hallucinations)

## API Endpoints

### Content Ingestion
- `POST /api/v1/ingest` - Process and store book content
- `POST /api/v1/ingest/chunk` - Process content with custom chunking

### RAG Query
- `POST /api/v1/query` - Submit query and get RAG response
- `POST /api/v1/query/context` - Query with specific context selection

### Sessions
- `POST /api/v1/sessions` - Create new session
- `GET /api/v1/sessions/{session_id}` - Get session history

## Deployment

### GitHub Pages for Documentation
1. Configure GitHub Actions workflow
2. Set up custom domain (optional)
3. Enable HTTPS

### Backend Deployment
Deploy the FastAPI backend to a cloud platform like:
- Render
- Vercel
- AWS
- Google Cloud Run

### Configuration for Production
- Set `DEBUG=false`
- Use production database URL
- Configure proper authentication
- Set up monitoring and logging

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Ensure sufficient OpenAI API quota
2. **Database Connection**: Verify database URL and credentials
3. **Embedding Generation**: Check Qdrant connection and API key
4. **Content Not Found**: Verify content was properly ingested into vector store

### Verification Commands

```bash
# Test backend connectivity
curl http://localhost:8000/health

# Test content ingestion
python -c "from src.ingestion import verify_ingestion; verify_ingestion()"

# Test RAG functionality
python -c "from src.rag import test_rag; test_rag()"
```