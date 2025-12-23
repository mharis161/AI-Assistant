# Hugging Face Spaces Deployment Guide

## 🚀 Quick Deploy to Hugging Face Spaces

### Prerequisites
- Hugging Face account ([sign up here](https://huggingface.co/join))
- OpenAI API key

### Step-by-Step Deployment

#### 1. Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in:
   - **Space name**: `ai-policy-assistant` (or your preferred name)
   - **License**: MIT
   - **Select SDK**: Docker
   - **Space hardware**: CPU basic (free) or upgrade for better performance

#### 2. Clone Your Space Repository

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-policy-assistant
cd ai-policy-assistant
```

#### 3. Copy Project Files

Copy these files from your local project to the cloned space:

```bash
# Core application files
cp -r d:/Antigravityworkspace/AIAssistant/* ./

# Or manually copy:
# - All Python files (*.py)
# - frontend/ directory
# - Dockerfile
# - requirements.txt
# - README_HF.md (rename to README.md)
```

#### 4. Rename README

```bash
mv README_HF.md README.md
```

#### 5. Set Environment Variables (Secrets)

1. Go to your Space settings on Hugging Face
2. Click "Settings" → "Repository secrets"
3. Add the following secret:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (sk-...)

#### 6. Commit and Push

```bash
git add .
git commit -m "Initial deployment"
git push
```

#### 7. Wait for Build

- Hugging Face will automatically build your Docker container
- This may take 5-10 minutes
- Monitor progress in the "Build" tab

#### 8. Access Your App

Once built, your app will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/ai-policy-assistant
```

## 🔧 Configuration Options

### Environment Variables

Set these in Space Settings → Repository secrets:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `DEEPSEEK_API_KEY` | No | Alternative LLM API key |
| `DEEPSEEK_BASE_URL` | No | Alternative LLM endpoint |

### Hardware Requirements

**Recommended for production:**
- **CPU**: Upgrade to CPU Upgrade (2 vCPU) for better performance
- **Memory**: 16GB recommended for large document processing
- **Storage**: Persistent storage for vector_db (optional)

## 📊 Post-Deployment

### Upload Documents

1. Open your deployed app
2. Click "Select PDF Document"
3. Upload your policy documents
4. Wait for ingestion (progress shown in UI)
5. Start asking questions!

### Monitor Usage

- Check Space analytics in Settings → Analytics
- Monitor API costs in OpenAI dashboard
- View logs in Space Settings → Logs

## 🐛 Troubleshooting

### Build Fails

**Issue**: Docker build fails
- Check Dockerfile syntax
- Ensure all dependencies in requirements.txt
- Check build logs for specific errors

**Issue**: Frontend build fails
- Verify package.json is correct
- Check Node.js version compatibility
- Review frontend build logs

### Runtime Issues

**Issue**: "No module named 'fastapi'"
- Ensure requirements.txt is complete
- Rebuild the space

**Issue**: "OPENAI_API_KEY not found"
- Verify secret is set correctly
- Restart the space

**Issue**: Vector DB not persisting
- Consider upgrading to persistent storage
- Or accept that DB rebuilds on restart

### Performance Issues

**Issue**: Slow responses
- Upgrade to better CPU
- Optimize chunk size in config.py
- Use caching for embeddings

**Issue**: Out of memory
- Upgrade to higher memory tier
- Reduce TOP_K_RESULTS in config.py
- Process fewer documents at once

## 🔄 Updates and Maintenance

### Update Code

```bash
# Make changes locally
git add .
git commit -m "Update: description"
git push
```

Space will automatically rebuild.

### Update Dependencies

1. Modify `requirements.txt` or `frontend/package.json`
2. Commit and push
3. Space rebuilds with new dependencies

### Rollback

```bash
git revert HEAD
git push
```

## 📈 Scaling Considerations

### For High Traffic

1. **Upgrade Hardware**: Use GPU for faster embeddings
2. **Add Caching**: Implement Redis for embedding cache
3. **Load Balancing**: Deploy multiple spaces behind a proxy
4. **Database**: Use managed ChromaDB or Pinecone

### Cost Optimization

1. **Use Local Embeddings**: Switch to sentence-transformers
2. **Batch Processing**: Process documents in batches
3. **Cache Results**: Store frequent query results
4. **Monitor API Usage**: Set OpenAI usage limits

## 🔐 Security Best Practices

1. **Never commit API keys** - Always use secrets
2. **Validate uploads** - Check file types and sizes
3. **Rate limiting** - Implement request throttling
4. **User authentication** - Add auth for production use
5. **HTTPS only** - Hugging Face provides this by default

## 📞 Support

- Hugging Face Spaces docs: https://huggingface.co/docs/hub/spaces
- Issues: Report on your space's discussion tab
- OpenAI docs: https://platform.openai.com/docs

## 🎉 Success!

Your AI Policy Assistant is now live and accessible to anyone with the URL!

Share it with your team and start querying your policy documents! 🚀
