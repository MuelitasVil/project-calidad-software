#!/bin/bash
# Complete workflow script for stopping services with data backup

set -e

echo "🛑 Stopping development environment..."
echo ""

# Backup data
echo "1️⃣ Backing up DynamoDB data..."
make backup-db

echo ""
echo "2️⃣ Stopping services..."
make down

echo ""
echo "✅ Services stopped successfully!"
echo "💾 Data backed up to: /tmp/dynamodb-backup/"
echo ""
echo "💡 To start again with restored data: ./start-dev.sh"
