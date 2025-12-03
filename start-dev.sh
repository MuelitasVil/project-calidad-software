#!/bin/bash
# Complete workflow script for starting services with data restoration

set -e

echo "🚀 Starting development environment..."
echo ""

# Check if docker compose is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

# Start services
echo "1️⃣ Starting services..."
make up

# Wait for services to be ready
echo ""
echo "2️⃣ Waiting for services to be ready..."
sleep 10

# Check if backup exists
if [ -d "/tmp/dynamodb-backup" ] && [ -f "/tmp/dynamodb-backup/auth_ms_usuario.json" ]; then
    echo ""
    echo "3️⃣ Found existing backup, restoring data..."
    make restore-db
else
    echo ""
    echo "3️⃣ No backup found, creating admin user..."
    make seed-admin
    
    echo ""
    echo "💾 Creating initial backup..."
    make backup-db
fi

echo ""
echo "✅ Development environment is ready!"
echo ""
echo "📝 URLs disponibles:"
echo "   - Frontend:     http://localhost:3000"
echo "   - Auth Service: http://localhost:8000/docs"
echo "   - Users Service: http://localhost:8001/docs"
echo ""
echo "🔐 Admin credentials:"
echo "   Email:    mhoyos@example.com"
echo "   Password: qwerty123"
echo ""
echo "⚠️  Remember to run 'make backup-db' before stopping services!"
