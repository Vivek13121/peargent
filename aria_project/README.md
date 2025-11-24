# 🏢 ARIA - Advanced Research & Intelligence Assistant

A sophisticated multi-agent AI system for automated research, analysis, and intelligence gathering with enterprise-grade features.

## 🎯 Overview

ARIA is a production-ready platform that orchestrates 12+ specialized AI agents to conduct comprehensive research, perform deep analysis, and generate actionable intelligence reports. Built on Peargent, it showcases advanced multi-agent patterns, distributed systems architecture, and enterprise observability.

## ✨ Key Features

### Multi-Agent Architecture
- **Research Agents**: Web, Academic, Social Media, Competitor Analysis
- **Analysis Agents**: Data Analysis, Sentiment Analysis, Trend Detection, Fact Checking
- **Synthesis Agents**: Report Writing, Summarization, Citation Management, Visualization
- **Orchestration**: Intelligent coordination, quality control, priority routing

### Enterprise Capabilities
- 🔒 **Authentication & Authorization**: JWT-based auth, role-based access
- 📊 **Full Observability**: Distributed tracing, metrics, logging, alerting
- 💰 **Cost Management**: Budget tracking, cost optimization, usage analytics
- 🚀 **Scalability**: Horizontal scaling, load balancing, caching
- 📈 **Analytics Dashboard**: Real-time metrics, agent performance, cost analytics
- 🔄 **Background Processing**: Celery workers for long-running tasks

### Advanced Features
- Vector search with Pinecone/Weaviate for knowledge retrieval
- Real-time collaboration via WebSocket
- Multi-source data aggregation and deduplication
- Automated fact-checking and source verification
- Citation management with academic formatting
- Export to PDF, DOCX, Markdown
- Scheduled research reports
- Email/Slack notifications

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         API Gateway                          │
│                    (FastAPI + WebSocket)                     │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼────────┐      ┌─────────▼──────┐
│  REST API  │      │   WebSocket    │
│  Endpoints │      │    Streaming   │
└───┬────────┘      └─────────┬──────┘
    │                         │
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────────────────┐
    │      Research Orchestrator          │
    │    (Intelligent Agent Router)       │
    └────┬─────────────────────────┬──────┘
         │                         │
    ┌────▼────────┐       ┌───────▼────────┐
    │  Research   │       │    Analysis    │
    │  Pipeline   │──────▶│    Pipeline    │
    │             │       │                │
    │ - WebSearch │       │ - DataAnalysis │
    │ - Academic  │       │ - Sentiment    │
    │ - SocialMed │       │ - TrendDetect  │
    │ - Competitor│       │ - FactCheck    │
    └────┬────────┘       └───────┬────────┘
         │                        │
         └────────────┬───────────┘
                      │
              ┌───────▼────────┐
              │   Synthesis    │
              │    Pipeline    │
              │                │
              │ - ReportWriter │
              │ - Summarizer   │
              │ - Citations    │
              │ - Visualizer   │
              └───────┬────────┘
                      │
         ┌────────────▼─────────────┐
         │     Storage Layer        │
         ├──────────────────────────┤
         │ PostgreSQL │ Redis       │
         │ (Primary)  │ (Cache)     │
         ├────────────┼─────────────┤
         │ Pinecone   │ S3          │
         │ (Vector)   │ (Documents) │
         └────────────┴─────────────┘
```

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# Docker & Docker Compose
docker --version
docker-compose --version
```

### Installation

```bash
# Clone repository
git clone https://github.com/yourorg/aria.git
cd aria

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start infrastructure (PostgreSQL, Redis, etc.)
docker-compose up -d

# Initialize database
python scripts/setup_db.py

# Start application
uvicorn aria.main:app --reload
```

### Access

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

## 📖 Usage Examples

### 1. Simple Research Request

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/research",
    json={
        "query": "Latest developments in quantum computing",
        "depth": "comprehensive",
        "sources": ["web", "academic", "social"],
        "output_format": "report"
    }
)

research_id = response.json()["research_id"]
print(f"Research started: {research_id}")
```

### 2. Real-Time Streaming

```python
import asyncio
import websockets
import json

async def stream_research():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        # Start research
        await ws.send(json.dumps({
            "action": "start_research",
            "query": "AI safety trends 2024"
        }))

        # Stream updates
        async for message in ws:
            data = json.loads(message)
            if data["type"] == "agent_update":
                print(f"[{data['agent']}] {data['message']}")
            elif data["type"] == "progress":
                print(f"Progress: {data['percentage']}%")
            elif data["type"] == "complete":
                print(f"Report ready: {data['report_url']}")
                break

asyncio.run(stream_research())
```

### 3. Scheduled Research

```python
# Schedule daily competitor analysis
response = requests.post(
    "http://localhost:8000/api/v1/research/schedule",
    json={
        "query": "Competitor product launches",
        "schedule": "0 9 * * *",  # Daily at 9 AM
        "notify": ["email", "slack"]
    }
)
```

### 4. Cost Analytics

```python
# Get cost breakdown
response = requests.get(
    "http://localhost:8000/api/v1/analytics/costs",
    params={
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "group_by": "agent"
    }
)

costs = response.json()
for agent, cost in costs["breakdown"].items():
    print(f"{agent}: ${cost:.2f}")
```

## 🔧 Configuration

### Agent Configuration

Edit `aria/config/agents_config.yaml`:

```yaml
research_agents:
  web_researcher:
    model: groq/llama-3.3-70b-versatile
    temperature: 0.7
    max_tokens: 4000
    tools:
      - google_search
      - web_scraper
      - content_extractor
    retry:
      max_attempts: 3
      backoff: exponential

  academic_researcher:
    model: openai/gpt-4o
    temperature: 0.5
    tools:
      - arxiv_search
      - pubmed_search
      - pdf_parser
```

### Pipeline Configuration

Edit `aria/config/pipelines_config.yaml`:

```yaml
full_report_pipeline:
  stages:
    - name: research
      agents: [web_researcher, academic_researcher]
      parallel: true
      timeout: 300

    - name: analysis
      agents: [data_analyst, sentiment_analyzer]
      depends_on: research

    - name: synthesis
      agents: [report_writer, citation_manager]
      depends_on: analysis
```

## 📊 Monitoring

### Metrics Dashboard

Access Grafana at http://localhost:3000

**Key Metrics:**
- Agent execution time
- Success/failure rates
- Cost per research
- Queue depth
- API latency

### Tracing

View distributed traces in Jaeger: http://localhost:16686

### Logs

```bash
# View real-time logs
docker-compose logs -f aria

# Search logs
docker-compose exec aria python scripts/search_logs.py --query "error"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit

# Integration tests
pytest tests/integration

# With coverage
pytest --cov=aria --cov-report=html
```

## 📦 Deployment

### Docker

```bash
# Build image
docker build -t aria:latest .

# Run container
docker run -p 8000:8000 aria:latest
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deploy/kubernetes/

# Check status
kubectl get pods -n aria
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `GROQ_API_KEY` | Groq API key | Yes |
| `OPENAI_API_KEY` | OpenAI API key | No |
| `PINECONE_API_KEY` | Pinecone vector DB key | No |
| `SLACK_WEBHOOK_URL` | Slack notifications | No |
| `SENTRY_DSN` | Error tracking | No |

## 🏢 Enterprise Features

### Multi-Tenancy

```python
# Tenant isolation
response = requests.post(
    "http://localhost:8000/api/v1/research",
    headers={"X-Tenant-ID": "acme-corp"},
    json={...}
)
```

### Role-Based Access Control

```yaml
roles:
  admin:
    - research:create
    - research:read
    - research:delete
    - agents:configure

  analyst:
    - research:create
    - research:read

  viewer:
    - research:read
```

### Audit Logging

All actions are logged with:
- User ID
- Tenant ID
- Timestamp
- Action type
- Resource affected
- IP address

## 🤝 Contributing

See [CONTRIBUTING.md](docs/contributing.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [Peargent](https://github.com/yourorg/peargent) - Multi-agent framework
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Celery](https://docs.celeryproject.org/) - Task queue
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Redis](https://redis.io/) - Cache
- [Pinecone](https://www.pinecone.io/) - Vector database

## 📞 Support

- **Documentation**: https://aria-docs.example.com
- **Issues**: https://github.com/yourorg/aria/issues
- **Discussions**: https://github.com/yourorg/aria/discussions
- **Slack**: https://aria-community.slack.com