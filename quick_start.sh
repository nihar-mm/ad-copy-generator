#!/bin/bash

# Quick Start Script - Minimal Setup
# This sets up the project with minimal dependencies

echo "🚀 Quick Start - Ad Copy Regenerator"
echo "===================================="

# Navigate to project directory
cd "$(dirname "$0")"

# Backend setup
echo "Setting up backend..."
cd server

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install minimal dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn python-multipart pydantic-settings python-dotenv

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit .env with your API keys"
fi

# Frontend setup
echo "Setting up frontend..."
cd ../web

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Create simple run scripts
echo "Creating run scripts..."

# Backend run script
cat > ../run_backend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/server"
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
EOF

# Frontend run script
cat > ../run_frontend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/web"
npm run dev
EOF

# Make scripts executable
chmod +x ../run_backend.sh
chmod +x ../run_frontend.sh

echo ""
echo "✅ Quick setup complete!"
echo ""
echo "To run:"
echo "  ./run_backend.sh    # Terminal 1"
echo "  ./run_frontend.sh   # Terminal 2"
echo ""
echo "⚠️  Note: Some features may not work without full dependencies"
echo "   Run ./setup_mac_no_sudo.sh for complete setup"

