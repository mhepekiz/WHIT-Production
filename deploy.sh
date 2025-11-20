#!/bin/bash

# WHIT Application Deployment Script for Linode/Ubuntu
# This script prepares your application for production deployment on nahhat.com

echo "🚀 Starting WHIT deployment setup for nahhat.com..."

# Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
   exit 1
fi

print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

print_status "Installing required system packages..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib certbot python3-certbot-nginx git curl

# Install Node.js (for frontend build)
print_status "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Create application directory
print_status "Setting up application directory..."
sudo mkdir -p /var/www/whit
sudo chown -R $USER:$USER /var/www/whit

# Copy application files (you'll need to upload your code)
print_status "Application files should be uploaded to /var/www/whit"
print_warning "Please upload your WHIT project files to /var/www/whit using scp, rsync, or git clone"

# Setup PostgreSQL database
print_status "Setting up PostgreSQL database..."
sudo -u postgres createdb whit_production || print_warning "Database might already exist"
sudo -u postgres createuser whit_user || print_warning "User might already exist"

echo "Please set a password for the database user 'whit_user':"
sudo -u postgres psql -c "ALTER USER whit_user WITH PASSWORD 'your_secure_password_here';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE whit_production TO whit_user;"

print_status "Database setup completed. Please update your .env.production file with the correct database credentials."

# Setup Python virtual environment (to be done after code upload)
echo "
📋 NEXT STEPS (after uploading your code to /var/www/whit):

1. Setup Python environment:
   cd /var/www/whit/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn

2. Setup environment variables:
   cp ../.env.production .env
   # Edit .env with your actual values

3. Run Django setup:
   python manage.py collectstatic --noinput
   python manage.py migrate
   python manage.py createsuperuser

4. Build frontend:
   cd /var/www/whit/frontend
   npm install
   npm run build

5. Setup systemd service:
   sudo cp ../whit.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable whit
   sudo systemctl start whit

6. Setup NGINX:
   sudo cp ../nginx.conf /etc/nginx/sites-available/nahhat.com
   sudo ln -s /etc/nginx/sites-available/nahhat.com /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx

7. Setup SSL with Let's Encrypt:
   sudo certbot --nginx -d nahhat.com -d www.nahhat.com

8. Configure firewall:
   sudo ufw allow 'Nginx Full'
   sudo ufw allow ssh
   sudo ufw enable

9. Test your application:
   Visit https://nahhat.com

📝 IMPORTANT NOTES:
- Update DNS A records to point nahhat.com to your Linode server IP
- Set strong passwords in .env.production
- Configure proper backup strategy for your database
- Monitor logs: sudo journalctl -u whit -f
"

print_success "Initial deployment setup completed!"
print_warning "Please follow the next steps above to complete the deployment."