# Who Is Hiring In Tech - Project Overview

## 🎯 Project Description

A full-stack web application that displays a comprehensive list of tech companies currently hiring. The application replicates your WordPress site with enhanced functionality, including an admin dashboard for data management.

## 🏗️ Architecture

### Backend (Django)
- **Framework:** Django 4.2 with Django REST Framework
- **Database:** PostgreSQL
- **Key Features:**
  - RESTful API with filtering, search, and pagination
  - Customized Django Admin panel
  - CSV data import command
  - CORS support for frontend integration

### Frontend (React)
- **Framework:** React 18 with Vite
- **Key Features:**
  - Modern, responsive UI
  - Advanced filtering system
  - Real-time search
  - Statistics dashboard
  - Company listing table with badges and tags

## 📁 Project Structure

```
whit/
├── backend/                    # Django Backend
│   ├── whit/                  # Project settings
│   │   ├── settings.py        # Django configuration
│   │   ├── urls.py            # Main URL routing
│   │   └── wsgi.py            # WSGI configuration
│   ├── companies/             # Companies app
│   │   ├── models.py          # Company, Function, WorkEnvironment models
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API viewsets
│   │   ├── admin.py           # Admin customization
│   │   ├── filters.py         # Django filters
│   │   ├── urls.py            # App URL routing
│   │   └── management/        # Custom commands
│   │       └── commands/
│   │           └── import_companies.py
│   ├── requirements.txt       # Python dependencies
│   ├── manage.py              # Django management script
│   └── .env.example           # Environment variables template
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Header.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── Filters.jsx
│   │   │   ├── Stats.jsx
│   │   │   └── CompanyTable.jsx
│   │   ├── pages/             # Page components
│   │   │   └── CompanyList.jsx
│   │   ├── services/          # API services
│   │   │   └── api.js
│   │   ├── App.jsx            # Main app component
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Global styles
│   ├── index.html             # HTML template
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── .env.example           # Environment variables template
│
├── data/                       # Data files
│   └── companies.csv          # Company data
│
├── README.md                  # Main documentation
├── SETUP.md                   # Setup instructions
├── setup.sh                   # Automated setup script
└── start.sh                   # Start both servers
```

## 🗄️ Database Schema

### Company Model
- `id` - Primary key
- `name` - Company name (unique)
- `logo` - URL to company logo
- `jobs_page_url` - URL to jobs page
- `company_reviews` - URL to company reviews
- `country` - Country location
- `state` - State/province (optional)
- `city` - City (optional)
- `work_environment` - Comma-separated (Remote, On-Site, Hybrid)
- `functions` - Comma-separated (Engineering, Sales, etc.)
- `engineering_positions` - Boolean flag
- `status` - Active/Inactive
- `created_at` - Timestamp
- `updated_at` - Timestamp

### Function Model
- `id` - Primary key
- `name` - Function/department name

### WorkEnvironment Model
- `id` - Primary key
- `name` - Work environment type

## 🔌 API Endpoints

### Companies
- `GET /api/companies/` - List all companies (with filters)
- `GET /api/companies/{id}/` - Get company details
- `POST /api/companies/` - Create company (admin)
- `PUT /api/companies/{id}/` - Update company (admin)
- `DELETE /api/companies/{id}/` - Delete company (admin)
- `GET /api/companies/filters/` - Get available filter options
- `GET /api/companies/stats/` - Get statistics

### Query Parameters for Filtering
- `search` - Search by name, city, or function
- `country` - Filter by country
- `state` - Filter by state
- `city` - Filter by city
- `functions` - Filter by function
- `work_environment` - Filter by work environment
- `engineering_positions` - Filter by engineering positions (true/false)
- `status` - Filter by status (Active/Inactive)
- `page` - Page number for pagination

## 🎨 UI Components

### Header
- Gradient background with title and subtitle
- Responsive design

### Stats Dashboard
- 4 stat cards showing:
  - Total companies
  - Active companies
  - Engineering positions
  - Countries count

### Search Bar
- Real-time search input
- Clear button
- Responsive layout

### Filters
- Dropdown filters for:
  - Status
  - Country
  - State
  - City
  - Function
  - Work Environment
  - Engineering Positions
- Reset all button

### Company Table
- Sortable columns
- Company logos
- Clickable links to jobs and reviews
- Function and work environment tags
- Location display
- Engineering positions badge
- Status badge
- Hover effects

## 🔐 Admin Dashboard

Access at `http://localhost:8000/admin`

**Features:**
- Full CRUD operations for companies
- Bulk actions (mark as active/inactive)
- Search and filter capabilities
- Custom fieldsets for better organization
- Company statistics

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
./setup.sh
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
createdb whit_db
python manage.py migrate
python manage.py import_companies ../data/companies.csv
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Start Both Servers
```bash
./start.sh
```

## 🌐 URLs

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/

## 📊 Data Management

### Import Companies
```bash
cd backend
python manage.py import_companies path/to/companies.csv
```

### CSV Format
The CSV should have the following columns:
- Company Name
- Logo
- Jobs Page URL
- Company Reviews
- Function
- Country
- State
- City
- WorkEnvironment
- EngineeringPositions
- Status

## 🎨 Customization

### Styling
- Modify CSS files in `frontend/src/components/*.css`
- Global styles in `frontend/src/index.css`
- Color scheme uses purple gradient (#667eea to #764ba2)

### Adding Features
- Backend: Add to `companies/views.py`
- Frontend: Create new components in `src/components/`

## 🔒 Security

For production deployment:
1. Set `DEBUG=False` in Django settings
2. Use a strong `SECRET_KEY`
3. Configure proper CORS settings
4. Use environment variables for sensitive data
5. Set up HTTPS
6. Use a production-grade database
7. Implement rate limiting
8. Add authentication for admin panel

## 📦 Dependencies

### Backend
- Django 4.2
- djangorestframework
- django-cors-headers
- psycopg2-binary
- python-decouple
- django-filter

### Frontend
- React 18
- react-router-dom
- axios
- vite

## 🐛 Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check credentials in `.env`
- Verify database exists

### Port Already in Use
- Change port in Django: `python manage.py runserver 8001`
- Change port in Vite: Edit `vite.config.js`

### CSV Import Fails
- Check CSV file format
- Ensure all required columns exist
- Check console for specific errors

## 📝 License

MIT

## 👨‍💻 Development

### Running Tests
```bash
cd backend
python manage.py test
```

### Code Quality
```bash
# Frontend
cd frontend
npm run lint
```

## 🚀 Deployment

### Backend (Django)
- Use Gunicorn/uWSGI
- Configure nginx as reverse proxy
- Use PostgreSQL in production
- Set up SSL certificates

### Frontend (React)
- Build: `npm run build`
- Serve `dist/` folder with nginx/Apache
- Configure proper routing

### Recommended Platforms
- **Backend:** Heroku, DigitalOcean, AWS
- **Frontend:** Vercel, Netlify, Cloudflare Pages
- **Database:** AWS RDS, DigitalOcean Managed Databases

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
