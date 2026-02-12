# Todo Chatbot Quickstart Guide

## Overview
This guide provides step-by-step instructions to deploy the Todo Chatbot application to a local Kubernetes cluster using AI-assisted tools.

## Prerequisites
- Docker Desktop (v4.38+ with Docker AI enabled in Beta features)
- Minikube (latest version)
- kubectl
- Helm 3
- kubectl-ai plugin
- Gordon (Docker AI Agent)

## Setup Instructions

### 1. Start Minikube
```bash
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=docker
minikube addons enable ingress
minikube addons enable metrics-server
```

### 2. Configure Docker to use Minikube's container registry
```bash
eval $(minikube docker-env)
```

### 3. Build Docker Images using Gordon
```bash
# Navigate to frontend directory
cd frontend

# Use Gordon to create optimized Dockerfile
docker ai "create optimized multi-stage Dockerfile for React app named todo-frontend"

# Build the frontend image
docker ai "build optimized production image for React app named todo-frontend:v1.0.0"

# Navigate to backend directory
cd ../backend

# Use Gordon to create optimized Dockerfile
docker ai "create optimized multi-stage Dockerfile for Python FastAPI app named todo-backend"

# Build the backend image
docker ai "build optimized production image for FastAPI app named todo-backend:v1.0.0"
```

### 4. Deploy PostgreSQL using Helm
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql \
  --namespace todo-chatbot \
  --create-namespace \
  --set auth.username=todouser \
  --set auth.password=todopass \
  --set auth.database=tododb \
  --set primary.persistence.size=5Gi
```

### 5. Create Application Secrets
```bash
kubectl create secret generic postgres-credentials \
  --from-literal=url="postgresql://todouser:todopass@postgres:5432/tododb" \
  -n todo-chatbot

kubectl create secret generic openai-credentials \
  --from-literal=api-key="$OPENAI_API_KEY" \
  -n todo-chatbot
```

### 6. Deploy Todo Chatbot using Helm
```bash
cd helm/todo-chatbot

# Use kubectl-ai to generate appropriate values for your environment
kubectl-ai "generate Helm values.yaml for local development with 1 replica each"

# Install the Helm chart
helm install todo-chatbot . --namespace todo-chatbot --create-namespace --values values-dev.yaml
```

### 7. Verify Deployment
```bash
# Check if all pods are running
kubectl get pods -n todo-chatbot

# Check services
kubectl get services -n todo-chatbot

# Check ingress
kubectl get ingress -n todo-chatbot

# Use kagent to analyze cluster health
kagent "analyze cluster health for todo-chatbot deployment"
```

### 8. Access the Application
```bash
# Get the Minikube IP
minikube ip

# Add to your hosts file:
# <MINIKUBE_IP> todo-chatbot.local

# Access the application
open http://todo-chatbot.local
```

## AI-Assisted Commands

### Using Gordon (Docker AI)
```bash
# Optimize existing Dockerfile
docker ai "optimize this Dockerfile for size and security"

# Troubleshoot image issues
docker ai "why is my image failing to start and how can I fix it"

# Scan for vulnerabilities
docker ai "scan todo-backend:v1.0.0 for security vulnerabilities"
```

### Using kubectl-ai
```bash
# Generate Kubernetes manifests
kubectl-ai "create a deployment yaml for a React frontend with 2 replicas"

# Troubleshoot issues
kubectl-ai "explain why my pod is in CrashLoopBackOff and suggest fix"

# Generate scaling configurations
kubectl-ai "generate HPA configuration for backend based on CPU and memory"
```

### Using kagent
```bash
# Analyze cluster health
kagent "analyze the cluster health after deployment"

# Optimize resource allocation
kagent "optimize resource allocation for these deployments"

# Perform advanced analysis
kagent "run comprehensive analysis on todo-chatbot namespace"
```

## Troubleshooting

### Common Issues

1. **Images not found**: Make sure to run `eval $(minikube docker-env)` before building images
2. **Ingress not working**: Ensure the ingress addon is enabled in Minikube
3. **Database connection issues**: Verify that PostgreSQL is running and credentials are correct

### AI-Assisted Troubleshooting
```bash
# Get help with specific issues
kubectl-ai "show me logs from backend pods in the last 10 minutes"
kubectl-ai "check if frontend can connect to backend service"
kagent "analyze why pods are consuming too much memory"
```

## Scaling the Application

### Horizontal Pod Autoscaler
The deployment includes HPA configurations. To test scaling:

```bash
# Generate load to trigger scaling
kubectl-ai "generate command to create load on backend service"

# Monitor scaling events
kubectl get hpa -n todo-chatbot
kubectl get pods -n todo-chatbot  # Observe new pods being created
```

## Cleanup

To remove the Todo Chatbot deployment:

```bash
helm uninstall todo-chatbot -n todo-chatbot
helm uninstall postgres -n todo-chatbot
kubectl delete secret postgres-credentials openai-credentials -n todo-chatbot
minikube stop
```

## Next Steps

1. Explore the API documentation at `http://todo-chatbot.local/api/docs`
2. Customize the Helm values for different environments
3. Set up monitoring and alerting
4. Implement CI/CD pipeline for automated deployments