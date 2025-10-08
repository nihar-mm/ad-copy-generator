#!/bin/bash

# Ad Copy Regenerator - Mac Setup Script
# This script sets up the complete environment on macOS

set -e  # Exit on any error

echo "🚀 Setting up Ad Copy Regenerator on macOS"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_status "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    print_success "Homebrew installed"
else
    print_success "Homebrew already installed"
fi

# Install system dependencies
print_status "Installing system dependencies..."
brew install python@3.11 node@18 tesseract libjpeg libpng libtiff
print_success "System dependencies installed"

# Navigate to project directory
cd "$(dirname "$0")"

# Backend setup
print_status "Setting up backend..."
cd server

# Create virtual environment
if [ ! -d ".venv" ]; then
    print_status "Creating Python virtual environment..."
    python3.11 -m venv .venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Python dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file..."
    cp env.example .env
    print_warning "Please edit .env file with your API keys"
    print_warning "Required: GROQ_API_KEY or OPENAI_API_KEY"
else
    print_success ".env file already exists"
fi

# Initialize database
print_status "Initializing database..."
python init_db.py
print_success "Database initialized"

# Frontend setup
print_status "Setting up frontend..."
cd ../web

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install
print_success "Node.js dependencies installed"

# Create run scripts
print_status "Creating run scripts..."

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

print_success "Run scripts created"

# Test system
print_status "Testing system..."
cd ../server
source .venv/bin/activate

# Test Python imports
python -c "
try:
    from fastapi import FastAPI
    from app.config import settings
    print('✅ Backend imports working')
except Exception as e:
    print(f'❌ Backend import error: {e}')
    exit(1)
"

print_success "Backend test passed"

cd ../web
# Test Node.js
if npm run build --silent > /dev/null 2>&1; then
    print_success "Frontend build test passed"
else
    print_warning "Frontend build test failed, but continuing..."
fi

# Final instructions
echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  ./run_backend.sh"
echo ""
echo "Terminal 2 (Frontend):"
echo "  ./run_frontend.sh"
echo ""
echo "Access points:"
echo "  Main UI: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
echo "  Health Check: http://localhost:8000/api/health/"
echo ""
echo "⚠️  Don't forget to:"
echo "  1. Edit server/.env with your API keys"
echo "  2. Install Tesseract OCR: brew install tesseract"
echo "  3. Test with: python test_system.py"
echo ""
print_success "Setup complete! 🚀"


