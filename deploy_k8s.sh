#!/usr/bin/env bash
set -euo pipefail

ACCOUNT_ID=${1:-123456789012}
REGION=${2:-us-east-1}
TAG=${3:-latest}

echo "🔧 Deploying to EKS with images from ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com, tag=${TAG}"

# Reemplazar placeholders en manifests y aplicar
for file in k8s/*.yaml; do
  echo "➡️  Applying $file"
  sed "s/{{ACCOUNT_ID}}/${ACCOUNT_ID}/g; s/{{REGION}}/${REGION}/g; s/{{TAG}}/${TAG}/g" "$file" | kubectl apply -f -
done

# Forzar que los deployments se actualicen con la nueva imagen
#kubectl rollout restart deployment auth-deployment
kubectl rollout restart deployment users-deployment

echo "✅ Deploy complete!"