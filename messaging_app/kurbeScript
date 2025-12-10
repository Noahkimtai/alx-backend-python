#!/bin/bash

echo "Starting Minikube..."
minikube start

if [ $? -ne 0 ]; then
    echo "Failed to start Minikube."
    exit 1
fi 

echo "Minikube started successfully."
kubectl cluster-info

echo "Retrieving list of pods in the default namespace.."

kubectl get pods