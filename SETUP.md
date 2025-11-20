# Setup Guide

Follow these steps to set up the Who Is Hiring In Tech application.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Git

## Backend Setup

### 1. Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

### 2. Create Database

```bash
createdb whit_db
```

### 3. Set Up Python Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and update the database credentials:
```
DATABASE_NAME=whit_db
DATABASE_USER=your_postgres_user
DATABASE_PASSWORD=your_postgres_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Import Company Data

```bash
python manage.py import_companies ../data/companies.csv
```

### 7. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 8. Start Backend Server

```bash
python manage.py runserver
```

Backend will be available at http://localhost:8000
Admin panel at http://localhost:8000/admin

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

The default configuration should work if the backend is running on localhost:8000.

### 3. Start Development Server

```bash
npm run dev
```

Frontend will be available at http://localhost:5173

## Access the Application

1. **Main Application:** http://localhost:5173
2. **Admin Dashboard:** http://localhost:8000/admin
3. **API Documentation:** http://localhost:8000/api/

## Common Issues

### Database Connection Error

If you get a database connection error:
1. Make sure PostgreSQL is running: `brew services list`
2. Check your database credentials in `backend/.env`
3. Verify the database exists: `psql -l`

### Port Already in Use

If port 8000 or 5173 is already in use:
- Backend: `python manage.py runserver 8001`
- Frontend: Edit `vite.config.js` to change the port

### Import Error

If the CSV import fails:
1. Check the CSV file path
2. Ensure the CSV file has the correct format
3. Check the logs for specific errors

## Next Steps

1. Import your company data
2. Customize the styling to match your brand
3. Add authentication if needed
4. Deploy to production

## Production Deployment

For production deployment:

1. Update `DEBUG=False` in backend `.env`
2. Set a secure `SECRET_KEY`
3. Configure proper database (not SQLite)
4. Set up proper CORS settings
5. Build frontend: `npm run build`
6. Serve static files with nginx or similar
7. Use gunicorn/uwsgi for Django
8. Set up HTTPS

Refer to Django and React deployment guides for detailed instructions.
