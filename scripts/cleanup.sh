#!/bin/bash

# Script to clean up the Todo Chatbot deployment

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting cleanup of Todo Chatbot deployment..."

# Uninstall the Helm release
helm uninstall todo-chatbot -n todo-chatbot || echo "Helm release not found, continuing..."

# Delete the namespace if it still exists
kubectl delete namespace todo-chatbot --ignore-not-found=true

# Stop Minikube
minikube stop

echo "Cleanup completed!"