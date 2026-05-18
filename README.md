# Who Is Hiring In Tech

A full-stack web application for tracking tech companies that are currently hiring.

## Tech Stack

- **Backend:** Django 4.2 + Django REST Framework
- **Frontend:** React 18 + Vite
- **Database:** PostgreSQL
- **Styling:** CSS3 with modern design

## Features

- 📊 Company listings with comprehensive data
- 🔍 Advanced search and filtering
- 🎯 Filter by location, function, work environment
- 👨‍💼 Admin dashboard for data management
- 📱 Responsive design
- ⚡ Fast and efficient API

## Project Structure

```
whit/
├── backend/          # Django backend
│   ├── api/         # REST API app
│   ├── companies/   # Companies app
│   └── whit/        # Project settings
├── frontend/        # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── public/
└── data/           # CSV data files
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure PostgreSQL
createdb whit_db

# Run migrations
python manage.py migrate

# Import data
python manage.py import_companies ../data/companies.csv

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /api/companies/` - List all companies (with pagination, search, filters)
- `GET /api/companies/{id}/` - Get company details
- `POST /api/companies/` - Create company (admin only)
- `PUT /api/companies/{id}/` - Update company (admin only)
- `DELETE /api/companies/{id}/` - Delete company (admin only)
- `GET /api/companies/filters/` - Get available filter options

## Admin Access

Navigate to `http://localhost:8000/admin` to access the Django admin dashboard.

## Environment Variables

Create a `.env` file in the backend directory:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/whit_db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Production Deployment

For production deployment to a server, see:
- [SYSTEM_DOCUMENTATION.md](SYSTEM_DOCUMENTATION.md) - Practical operating guide for architecture, staging deploys, admin settings, and maintenance
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Troubleshooting guide for common issues

### Production Scripts

- `setup-gunicorn-logs.sh` - Setup Gunicorn logging directories
- `health-check.sh` - Verify Django application health before deployment
- `restart_production.sh` - Restart production services with health checks

## License

MIT
# Deployment test Mon Feb  9 19:16:56 CST 2026
# Permission fix test
# Final deployment test
