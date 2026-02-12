#!/bin/bash

# setup-minikube.sh - Sets up Minikube for Todo Chatbot deployment

echo "🚀 Setting up Minikube for Todo Chatbot..."

# Start Minikube with adequate resources
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=20g \
  --driver=docker \
  --kubernetes-version=stable

# Enable addons
echo "📦 Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Configure local Docker to use Minikube's daemon
echo "🐳 Configuring Docker environment..."
eval $(minikube docker-env)

# Add todo-chatbot.local to /etc/hosts
echo "📝 Configuring /etc/hosts..."
MINIKUBE_IP=$(minikube ip)
echo "$MINIKUBE_IP todo-chatbot.local" | sudo tee -a /etc/hosts

echo "✅ Minikube setup complete!"
echo "🌐 Access dashboard: minikube dashboard"
echo "🔗 Application will be available at: http://todo-chatbot.local"