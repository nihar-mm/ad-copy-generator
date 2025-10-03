# Ad Copy Regenerator

A production-ready AI-powered ad copy generation system that analyzes images and generates diverse, platform-optimized ad copy variants.

## 🚀 Features

### Core Pipeline
- **Image Upload & Storage**: Local file storage with job queuing
- **Preflight Checks**: Size/DPI validation, contrast analysis, background complexity detection
- **OCR Ensemble**: Tesseract + EasyOCR with confidence-based fusion
- **Smart Zoning**: Automatic classification of Headline/Subhead/CTA/Legal/Price areas
- **Semantic Extraction**: Intent, tone, and entity analysis
- **AI Generation**: 8 strategic angles with LLM-powered copy creation
- **Validation**: Readability scoring, policy compliance, CTA verification
- **Placement Simulation**: Safe-area fitting with overlay previews

### Production Features
- **Rate Limiting**: Configurable per-minute limits on job creation
- **Enhanced LLM Integration**: OpenAI + Groq with fallbacks and retries
- **Admin Panel**: Real-time policy management (character caps, banned words, risk modes)
- **Comprehensive Logging**: Request tracking and error monitoring
- **CORS & Security**: Production-ready middleware stack

### Brand Voice & Diversity
- **Voice Similarity**: Embedding-based brand voice matching
- **De-duplication**: Cosine similarity filtering for variant diversity
- **Locale Support**: Indian English (EN-IN) and Hindi (HI-IN) with cultural context

## 🛠️ Tech Stack

- **Backend**: FastAPI + SQLite + Inline Processing
- **Storage**: Local file system (configurable to S3/MinIO)
- **AI/ML**: OpenAI GPT-4, Groq Llama-3, Tesseract, EasyOCR
- **Frontend**: React + Tailwind CSS + Vite
- **Infrastructure**: Local development setup
- **Monitoring**: Sentry integration ready

## 📋 Prerequisites

- **Python 3.11+** (recommended)
- **Node.js 18+** and npm
- **Tesseract OCR** installed locally:
  - **Windows**: `winget install UB-Mannheim.TesseractOCR`
  - **macOS**: `brew install tesseract`
  - **Ubuntu/Debian**: `sudo apt install tesseract-ocr`
- **OpenAI API key** (optional, for GPT-4)
- **Groq API key** (optional, for Llama-3)
- **Local LLM endpoint** (optional, for offline processing)

## 🚀 Local Development

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ad-copy-regenerator
```

### 2. Backend Setup

```bash
cd server

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env
# Edit .env with your API keys and configuration
```

### 3. Frontend Setup

```bash
cd web

# Install dependencies
npm ci

# Copy environment file (optional)
cp .env.local.example .env.local
# Edit .env.local if you need custom API configuration
```

### 4. Start Services

**Option A: Using provided scripts**

```bash
# Backend (in server directory)
# On Windows:
run_local.bat
# On macOS/Linux:
./run_local.sh

# Frontend (in web directory, new terminal)
npm run dev
```

**Option B: Manual startup**

```bash
# Backend (in server directory)
uvicorn app.main:app --reload --port 8000

# Frontend (in web directory, new terminal)
npm run dev
```

### 5. Access the System

- **Main UI**: http://localhost:5173
- **Admin Panel**: Click "Admin Panel" button in the header
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health/

## 🧪 Testing

### Quick Test via UI

1. Open http://localhost:5173
2. Upload an image (PNG/JPG, max 10MB)
3. Fill in brand voice, product details, and preferences
4. Submit and watch the pipeline process
5. View generated variants with overlay previews

### API Testing

```bash
# Create a job
curl -F "image=@sample_ad_clean.png" \
     -F "brand_voice=playful, no_exclaim" \
     -F "product_name=Couples Card Deck" \
     -F "must_include=warming gel,couples" \
     -F "persona=Couples 20-30" \
     -F "platform=Meta" \
     -F "locales=en-IN" \
     -F "risk_mode=standard" \
     -F "n_variants=8" \
     http://localhost:8000/api/jobs/create

# Check job status
curl http://localhost:8000/api/jobs/<JOB_ID>
```

### Admin Panel Testing

1. Navigate to Admin Panel
2. Adjust character limits for different content types
3. Update banned words/phrases
4. Modify must-include requirements
5. Switch between risk modes (lenient/standard/strict)

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```bash
# App Configuration
APP_ENV=dev
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO

# Database (SQLite by default)
DATABASE_URL=sqlite:///./dev.db

# Storage (Local by default)
STORAGE_BACKEND=local
LOCAL_STORAGE_DIR=./_data

# Queue (Inline by default, no Redis required)
QUEUE_MODE=inline

# LLM Configuration
LLM_PROVIDER=groq
OPENAI_API_KEY=your-openai-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

**Frontend (.env.local)**
```bash
VITE_API_BASE=http://localhost:8000/api
```

### Character Caps
- **Headline**: 60 characters (default)
- **Subhead**: 120 characters (default)
- **CTA**: 20 characters (default)
- **Legal**: 200 characters (default)

### Risk Modes
- **Lenient**: Minimal filtering, creative freedom
- **Standard**: Balanced approach (default)
- **Strict**: Maximum compliance, conservative output

### Locale Rules
- **en-IN**: Indian English with INR currency
- **hi-IN**: Hindi with cultural context

## 📊 API Endpoints

### Jobs
- `POST /api/jobs/create` - Create new generation job
- `GET /api/jobs/{job_id}` - Get job status and results

### Admin
- `GET /api/admin/settings` - Get current settings
- `PUT /api/admin/settings/character-caps` - Update character limits
- `PUT /api/admin/settings/banned-words` - Update banned words
- `PUT /api/admin/settings/must-include` - Update required words
- `PUT /api/admin/settings/risk-mode` - Update risk mode
- `GET /api/admin/stats` - Get system statistics

### Health
- `GET /api/health` - System health check

## 🔒 Production Deployment

### Security Considerations
- Set `APP_ENV=prod` in production
- Configure proper `SECRET_KEY`
- Set up trusted hosts for your domain
- Enable HTTPS with proper CORS origins
- Implement authentication (JWT/OAuth)

### Environment Variables
```bash
APP_ENV=prod
SECRET_KEY=<strong-secret-key>
CORS_ORIGINS=https://yourdomain.com
SENTRY_DSN=<your-sentry-dsn>
```

### Scaling
- Use external PostgreSQL and Redis instances
- Implement load balancing for the API
- Set up monitoring and alerting
- Configure backup strategies

## 🚨 Troubleshooting

### Common Issues

**Tesseract OCR Not Found**
- Ensure Tesseract is installed and in PATH
- On Windows, add Tesseract to system PATH
- Test with: `tesseract --version`

**LLM API Errors**
- Check API keys in `.env`
- Verify rate limits and quotas
- Check network connectivity

**Image Processing Failures**
- Ensure images are PNG/JPG format
- Check file size (max 10MB)
- Verify local storage directory permissions

**Database Connection Issues**
- Check SQLite file permissions
- Verify connection string in `.env`
- Ensure server directory is writable

### Logs
```bash
# View API logs (in terminal where uvicorn is running)
# Check console output for errors

# For production, configure proper logging
LOG_LEVEL=DEBUG
```

## 🔮 Roadmap

### Phase 2 (Next)
- [ ] Brand voice similarity scoring
- [ ] Variant de-duplication
- [ ] Enhanced policy rules
- [ ] WCAG contrast validation

### Phase 3 (Future)
- [ ] Multi-language support expansion
- [ ] Advanced analytics dashboard
- [ ] A/B testing integration
- [ ] Custom model fine-tuning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
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

**Built for MyMuse Ad Studio** - Transforming ad creation with AI-powered copy generation.