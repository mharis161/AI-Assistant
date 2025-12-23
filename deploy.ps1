# PowerShell Deployment Script for Hugging Face Spaces
param(
    [Parameter(Mandatory=$true)]
    [string]$HF_USERNAME,
    
    [Parameter(Mandatory=$false)]
    [string]$SPACE_NAME = "ai-policy-assistant"
)

Write-Host "🚀 Hugging Face Spaces Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$SPACE_URL = "https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
Write-Host "📦 Deploying to: $SPACE_URL" -ForegroundColor Green
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "⚙️  Initializing git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit"
}

# Add Hugging Face remote
Write-Host "🔗 Adding Hugging Face remote..." -ForegroundColor Yellow
git remote remove huggingface 2>$null
git remote add huggingface "https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

# Backup and prepare README
if (Test-Path "README_HF.md") {
    Write-Host "📝 Preparing README..." -ForegroundColor Yellow
    if (Test-Path "README.md") {
        Copy-Item "README.md" "README_LOCAL.md" -Force
    }
    Copy-Item "README_HF.md" "README.md" -Force
}

# Commit changes
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git add .
$commitResult = git commit -m "Deploy to Hugging Face Spaces" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "No changes to commit" -ForegroundColor Gray
}

# Push to Hugging Face
Write-Host "🚀 Pushing to Hugging Face Spaces..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  You may be prompted for Hugging Face credentials:" -ForegroundColor Yellow
Write-Host "   Username: $HF_USERNAME" -ForegroundColor White
Write-Host "   Password: Use your Hugging Face ACCESS TOKEN (not password)" -ForegroundColor White
Write-Host "   Get token at: https://huggingface.co/settings/tokens" -ForegroundColor Cyan
Write-Host ""

git push huggingface main -f

if ($LASTEXITCODE -eq 0) {
    # Restore local README
    if (Test-Path "README_LOCAL.md") {
        Move-Item "README_LOCAL.md" "README.md" -Force
    }

    Write-Host ""
    Write-Host "✅ Deployment complete!" -ForegroundColor Green
    Write-Host "🌐 Your app will be available at:" -ForegroundColor Cyan
    Write-Host "   $SPACE_URL" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️  Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Go to: $SPACE_URL/settings" -ForegroundColor White
    Write-Host "   2. Click 'Repository secrets'" -ForegroundColor White
    Write-Host "   3. Add: OPENAI_API_KEY = sk-your-key-here" -ForegroundColor White
    Write-Host "   4. Wait for Docker build (5-10 minutes)" -ForegroundColor White
    Write-Host "   5. Upload your policy documents" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Please check the error message above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "   - Invalid credentials (use access token, not password)" -ForegroundColor White
    Write-Host "   - Space doesn't exist yet - create it first at:" -ForegroundColor White
    Write-Host "     https://huggingface.co/new-space" -ForegroundColor Cyan
    Write-Host ""
    
    # Restore local README on failure
    if (Test-Path "README_LOCAL.md") {
        Move-Item "README_LOCAL.md" "README.md" -Force
    }
    
    exit 1
}
