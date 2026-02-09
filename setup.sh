#!/bin/bash
# Setup script for Campspots application

echo "Setting up Campspots reservation system..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Stripe API keys!"
    echo "   Get them from: https://dashboard.stripe.com/test/apikeys"
    echo ""
fi

# Initialize database
echo "Initializing database..."
python init_db.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Stripe keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the app: python app.py"
echo "4. Visit: http://localhost:5000"
echo ""
