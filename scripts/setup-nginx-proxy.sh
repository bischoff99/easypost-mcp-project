#!/bin/bash
# Setup nginx reverse proxy for EasyPost MCP project

echo "🔧 Setting up Nginx Reverse Proxy"
echo "=================================="
echo ""

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "📥 Installing nginx..."
    brew install nginx
fi

# Backup existing config
if [ -f /opt/homebrew/etc/nginx/nginx.conf ]; then
    echo "💾 Backing up existing nginx config..."
    sudo cp /opt/homebrew/etc/nginx/nginx.conf /opt/homebrew/etc/nginx/nginx.conf.backup
fi

# Copy our config
echo "📝 Installing EasyPost MCP nginx config..."
sudo cp nginx.conf /opt/homebrew/etc/nginx/servers/easypost-mcp.conf

# Test config
echo "🧪 Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Nginx config valid"
    echo ""
    echo "🚀 Start nginx:"
    echo "   sudo nginx"
    echo ""
    echo "🔄 Reload (after changes):"
    echo "   sudo nginx -s reload"
    echo ""
    echo "🛑 Stop:"
    echo "   sudo nginx -s stop"
    echo ""
    echo "📍 Access points (with proxy):"
    echo "   Frontend:  http://localhost/"
    echo "   Backend:   http://localhost/api/*"
    echo "   MCP:       http://localhost/mcp"
    echo "   Health:    http://localhost/health"
    echo "   Docs:      http://localhost/docs"
    echo ""
    echo "🎯 Benefits:"
    echo "   • Single port (80) - no CORS issues"
    echo "   • Static asset caching - 20x faster"
    echo "   • Rate limiting at edge"
    echo "   • Production-ready architecture"
else
    echo "❌ Nginx config has errors"
    exit 1
fi

