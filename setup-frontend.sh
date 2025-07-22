#!/bin/bash

echo "🚀 Setting up CB2 Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install additional dev dependencies if not present
echo "🔧 Installing development dependencies..."
npm install --save-dev @types/react @types/react-dom @types/node typescript

# Run type checking
echo "🔍 Running TypeScript type checking..."
npm run type-check

# Run linting
echo "🧹 Running linting..."
npm run lint

# Build the project
echo "🏗️ Building the project..."
npm run build

echo "✅ Frontend setup completed!"
echo ""
echo "To start the development server:"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "To run tests:"
echo "  npm test"
echo ""
echo "To build for production:"
echo "  npm run build"
