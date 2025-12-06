#!/bin/bash
# Script to seed the admin user if it doesn't exist

set -e

echo "🌱 Seeding admin user..."

# Wait for auth service to be ready
echo "⏳ Waiting for auth service..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1 || \
       curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo "✅ Auth service is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Auth service not responding after 30 seconds"
        exit 1
    fi
    sleep 1
done

# Admin credentials
ADMIN_EMAIL="mhoyos@example.com"
ADMIN_PASSWORD="qwerty123"

# Check if admin already exists by trying to register
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:8000/auth/register" \
    -H "Content-Type: application/json" \
    -d "{
        \"e_mail\": \"$ADMIN_EMAIL\",
        \"password\": \"$ADMIN_PASSWORD\",
        \"type_user\": \"admin\"
    }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Admin user created: $ADMIN_EMAIL"
    echo "   Password: $ADMIN_PASSWORD"
elif [ "$HTTP_CODE" = "400" ]; then
    if echo "$BODY" | grep -q "Admin user already exists"; then
        echo "✅ Admin user already exists: $ADMIN_EMAIL"
    elif echo "$BODY" | grep -q "User already exists"; then
        echo "✅ Admin user already exists: $ADMIN_EMAIL"
    else
        echo "⚠️  Registration failed: $BODY"
    fi
else
    echo "⚠️  Unexpected response (HTTP $HTTP_CODE): $BODY"
fi

echo ""
echo "🔐 Admin credentials:"
echo "   Email: $ADMIN_EMAIL"
echo "   Password: $ADMIN_PASSWORD"
