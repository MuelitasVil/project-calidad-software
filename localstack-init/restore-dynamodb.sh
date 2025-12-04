#!/bin/bash
# Script to restore DynamoDB tables from JSON backup files

echo "🔄 Starting DynamoDB restore..."

BACKUP_DIR="/tmp/dynamodb-backup"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found: $BACKUP_DIR"
    echo "Please run backup-dynamodb.sh first"
    exit 1
fi

# AWS CLI configuration for LocalStack
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

TABLES=("auth_ms_usuario" "auth_ms_jwt" "auth_ms_type_user")

for TABLE in "${TABLES[@]}"; do
    BACKUP_FILE="$BACKUP_DIR/$TABLE.json"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "⚠️  Backup file not found: $BACKUP_FILE, skipping..."
        continue
    fi
    
    echo "📦 Restoring table: $TABLE"
    
    # Check if table exists
    if ! aws dynamodb describe-table \
        --table-name "$TABLE" \
        --endpoint-url http://localhost:4566 \
        --region us-east-1 \
        --no-cli-pager >/dev/null 2>&1; then
        echo "⚠️  Table $TABLE does not exist. Please create tables first with init-dynamodb-tables.sh"
        continue
    fi
    
    # Get items from backup
    ITEM_COUNT=$(jq '.Count' "$BACKUP_FILE")
    
    if [ "$ITEM_COUNT" -eq 0 ]; then
        echo "⚠️  No items to restore in $TABLE"
        continue
    fi
    
    # Restore each item
    ITEMS=$(jq -c '.Items[]' "$BACKUP_FILE")
    RESTORED=0
    
    while IFS= read -r item; do
        if [ -n "$item" ]; then
            aws dynamodb put-item \
                --table-name "$TABLE" \
                --item "$item" \
                --endpoint-url http://localhost:4566 \
                --region us-east-1 \
                --no-cli-pager >/dev/null 2>&1
            
            ((RESTORED++))
        fi
    done <<< "$ITEMS"
    
    ITEM_COUNT=$RESTORED
    
    echo "✅ Restored $ITEM_COUNT items to $TABLE"
done

echo ""
echo "✅ Restore completed successfully!"
echo ""
echo "Verification:"
for TABLE in "${TABLES[@]}"; do
    COUNT=$(aws dynamodb scan \
        --table-name "$TABLE" \
        --select COUNT \
        --endpoint-url http://localhost:4566 \
        --region us-east-1 \
        --no-cli-pager | jq '.Count')
    echo "  $TABLE: $COUNT items"
done
