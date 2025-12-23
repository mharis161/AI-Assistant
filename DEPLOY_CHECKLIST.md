# 🚀 Hugging Face Deployment Checklist

## Pre-Deployment Setup

### ✅ 1. Hugging Face Account
- [ ] Create account at https://huggingface.co/join
- [ ] Verify email address
- [ ] Set up username

### ✅ 2. API Keys
- [ ] Have OpenAI API key ready
- [ ] Verify API key has sufficient credits
- [ ] (Optional) Alternative LLM API key (DeepSeek, etc.)

### ✅ 3. Local Testing
- [ ] Frontend builds successfully (`cd frontend && npm run build`)
- [ ] Backend runs without errors (`python api.py`)
- [ ] Can upload and query documents
- [ ] All dependencies in requirements.txt

## Deployment Files Ready

### ✅ 4. Core Files
- [x] `Dockerfile` - Multi-stage build configuration
- [x] `app.py` - Hugging Face entry point
- [x] `README_HF.md` - Space documentation
- [x] `.dockerignore` - Exclude unnecessary files
- [x] `requirements.txt` - Python dependencies
- [x] `api.py` - Updated to serve static frontend

### ✅ 5. Frontend Files
- [x] `frontend/package.json` - Node dependencies
- [x] `frontend/vite.config.js` - Build configuration
- [x] `frontend/src/*` - Source files

### ✅ 6. Scripts
- [x] `build.sh` - Frontend build script
- [x] `deploy.sh` - Deployment automation

## Deployment Steps

### ✅ 7. Create Space
- [ ] Go to https://huggingface.co/spaces
- [ ] Click "Create new Space"
- [ ] Name: `ai-policy-assistant` (or custom)
- [ ] SDK: Select **Docker**
- [ ] License: MIT
- [ ] Visibility: Public or Private
- [ ] Click "Create Space"

### ✅ 8. Clone and Setup
```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
cd SPACE_NAME

# Copy all files from local project
# Option 1: Copy manually via file explorer
# Option 2: Use command line
cp -r /path/to/AIAssistant/* .

# Rename README
mv README_HF.md README.md
```

### ✅ 9. Configure Secrets
- [ ] Go to Space Settings
- [ ] Click "Repository secrets"
- [ ] Add `OPENAI_API_KEY` = `sk-your-key-here`
- [ ] (Optional) Add other API keys

### ✅ 10. Deploy
```bash
# Add and commit all files
git add .
git commit -m "Initial deployment"

# Push to Hugging Face
git push
```

### ✅ 11. Monitor Build
- [ ] Go to Space → Build tab
- [ ] Wait for Docker build (5-10 minutes)
- [ ] Check for build errors
- [ ] Verify both stages complete:
  - [ ] Frontend build (Node)
  - [ ] Backend build (Python)

## Post-Deployment

### ✅ 12. Verify Deployment
- [ ] Space shows "Running" status
- [ ] Open space URL
- [ ] Frontend loads correctly
- [ ] UI is responsive
- [ ] No console errors

### ✅ 13. Test Functionality
- [ ] API root endpoint responds
- [ ] Can upload PDF
- [ ] Document ingestion works
- [ ] Can query uploaded documents
- [ ] Responses show sources
- [ ] Confidence scores display
- [ ] Stats update correctly

### ✅ 14. Performance Check
- [ ] Response time acceptable (<5s)
- [ ] No memory errors
- [ ] No timeout errors
- [ ] Embedding generation works

### ✅ 15. Final Configuration
- [ ] Set Space visibility (Public/Private)
- [ ] Add Space description
- [ ] Add tags (AI, NLP, chatbot, etc.)
- [ ] Enable discussions (optional)
- [ ] Pin space (optional)

## Troubleshooting Common Issues

### Build Fails

**Frontend build error:**
- [ ] Check Node version in Dockerfile
- [ ] Verify package.json is correct
- [ ] Check build logs for npm errors

**Backend build error:**
- [ ] Check Python version
- [ ] Verify all imports in requirements.txt
- [ ] Check for missing dependencies

### Runtime Issues

**"OPENAI_API_KEY not found":**
- [ ] Verify secret is set correctly
- [ ] Restart the space
- [ ] Check secret name matches code

**Static files not serving:**
- [ ] Verify frontend/dist exists
- [ ] Check Dockerfile COPY command
- [ ] Rebuild the space

**Upload fails:**
- [ ] Check uploads/ directory permissions
- [ ] Verify file size limits
- [ ] Check disk space on hardware tier

## Optimization

### ✅ 16. Hardware Upgrade (Optional)
Current: CPU basic (free)

Recommended for production:
- [ ] CPU Upgrade (2 vCPU, 16GB RAM) - $0.60/hour
- [ ] Persistent storage for vector_db
- [ ] GPU for faster embeddings (optional)

### ✅ 17. Performance Tuning
- [ ] Adjust CHUNK_SIZE in config.py
- [ ] Tune TOP_K_RESULTS
- [ ] Enable embedding cache
- [ ] Optimize vector search

### ✅ 18. Monitoring Setup
- [ ] Enable Space analytics
- [ ] Monitor OpenAI API usage
- [ ] Set up usage alerts
- [ ] Track error rates

## Security

### ✅ 19. Security Checklist
- [ ] API keys in secrets only (never in code)
- [ ] Input validation enabled
- [ ] File upload restrictions
- [ ] Rate limiting (if needed)
- [ ] CORS configured correctly

## Documentation

### ✅ 20. User Documentation
- [ ] Usage instructions in README
- [ ] API endpoints documented
- [ ] Example queries provided
- [ ] Troubleshooting guide

## Success Criteria

### ✅ All Green?
- [ ] Space is running
- [ ] Frontend loads
- [ ] Can upload documents
- [ ] Can query documents
- [ ] Responses are accurate
- [ ] Sources displayed
- [ ] Performance acceptable
- [ ] No errors in logs

## 🎉 Deployment Complete!

Your AI Policy Assistant is now live on Hugging Face Spaces!

**Next Steps:**
1. Share the URL with your team
2. Upload your policy documents
3. Start querying!
4. Monitor usage and performance
5. Iterate and improve

**Your Space URL:**
```
https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
```

---

**Need Help?**
- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Discord: https://hf.co/join/discord
- Forum: https://discuss.huggingface.co/

**Deployment Guide:** See `DEPLOYMENT.md` for detailed instructions
