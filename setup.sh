#!/bin/bash

# ADGM Corporate Agent Pro - Setup Script
# Author: Shreyas
# Description: Automated setup script for easy installation

echo "🏢 ADGM Corporate Agent Pro - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.9" | bc -l) -eq 1 ]]; then
    echo "✅ Python $python_version detected (compatible)"
else
    echo "❌ Python 3.9+ required. Current version: $python_version"
    exit 1
fi

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
python -m venv venv
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment created successfully"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo ""
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create launcher script
echo ""
echo "📝 Creating launcher script..."
cat > launch.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting ADGM Corporate Agent Pro..."
source venv/bin/activate
streamlit run app.py --server.port 8501
EOF

chmod +x launch.sh

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "  ./launch.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "📱 The application will be available at: http://localhost:8501"
echo ""
