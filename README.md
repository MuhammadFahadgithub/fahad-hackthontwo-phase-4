# Todo Chatbot Application

This project implements a cloud-native Todo Chatbot application with both chat interface and web UI, deployed to a local Kubernetes cluster using AI-assisted tools.

## Architecture

The application follows a microservices architecture with:

- **Frontend**: React-based web interface for todo management
- **Backend**: FastAPI-based service for business logic and API endpoints
- **Database**: PostgreSQL for persistent storage
- **Deployment**: Helm charts for Kubernetes deployment

## Features

1. **Chat Interface**: Natural language processing for todo management
2. **Web UI**: Traditional interface for todo management
3. **AI Operations**: Integration with AI tools for deployment and management

## Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Frontend**: React, Next.js
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Orchestration**: Kubernetes, Helm
- **AI Tools**: Gordon (Docker AI), kubectl-ai, kagent

## Getting Started

### Prerequisites

- Docker Desktop (v4.38+ with Docker AI enabled)
- Minikube
- kubectl
- Helm 3
- kubectl-ai plugin
- Gordon (Docker AI Agent)

### Local Development

1. Start Minikube:
   ```bash
   minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=docker
   minikube addons enable ingress
   minikube addons enable metrics-server
   ```

2. Set Docker environment to use Minikube's container registry:
   ```bash
   eval $(minikube docker-env)
   ```

3. Build Docker images:
   ```bash
   # Build backend
   cd backend
   docker build -t todo-backend:latest -f ../docker/backend/Dockerfile .
   
   # Build frontend
   cd ../frontend
   docker build -t todo-frontend:latest -f ../docker/frontend/Dockerfile .
   ```

4. Deploy using Helm:
   ```bash
   cd ../helm/todo-chatbot
   helm install todo-chatbot . --namespace todo-chatbot --create-namespace
   ```

## AI-Assisted Operations

This project leverages AI tools for various operations:

- **Gordon**: Used for Docker operations and optimization
- **kubectl-ai**: Used for Kubernetes operations with natural language
- **kagent**: Used for cluster analysis and optimization

See the [AI Operations Guide](docs/ai-operations-guide.md) for more details.

## Project Structure

```
backend/                 # Backend service (FastAPI)
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── api/             # API endpoints
│   ├── database/        # Database setup
│   └── utils/           # Utility functions
frontend/               # Frontend service (React)
├── src/
│   ├── components/      # React components
│   ├── services/        # API clients
│   └── store/           # State management
helm/                   # Helm charts
└── todo-chatbot/       # Main chart
    ├── templates/      # Kubernetes manifests
    └── values.yaml     # Configuration values
docker/                 # Docker configurations
├── frontend/           # Frontend Dockerfile
└── backend/            # Backend Dockerfile
scripts/                # Utility scripts
docs/                   # Documentation
specs/                  # Specification files
```

## Testing

Unit and integration tests are available in the `tests/` directory. Run them with:

```bash
# Backend tests
cd backend
poetry run pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

The application is designed for Kubernetes deployment using Helm charts. The deployment includes:

- Horizontal Pod Autoscaling
- Health checks and readiness probes
- Resource limits and requests
- Secrets management
- Ingress configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.