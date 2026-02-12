#!/bin/bash

# Script to set up Minikube and deploy the Todo Chatbot application

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Minikube setup for Todo Chatbot..."

# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

echo "Minikube is ready!"

# Set Docker environment to use Minikube's container registry
eval $(minikube docker-env)

echo "Building Docker images..."

# Build backend image
cd ../backend
docker build -t todo-backend:latest -f ../docker/backend/Dockerfile .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest -f ../docker/frontend/Dockerfile .

echo "Docker images built successfully!"

# Navigate to Helm chart directory
cd ../helm/todo-chatbot

echo "Installing Todo Chatbot via Helm..."

# Install the Helm chart
helm install todo-chatbot . --namespace todo-chatbot --create-namespace --values values.yaml

echo "Deployment completed! You can access the application using 'minikube service todo-chatbot-frontend --namespace todo-chatbot'"