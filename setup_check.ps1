# Setup and Verification Script for Mechanic Diagnostic Assistant
# Run this after installing dependencies to verify everything is working

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Mechanic Diagnostic Assistant" -ForegroundColor Cyan
Write-Host "  Setup & Verification Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/8] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Check if venv exists
Write-Host "`n[2/8] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\activate") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found. Creating..." -ForegroundColor Red
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Check .env file
Write-Host "`n[3/8] Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
    
    # Check for required keys
    $envContent = Get-Content .env -Raw
    $missingKeys = @()
    
    if ($envContent -notmatch "OPENROUTER_API_KEY=\w+") { $missingKeys += "OPENROUTER_API_KEY"}
    if ($envContent -notmatch "OPENAI_API_KEY=\w+") { $missingKeys += "OPENAI_API_KEY" }
    if ($envContent -notmatch "LANGCHAIN_API_KEY=\w+") { $missingKeys += "LANGCHAIN_API_KEY" }
    
    if ($missingKeys.Count -gt 0) {
        Write-Host "⚠ Missing API keys: $($missingKeys -join ', ')" -ForegroundColor Yellow
        Write-Host "Please edit .env and add your API keys" -ForegroundColor Yellow
    } else {
        Write-Host "✓ All API keys configured" -ForegroundColor Green
    }
} else {
    Write-Host "✗ .env file not found. Copying from .env.example..." -ForegroundColor Red
    Copy-Item .env.example .env
    Write-Host "✓ .env created. Please edit it and add your API keys!" -ForegroundColor Yellow
}

# Check data files
Write-Host "`n[4/8] Checking knowledge base files..." -ForegroundColor Yellow
$dataFiles = @(
    "data\knowledge_base\obd_codes.json",
    "data\knowledge_base\common_symptoms.json",
    "data\knowledge_base\repair_guides.txt",
    "data\mock_data\parts_catalog.json",
    "data\mock_data\labor_rates.json"
)

$allDataPresent = $true
foreach ($file in $dataFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allDataPresent = $false
    }
}

if ($allDataPresent) {
    Write-Host "✓ All knowledge base files present" -ForegroundColor Green
} else {
    Write-Host "✗ Some data files are missing!" -ForegroundColor Red
}

# Check source files
Write-Host "`n[5/8] Checking source code structure..." -ForegroundColor Yellow
$srcDirs = @("src\agent", "src\rag", "src\tools_impl", "src\monitoring", "src\utils")
$allSrcPresent = $true

foreach ($dir in $srcDirs) {
    if (Test-Path $dir) {
        $fileCount = (Get-ChildItem $dir -Filter "*.py" | Measure-Object).Count
        Write-Host "  ✓ $dir ($fileCount files)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $dir MISSING" -ForegroundColor Red
        $allSrcPresent = $false
    }
}

# Test imports (requires venv activated)
Write-Host "`n[6/8] Testing Python imports..." -ForegroundColor Yellow
Write-Host "Note: Make sure you've activated the venv and installed requirements!" -ForegroundColor Cyan

$testScript = @"
import sys
try:
    from src.utils.config import get_config_summary
    from src.agent.tools import get_all_tools
    print('✓ Imports successful')
    
    tools = get_all_tools()
    print(f'✓ {len(tools)} tools loaded')
except Exception as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"@

$testScript | python 2>&1

# Check documentation
Write-Host "`n[7/8] Checking documentation..." -ForegroundColor Yellow
$docs = @("README.md", "TECHNICAL_DOC.md", "PROJECT_SUMMARY.md")
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        $size = (Get-Item $doc).Length
        Write-Host "  ✓ $doc ($([math]::Round($size/1KB, 1)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $doc MISSING" -ForegroundColor Red
    }
}

# Summary
Write-Host "`n[8/8] Setup Summary" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path ".env") {
    Write-Host "📝 Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Activate virtual environment:" -ForegroundColor White
    Write-Host "   venv\Scripts\activate" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Install dependencies (if not done):" -ForegroundColor White
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Configure your API keys in .env file" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Run the application:" -ForegroundColor White
    Write-Host "   python app.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "5. Open browser to http://localhost:7860" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "⚠ Please create .env file first!" -ForegroundColor Yellow
}

Write-Host "================================" -ForegroundColor Cyan
Write-Host "For more info, see PROJECT_SUMMARY.md" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
