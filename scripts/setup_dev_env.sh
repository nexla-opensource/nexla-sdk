#!/bin/bash
# Setup script for Nexla SDK development environment

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"

# Setup pre-commit hooks if pre-commit is installed
if command -v pre-commit &> /dev/null; then
    echo "Setting up pre-commit hooks..."
    pre-commit install
else
    echo "pre-commit not found. Skipping pre-commit setup."
    echo "To install pre-commit: pip install pre-commit"
fi

# Setup environment file
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp -n .env.example .env
    echo "Please update the .env file with your Nexla API credentials."
fi

echo "Development environment setup complete!"
echo "Activate the virtual environment with: source venv/bin/activate" 