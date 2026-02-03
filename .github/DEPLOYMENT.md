# GitHub Actions Deployment Pipeline

This repository includes automated deployment pipelines using a GitFlow branching strategy.

## Branching Strategy

- **`develop` branch**: Development and testing → deploys to staging
- **`main` branch**: Production-ready code → deploys to production
- **Feature branches**: Create from develop, merge back to develop
- **Hotfixes**: Create from main, merge to both main and develop

## Workflows

### 1. Staging Deployment (`deploy.yml`)
- **Trigger**: Automatically on push to `develop` branch
- **Target**: `staging.whoishiringintech.com`
- **Purpose**: Continuous deployment for testing and review

### 2. Production Deployment (`deploy-production.yml`)
- **Trigger**: Automatically on push to `main` branch, manual dispatch, or releases
- **Target**: `nahhat.com`
- **Purpose**: Controlled production deployments

## Development Workflow

### For New Features:
1. Create feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Develop and commit your changes:
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/your-feature-name
   ```

3. Create Pull Request to merge into `develop`
4. Once merged, staging deployment triggers automatically

### For Production Release:
1. Create Pull Request from `develop` to `main`
2. Review and test thoroughly on staging first
3. Merge to `main` → triggers production deployment automatically

### For Hotfixes:
1. Create hotfix branch from `main`:
   ```bash
   git checkout main
   git checkout -b hotfix/critical-fix
   ```
2. Fix the issue and commit
3. Create PR to `main` for immediate production fix
4. Also merge the hotfix back to `develop`

## Required GitHub Secrets

You need to configure these secrets in your GitHub repository settings:

### For Staging Deployment:
- `SERVER_HOST`: Your server IP address (45.79.211.144)
- `SERVER_USERNAME`: SSH username for your server
- `SERVER_SSH_KEY`: Private SSH key for authentication

### For Production Deployment:
- `PROD_SERVER_HOST`: Production server IP (can be same as staging)
- `PROD_SERVER_USERNAME`: SSH username for production server
- `PROD_SERVER_SSH_KEY`: Private SSH key for production

## Setting up SSH Keys

1. **Generate SSH key pair** (if you don't have one):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-actions@yourdomain.com"
   ```

2. **Add public key to server**:
   ```bash
   ssh-copy-id -i ~/.ssh/id_rsa.pub username@45.79.211.144
   ```

3. **Copy private key content** and add it to GitHub secrets:
   ```bash
   cat ~/.ssh/id_rsa
   ```

## Server Prerequisites

Ensure your server has:
- Python 3.11+
- Node.js 18+
- Nginx
- Systemd
- Required Python packages (pip, virtualenv)

## Deployment Process

### Staging Deployment
1. Push changes to `develop` branch (or merge PR into develop)
2. GitHub Actions automatically:
   - Builds React frontend
   - Runs Django tests
   - Deploys to staging server
   - Updates nginx configuration
   - Restarts services
   - Verifies deployment

### Production Deployment
1. Create PR from `develop` to `main`
2. Review and approve the PR
3. Merge to `main` branch
4. GitHub Actions automatically performs the same steps as staging plus:
   - Security checks (bandit, safety)
   - Production environment protection
   - Comprehensive verification

### Alternative Production Deployment
- Create a GitHub release, or
- Manually trigger the workflow from Actions tab

## Manual Deployment

You can still deploy manually using the existing scripts:
- `./deploy.sh` - Deploy to current server
- `./start.sh` - Start services
- `./restart_servers.sh` - Restart all services

## Monitoring

Check deployment status:
- GitHub Actions tab for build/deployment logs
- Server logs: `/var/log/nginx/` and `journalctl -u whit`
- Service status: `systemctl status whit nginx`

## Rollback

If deployment fails, the pipeline automatically creates backups:
```bash
# List available backups
ls -la /var/www/whit-backup-*

# Restore from backup
sudo systemctl stop whit
sudo rm -rf /var/www/whit
sudo mv /var/www/whit-backup-YYYYMMDD-HHMMSS /var/www/whit
sudo systemctl start whit
```

## Environment Variables

The deployment expects these environment variables to be set on the server:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- Database credentials (if using external database)

Create a `.env` file in `/var/www/whit/backend/` with these values.

## Troubleshooting

Common issues and solutions:

1. **SSH Permission Denied**: Check SSH key format and permissions
2. **Nginx Test Failed**: Verify nginx configuration syntax
3. **Django Won't Start**: Check Python dependencies and database connectivity
4. **Frontend Not Loading**: Verify build process and static file paths

For detailed logs, check the GitHub Actions workflow runs and server logs.