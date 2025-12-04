#!/bin/bash
# Script to backup DynamoDB tables to JSON files

set -e

echo "🔄 Starting DynamoDB backup..."

BACKUP_DIR="/tmp/dynamodb-backup"
mkdir -p "$BACKUP_DIR"

# AWS CLI configuration for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

TABLES=("auth_ms_usuario" "auth_ms_jwt" "auth_ms_type_user")

for TABLE in "${TABLES[@]}"; do
    echo "📦 Backing up table: $TABLE"
    
    # Check if table exists
    if aws dynamodb describe-table \
        --table-name "$TABLE" \
        --endpoint-url http://localhost:4566 \
        --region us-east-1 \
        --no-cli-pager >/dev/null 2>&1; then
        
        # Scan and save all items
        aws dynamodb scan \
            --table-name "$TABLE" \
            --endpoint-url http://localhost:4566 \
            --region us-east-1 \
            --no-cli-pager \
            > "$BACKUP_DIR/$TABLE.json"
        
        # Count items
        ITEM_COUNT=$(jq '.Count' "$BACKUP_DIR/$TABLE.json")
        echo "✅ Backed up $ITEM_COUNT items from $TABLE"
    else
        echo "⚠️  Table $TABLE does not exist, skipping..."
    fi
done

echo ""
echo "✅ Backup completed successfully!"
echo "📁 Backup location: $BACKUP_DIR"
echo ""
echo "Files created:"
ls -lh "$BACKUP_DIR"
