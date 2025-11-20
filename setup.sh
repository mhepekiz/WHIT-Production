#!/bin/bash

# Quick Start Script for Who Is Hiring In Tech

echo "🚀 Starting Who Is Hiring In Tech Setup..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed${NC}"
    echo "Install it with: brew install postgresql@14"
    exit 1
fi

echo -e "${GREEN}✓ PostgreSQL found${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js found${NC}"
echo ""

# Backend Setup
echo -e "${BLUE}📦 Setting up backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Create database if it doesn't exist
echo "Setting up database..."
psql -lqt | cut -d \| -f 1 | grep -qw whit_db
if [ $? -ne 0 ]; then
    createdb whit_db
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${GREEN}✓ Database already exists${NC}"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --no-input

# Import data
echo "Importing company data..."
if [ -f "../data/companies.csv" ]; then
    python manage.py import_companies ../data/companies.csv
else
    echo -e "${RED}⚠ CSV file not found. Skipping data import.${NC}"
fi

cd ..
echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Frontend Setup
echo -e "${BLUE}📦 Setting up frontend...${NC}"
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

cd ..
echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "To start the application:"
echo ""
echo -e "${BLUE}Terminal 1 (Backend):${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo -e "${BLUE}Terminal 2 (Frontend):${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
echo ""
echo "Admin panel: http://localhost:8000/admin"
echo "Create an admin user with: python manage.py createsuperuser"
