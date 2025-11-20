# Quick Reference Guide

## 🚀 Getting Started (5 minutes)

### 1. Run Automated Setup
```bash
cd /Users/mustafahepekiz/Desktop/whit
./setup.sh
```

### 2. Create Admin User
```bash
cd backend
source venv/bin/activate
python manage.py createsuperuser
```

### 3. Start Application
```bash
cd /Users/mustafahepekiz/Desktop/whit
./start.sh
```

### 4. Access the App
- **Main Site:** http://localhost:5173
- **Admin Panel:** http://localhost:8000/admin

---

## 📝 Common Commands

### Backend

**Activate virtual environment:**
```bash
cd backend
source venv/bin/activate
```

**Run migrations:**
```bash
python manage.py migrate
```

**Import CSV data:**
```bash
python manage.py import_companies ../data/companies.csv
```

**Start server:**
```bash
python manage.py runserver
```

**Create superuser:**
```bash
python manage.py createsuperuser
```

### Frontend

**Install dependencies:**
```bash
cd frontend
npm install
```

**Start development server:**
```bash
npm run dev
```

**Build for production:**
```bash
npm run build
```

---

## 🎯 Key Features

✅ **Company Listing** - Display all hiring companies
✅ **Advanced Filters** - Country, city, function, work environment
✅ **Search** - Real-time search by name, city, or function
✅ **Stats Dashboard** - Key metrics at a glance
✅ **Admin Panel** - Full CRUD operations
✅ **CSV Import** - Bulk data import from CSV
✅ **Responsive Design** - Works on all devices

---

## 📊 Admin Panel Features

1. **Add New Company** - Click "Add Company" button
2. **Edit Company** - Click on company name
3. **Delete Company** - Select and delete
4. **Bulk Actions** - Mark multiple as active/inactive
5. **Search** - Find companies quickly
6. **Filters** - Filter by status, country, etc.

---

## 🔧 Configuration

### Backend (.env)
```
DATABASE_NAME=whit_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

---

## 📁 Project Structure

```
whit/
├── backend/          # Django backend
│   ├── companies/    # Main app
│   ├── whit/        # Project settings
│   └── manage.py
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── data/            # CSV files
└── setup.sh         # Setup script
```

---

## 🐛 Troubleshooting

### Database Error
```bash
# Restart PostgreSQL
brew services restart postgresql@14

# Recreate database
dropdb whit_db
createdb whit_db
python manage.py migrate
```

### Port in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Module Not Found
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Documentation

- **Full Setup:** See `SETUP.md`
- **Project Details:** See `PROJECT_OVERVIEW.md`
- **Main README:** See `README.md`

---

## 🎨 Customization Tips

### Change Color Scheme
Edit CSS files in `frontend/src/components/*.css`

Current gradient: `#667eea` to `#764ba2`

### Add New Filter
1. Add field to model (`backend/companies/models.py`)
2. Update filter class (`backend/companies/filters.py`)
3. Add UI control (`frontend/src/components/Filters.jsx`)

### Modify Table Layout
Edit `frontend/src/components/CompanyTable.jsx` and `CompanyTable.css`

---

## 🚀 Deployment Checklist

### Before Deploying:

- [ ] Set `DEBUG=False` in Django
- [ ] Change `SECRET_KEY`
- [ ] Configure production database
- [ ] Set proper CORS origins
- [ ] Build React app (`npm run build`)
- [ ] Set up SSL certificates
- [ ] Configure static file serving
- [ ] Set up domain name
- [ ] Configure backups

### Recommended Services:

- **Backend:** Heroku, Railway, Render
- **Frontend:** Vercel, Netlify
- **Database:** AWS RDS, DigitalOcean

---

## 💡 Tips

1. **Regular Backups:** Export data regularly
   ```bash
   python manage.py dumpdata companies > backup.json
   ```

2. **Update Data:** Re-import CSV to update
   ```bash
   python manage.py import_companies new_data.csv
   ```

3. **Monitor Logs:** Check Django logs for errors
   ```bash
   tail -f backend/django.log
   ```

4. **Performance:** Add database indexes for frequently filtered fields

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review Django/React error messages
3. Check browser console for frontend errors
4. Verify all services are running

---

**Last Updated:** November 2025
**Version:** 1.0.0
