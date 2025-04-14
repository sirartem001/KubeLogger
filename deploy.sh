#!/bin/bash
minikube start
minikube image build -t app -f docker/Dockerfile .

kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/daemonset.yaml
kubectl apply -f kubernetes/cronjob.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=logging-app --timeout=60s

echo "Testing service..."
kubectl port-forward svc/logging-service 8080:80 & PORT_FORWARD_PID=$!
sleep 1
kubectl create job --from=cronjob/log-archiver manual-archiver-$(date +%s)
echo "Port-forward запущен на 8080, PID: $PORT_FORWARD_PID"
curl http://localhost:8080/
curl http://localhost:8080/status
curl -X POST http://localhost:8080/log -H "Content-Type: application/json" -d '{"message": "test"}'
curl http://localhost:8080/logs

echo "Deployment completed!"