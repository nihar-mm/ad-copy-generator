# 🍎 Ad Copy Regenerator - Mac Setup Guide

A production-ready AI-powered ad copy generation system specifically designed for MyMuse's intimate wellness products.

## 🚀 Quick Start (Mac)

### Option 1: Automated Setup
```bash
# Run the automated setup script
./setup_mac.sh
```

### Option 2: Manual Setup

#### 1. Install Prerequisites
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install python@3.11 node@18 tesseract libjpeg libpng libtiff
```

#### 2. Backend Setup
```bash
cd server

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
cp env.example .env
# Edit .env with your API keys

# Initialize database
python init_db.py
```

#### 3. Frontend Setup
```bash
cd ../web
npm install
```

#### 4. Run the Application
```bash
# Terminal 1 (Backend)
cd server
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2 (Frontend)
cd web
npm run dev
```

## 🔧 Configuration

### Required API Keys
Edit `server/.env` and add your API keys:

```bash
# At least one of these is required
GROQ_API_KEY=your-groq-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

### Get API Keys
- **Groq**: https://console.groq.com/keys (Free tier available)
- **OpenAI**: https://platform.openai.com/api-keys

## 🧪 Testing

```bash
# Test the complete system
python test_system.py

# Test individual components
cd server
source .venv/bin/activate
python -c "from app.config import settings; print('✅ Config loaded')"
```

## 📱 Access Points

- **Main UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health/
- **Admin Panel**: Click "Admin Panel" in the main UI

## 🎯 Features

### Core Pipeline
- **Image Upload & Storage**: Local file storage with job queuing
- **OCR Ensemble**: Tesseract + EasyOCR with confidence-based fusion
- **Smart Zoning**: Automatic classification of Headline/Subhead/CTA/Legal/Price areas
- **AI Generation**: 8 strategic angles with LLM-powered copy creation
- **Brand Voice Validation**: MyMuse-specific tone and style validation
- **Placement Simulation**: Safe-area fitting with overlay previews

### MyMuse Brand Integration
- **Sensual, Playful, Empowering**: Brand voice tailored for intimate wellness
- **Category-Specific Tone**: Different approaches for vibrators, lubricants, massage oils, candles, games, accessories
- **Quality Validation**: Comprehensive brand voice scoring and validation
- **Cultural Context**: Indian English (EN-IN) and Hindi (HI-IN) support

## 🛠️ Troubleshooting

### Common Issues

**OCR Not Working**
```bash
# Check if Tesseract is installed
tesseract --version

# If not installed:
brew install tesseract
```

**Python Dependencies Missing**
```bash
cd server
source .venv/bin/activate
pip install -r requirements.txt
```

**Node.js Dependencies Missing**
```bash
cd web
npm install
```

**Database Issues**
```bash
cd server
source .venv/bin/activate
python init_db.py
```

**Port Already in Use**
```bash
# Kill processes on ports 8000 and 5173
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Logs and Debugging

**Backend Logs**
```bash
cd server
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000 --log-level debug
```

**Frontend Logs**
```bash
cd web
npm run dev -- --debug
```

## 🔒 Security Notes

- Never commit your `.env` file
- Use strong API keys
- The system includes rate limiting and input validation
- All file uploads are validated for type and size

## 📊 Performance

- **OCR Processing**: ~2-5 seconds per image
- **AI Generation**: ~3-10 seconds for 8 variants
- **Total Pipeline**: ~10-20 seconds end-to-end
- **Memory Usage**: ~200-500MB for typical workloads

## 🚀 Production Deployment

For production deployment:

1. Set `APP_ENV=prod` in `.env`
2. Use a production database (PostgreSQL)
3. Set up proper CORS origins
4. Configure monitoring and logging
5. Use a reverse proxy (nginx)
6. Set up SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

[Your License Here]

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Open an issue on GitHub
- Contact the development team

---

**Built for MyMuse Ad Studio** - Transforming ad creation with AI-powered copy generation. 🚀


