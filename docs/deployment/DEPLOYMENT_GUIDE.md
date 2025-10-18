# CycleX Deployment Guide 🚀

**Complete guide for deploying CycleX to production**

**Version:** 1.0  
**Last Updated:** October 2025

---

## 🎯 Deployment Overview

This guide covers:
1. **Development Environment** (Local testing)
2. **Staging Environment** (Pre-production testing)
3. **Production Environment** (Live system)
4. **Post-Deployment** (Monitoring & maintenance)

---

## 📋 Prerequisites

### System Requirements:

#### Server Specifications (Minimum):
```
CPU: 4 cores
RAM: 8 GB
Storage: 100 GB SSD
OS: Ubuntu 20.04 LTS or later
```

#### Server Specifications (Recommended Production):
```
CPU: 8+ cores
RAM: 16+ GB
Storage: 500 GB SSD (with backup)
OS: Ubuntu 22.04 LTS
```

---

### Software Requirements:

```
✅ Python 3.10 or 3.11
✅ PostgreSQL 14 or later
✅ Nginx (web server / reverse proxy)
✅ SSL Certificate (Let's Encrypt recommended)
✅ Git (for code deployment)
✅ Supervisor (process management)
```

---

## 1️⃣ Development Environment Setup

### Already Complete! ✅

**Location:** `/media/sabry3/sabry_backup/cycle_x/`

**Configuration:**
```
Odoo: odoo18/
Config: odoo_conf/odoo.conf
Database: cyclex_db
Port: 10018
Virtual Env: venv/
Custom Addons: custom_addons/cyclex/
```

**Access:**
- Backend: http://localhost:10018
- Database: postgresql://localhost:5432/cyclex_db

**Status:** ✅ Working (Phases 1-5 complete)

---

## 2️⃣ Staging Environment Setup

### Purpose:
- Test before production
- UAT (User Acceptance Testing)
- Mobile app integration testing
- Performance testing

---

### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql-14 \
    postgresql-contrib \
    nginx \
    git \
    supervisor \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    wkhtmltopdf

# Install Node.js (for asset building)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

---

### Step 2: Setup PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database user
sudo -u postgres createuser -s odoo_staging
sudo -u postgres psql -c "ALTER USER odoo_staging WITH PASSWORD 'strong_password_here';"

# Create database
sudo -u postgres createdb cyclex_staging -O odoo_staging
```

---

### Step 3: Deploy Odoo

```bash
# Create odoo user
sudo useradd -m -d /opt/odoo -U -r -s /bin/bash odoo

# Clone Odoo
sudo su - odoo
cd /opt/odoo
git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0 odoo18

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r odoo18/requirements.txt

# Install CycleX dependencies
pip install qrcode pillow requests
# pip install firebase-admin  # Phase 7
```

---

### Step 4: Deploy CycleX Module

```bash
# Clone your repository
cd /opt/odoo
git clone https://github.com/sabryyoussef/cyclex_odoo18.git repo
# OR copy from development

# Create custom addons directory
mkdir -p /opt/odoo/custom_addons
cp -r repo/custom_addons/cyclex /opt/odoo/custom_addons/

# Set permissions
sudo chown -R odoo:odoo /opt/odoo
```

---

### Step 5: Configure Odoo

```bash
# Create config file
sudo mkdir -p /etc/odoo
sudo nano /etc/odoo/odoo-staging.conf
```

**Configuration:**
```ini
[options]
admin_passwd = CHANGE_THIS_STRONG_PASSWORD
db_host = localhost
db_port = 5432
db_user = odoo_staging
db_password = strong_password_here
addons_path = /opt/odoo/odoo18/addons,/opt/odoo/custom_addons
http_port = 8069
logfile = /var/log/odoo/odoo-staging.log
log_level = info
workers = 4
max_cron_threads = 2
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200
proxy_mode = True
xmlrpc_interface = 127.0.0.1
```

**Save and exit.**

---

### Step 6: Setup Supervisor

**Purpose:** Keep Odoo running automatically

```bash
# Create supervisor config
sudo nano /etc/supervisor/conf.d/odoo-staging.conf
```

**Configuration:**
```ini
[program:odoo-staging]
command=/opt/odoo/venv/bin/python /opt/odoo/odoo18/odoo-bin -c /etc/odoo/odoo-staging.conf
directory=/opt/odoo
user=odoo
autostart=true
autorestart=true
stdout_logfile=/var/log/odoo/odoo-staging-stdout.log
stderr_logfile=/var/log/odoo/odoo-staging-stderr.log
stopasgroup=true
killasgroup=true
```

**Start Odoo:**
```bash
# Create log directory
sudo mkdir -p /var/log/odoo
sudo chown odoo:odoo /var/log/odoo

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start odoo-staging

# Check status
sudo supervisorctl status odoo-staging
# Expected: RUNNING
```

---

### Step 7: Configure Nginx

**Purpose:** Reverse proxy, SSL termination, load balancing

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/cyclex-staging
```

**Configuration:**
```nginx
upstream odoo_staging {
    server 127.0.0.1:8069;
}

server {
    listen 80;
    server_name staging.cyclex.app;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name staging.cyclex.app;

    # SSL configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/staging.cyclex.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.cyclex.app/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logs
    access_log /var/log/nginx/cyclex-staging-access.log;
    error_log /var/log/nginx/cyclex-staging-error.log;

    # Proxy settings
    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;

    # Increase buffer size
    proxy_buffers 16 64k;
    proxy_buffer_size 128k;

    # File upload size
    client_max_body_size 20M;

    # Odoo backend
    location / {
        proxy_pass http://odoo_staging;
        proxy_redirect off;
    }

    # WebSocket support (longpolling)
    location /longpolling {
        proxy_pass http://odoo_staging;
    }

    # Static files (cache)
    location ~* /web/static/ {
        proxy_cache_valid 200 90m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://odoo_staging;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/cyclex-staging /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

---

### Step 8: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d staging.cyclex.app

# Auto-renewal (certbot sets this up automatically)
sudo certbot renew --dry-run
```

---

### Step 9: Initialize Database

```bash
# As odoo user
sudo su - odoo
source venv/bin/activate
cd odoo18

# Initialize database and install module
python odoo-bin -c /etc/odoo/odoo-staging.conf \
    -d cyclex_staging \
    -i cyclex \
    --stop-after-init

# Restart Odoo
exit
sudo supervisorctl restart odoo-staging
```

---

### Step 10: Verify Deployment

**Check Services:**
```bash
# PostgreSQL
sudo systemctl status postgresql
# Expected: active (running)

# Odoo
sudo supervisorctl status odoo-staging
# Expected: RUNNING

# Nginx
sudo systemctl status nginx
# Expected: active (running)
```

**Access Application:**
```
URL: https://staging.cyclex.app
Database: cyclex_staging
Login: admin@cyclex.com
Password: (set during initialization)
```

**Test:**
- ✅ Backend loads
- ✅ CycleX module visible
- ✅ Sample data loaded
- ✅ API endpoints accessible

---

## 3️⃣ Production Environment Setup

### Differences from Staging:

```
Staging                         Production
├── staging.cyclex.app          ├── api.cyclex.app
├── cyclex_staging DB           ├── cyclex_production DB
├── Test SMS Misr account       ├── Production SMS Misr
├── Dev Firebase project        ├── Production Firebase
├── 1 server                    ├── 2+ servers (load balanced)
└── Daily backups               └── Hourly backups + replication
```

---

### Production Deployment Steps:

**Same as staging PLUS:**

#### 1. High Availability Setup

```
Load Balancer (Nginx)
         │
         ├── Odoo Server 1 (Primary)
         ├── Odoo Server 2 (Secondary)
         └── Odoo Server 3 (Secondary)
         │
         ↓
PostgreSQL Primary (Master)
         ├── Replica 1 (Read)
         └── Replica 2 (Read)
```

---

#### 2. Production Database Configuration

```bash
# PostgreSQL production config
sudo nano /etc/postgresql/14/main/postgresql.conf
```

**Optimize for production:**
```ini
max_connections = 200
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
work_mem = 10MB
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
wal_buffers = 16MB
checkpoint_completion_target = 0.9
random_page_cost = 1.1
effective_io_concurrency = 200
```

**Restart PostgreSQL:**
```bash
sudo systemctl restart postgresql
```

---

#### 3. Production Odoo Configuration

```ini
[options]
# Database
db_host = postgres-primary.cyclex.internal
db_port = 5432
db_user = odoo_prod
db_password = VERY_STRONG_PASSWORD
db_maxconn = 64

# Server
http_port = 8069
workers = 8
max_cron_threads = 4
limit_memory_hard = 4294967296
limit_memory_soft = 3221225472

# Security
admin_passwd = SUPER_STRONG_ADMIN_PASSWORD
list_db = False
proxy_mode = True

# Logging
logfile = /var/log/odoo/odoo-production.log
log_level = warn
log_db = True
log_handler = :INFO
syslog = True

# Performance
db_template = template0
unaccent = True
```

---

#### 4. Firewall Configuration

```bash
# UFW firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Close Odoo port (only accessed via Nginx)
# Port 8069 should NOT be publicly accessible
```

---

#### 5. Backup Strategy

**Daily Full Backups:**

```bash
# Create backup script
sudo nano /opt/odoo/backup.sh
```

**Script:**
```bash
#!/bin/bash
BACKUP_DIR="/backup/odoo"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="cyclex_production"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Filestore backup
tar -czf $BACKUP_DIR/filestore_$DATE.tar.gz \
    /opt/odoo/.local/share/Odoo/filestore/$DB_NAME

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Make executable:**
```bash
sudo chmod +x /opt/odoo/backup.sh
```

**Schedule with cron:**
```bash
sudo crontab -e

# Add line (daily at 2 AM):
0 2 * * * /opt/odoo/backup.sh >> /var/log/odoo/backup.log 2>&1
```

---

#### 6. Monitoring Setup

**Install monitoring tools:**

```bash
# Install Prometheus Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar -xvf node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter

# Create systemd service
sudo nano /etc/systemd/system/node_exporter.service
```

**Service configuration:**
```ini
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
```

---

## 4️⃣ Deployment Checklist

### Pre-Deployment:

- [ ] Code reviewed and tested
- [ ] All tests passing (32 automated tests)
- [ ] Sample data working
- [ ] API tested with Postman
- [ ] Database backup created
- [ ] Rollback plan prepared
- [ ] Team notified
- [ ] Maintenance window scheduled

---

### Deployment Steps:

- [ ] **Step 1:** Put site in maintenance mode
- [ ] **Step 2:** Backup current database
- [ ] **Step 3:** Pull latest code from Git
- [ ] **Step 4:** Update Python dependencies
- [ ] **Step 5:** Upgrade Odoo module
- [ ] **Step 6:** Restart Odoo service
- [ ] **Step 7:** Verify deployment
- [ ] **Step 8:** Test critical paths
- [ ] **Step 9:** Monitor logs (30 min)
- [ ] **Step 10:** Remove maintenance mode

---

### Deployment Script:

```bash
#!/bin/bash
# deploy.sh - CycleX deployment script

set -e  # Exit on error

echo "=== CycleX Deployment Started ==="
DATE=$(date +%Y%m%d_%H%M%S)

# 1. Backup
echo "Creating backup..."
sudo -u odoo /opt/odoo/backup.sh

# 2. Pull code
echo "Pulling latest code..."
cd /opt/odoo/repo
git pull origin main

# 3. Copy module
echo "Updating module..."
sudo rm -rf /opt/odoo/custom_addons/cyclex
sudo cp -r custom_addons/cyclex /opt/odoo/custom_addons/
sudo chown -R odoo:odoo /opt/odoo/custom_addons

# 4. Update dependencies
echo "Updating dependencies..."
sudo -u odoo bash -c "source /opt/odoo/venv/bin/activate && pip install -r requirements.txt"

# 5. Upgrade module
echo "Upgrading module..."
sudo -u odoo bash -c "
    source /opt/odoo/venv/bin/activate
    cd /opt/odoo/odoo18
    python odoo-bin -c /etc/odoo/odoo-production.conf \
        -d cyclex_production \
        -u cyclex \
        --stop-after-init
"

# 6. Restart Odoo
echo "Restarting Odoo..."
sudo supervisorctl restart odoo-production

# 7. Wait for startup
echo "Waiting for Odoo to start..."
sleep 10

# 8. Health check
echo "Health check..."
curl -f http://localhost:8069/web/health || exit 1

echo "=== Deployment Completed Successfully ==="
echo "Time: $DATE"
```

---

## 5️⃣ SSL/HTTPS Configuration

### Let's Encrypt Setup (Free SSL):

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d api.cyclex.app --email admin@cyclex.app --agree-tos

# Test auto-renewal
sudo certbot renew --dry-run
```

**Certificate auto-renews every 90 days.**

---

### Force HTTPS (Production):

**In Nginx:**
```nginx
# Redirect all HTTP to HTTPS
server {
    listen 80;
    server_name api.cyclex.app;
    return 301 https://$server_name$request_uri;
}
```

**In Odoo config:**
```ini
[options]
proxy_mode = True
```

---

## 6️⃣ External Services Configuration

### SMS Misr Setup (Phase 7):

**In Odoo Backend:**

1. Go to **Settings → Technical → Parameters → System Parameters**
2. Create parameters:
   ```
   Key: sms.misr.username
   Value: your_production_username

   Key: sms.misr.password
   Value: your_production_password

   Key: sms.misr.sender
   Value: CycleX
   ```

**Test SMS:**
```python
# In Odoo shell
env['cyclex.sms'].send_verification_sms(
    phone='+201234567890',
    code='123456',
    language='ar'
)
```

---

### Firebase FCM Setup (Phase 7):

**Prerequisites from Mobile Team:**
- Firebase Server Key
- Android package name
- iOS bundle ID

**In Odoo Backend:**

1. Install library:
   ```bash
   sudo -u odoo bash -c "source /opt/odoo/venv/bin/activate && pip install firebase-admin"
   ```

2. Set parameter:
   ```
   Key: firebase.server_key
   Value: AAAA...xxxx (from mobile team)
   ```

3. Restart Odoo:
   ```bash
   sudo supervisorctl restart odoo-production
   ```

---

## 7️⃣ Database Migration

### From Staging to Production:

**Option 1: Fresh Install**
```bash
# 1. Install module in production
# 2. Load sample data
# 3. Manually create any custom records
```

**Option 2: Copy Staging Data**
```bash
# 1. Backup staging database
sudo -u postgres pg_dump cyclex_staging > staging_export.sql

# 2. Import to production (CAREFUL!)
sudo -u postgres psql cyclex_production < staging_export.sql

# 3. Update system parameters for production
# (SMS credentials, Firebase key, etc.)
```

**⚠️ Warning:** Never copy production data back to staging!

---

## 8️⃣ Post-Deployment

### Immediate Checks (First Hour):

```
□ Application loads without errors
□ Login works (admin user)
□ CycleX module menu visible
□ Sample data present
□ API endpoints respond (test with Postman)
□ Customer registration works
□ Collector registration works
□ Request creation works
□ QR code generation works
□ Wallet operations work
□ No errors in logs
```

---

### Monitoring (First Week):

**Daily Checks:**
```
□ Check error logs: /var/log/odoo/odoo-production.log
□ Check Nginx logs: /var/log/nginx/cyclex-*.log
□ Monitor database performance
□ Check disk space usage
□ Review cron job execution logs
□ Monitor API response times
□ Check for security issues
```

**Weekly Checks:**
```
□ Review backup logs
□ Test backup restoration
□ Check SSL certificate validity
□ Review user growth
□ Monitor server resources (CPU, RAM, disk)
□ Check for Odoo/security updates
```

---

### Log Monitoring:

```bash
# Watch Odoo logs in real-time
sudo tail -f /var/log/odoo/odoo-production.log

# Check for errors
sudo grep -i error /var/log/odoo/odoo-production.log | tail -50

# Check for warnings
sudo grep -i warning /var/log/odoo/odoo-production.log | tail -50

# Monitor Nginx access
sudo tail -f /var/log/nginx/cyclex-production-access.log

# Check Nginx errors
sudo tail -f /var/log/nginx/cyclex-production-error.log
```

---

## 9️⃣ Performance Optimization

### Odoo Performance:

**1. Enable Caching:**
```ini
[options]
data_dir = /opt/odoo/.local/share/Odoo
```

**2. Optimize Workers:**
```ini
# Formula: (CPU cores * 2) + 1
# For 8 cores: (8 * 2) + 1 = 17 workers
workers = 17
```

**3. Database Connection Pooling:**
```ini
db_maxconn = 64
db_template = template0
```

---

### PostgreSQL Performance:

**1. Vacuum Database (Weekly):**
```bash
sudo -u postgres vacuumdb -z cyclex_production
```

**2. Analyze Database:**
```bash
sudo -u postgres psql cyclex_production -c "ANALYZE;"
```

**3. Reindex (Monthly):**
```bash
sudo -u postgres reindexdb cyclex_production
```

---

### Nginx Performance:

**Enable Gzip Compression:**
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/json
    application/javascript
    application/xml+rss;
```

---

## 🔟 Scaling Strategy

### Vertical Scaling (Single Server):

**Upgrade Resources:**
```
4 CPU → 8 CPU
8 GB RAM → 16 GB RAM
100 GB Storage → 500 GB Storage
```

**Update Odoo workers:**
```ini
workers = 17  # Updated based on new CPU count
```

---

### Horizontal Scaling (Multiple Servers):

**Load Balancer Configuration:**

```nginx
upstream odoo_cluster {
    server odoo1.internal:8069 weight=3;
    server odoo2.internal:8069 weight=2;
    server odoo3.internal:8069 weight=1;
    
    # Health checks
    keepalive 32;
}

server {
    location / {
        proxy_pass http://odoo_cluster;
    }
}
```

**Session Persistence:**
- Use database-backed sessions (default in Odoo)
- OR configure sticky sessions in load balancer

---

## 1️⃣1️⃣ Troubleshooting Deployment

### Issue: Odoo Won't Start

**Check:**
```bash
# View supervisor logs
sudo tail -100 /var/log/odoo/odoo-production-stderr.log

# Common issues:
# - Database connection failed
# - Port already in use
# - Permission denied
# - Missing Python dependencies
```

**Fix:**
1. Check PostgreSQL is running
2. Verify database credentials
3. Check port conflicts: `sudo lsof -i :8069`
4. Fix permissions: `sudo chown -R odoo:odoo /opt/odoo`

---

### Issue: 502 Bad Gateway

**Symptoms:** Nginx shows 502 error

**Check:**
```bash
# Is Odoo running?
sudo supervisorctl status odoo-production

# Check Odoo logs
sudo tail -50 /var/log/odoo/odoo-production.log
```

**Fix:**
1. Restart Odoo: `sudo supervisorctl restart odoo-production`
2. Check Nginx upstream: `sudo nginx -t`
3. Verify port 8069 is accessible

---

### Issue: Module Not Found

**Symptoms:** "Module cyclex not found"

**Fix:**
```bash
# Check addons path
grep addons_path /etc/odoo/odoo-production.conf

# Verify module exists
ls -la /opt/odoo/custom_addons/cyclex

# Check permissions
sudo chown -R odoo:odoo /opt/odoo/custom_addons

# Restart Odoo
sudo supervisorctl restart odoo-production
```

---

## 1️⃣2️⃣ Rollback Procedure

### If Deployment Fails:

```bash
#!/bin/bash
# rollback.sh

echo "Rolling back deployment..."

# 1. Stop Odoo
sudo supervisorctl stop odoo-production

# 2. Restore database from backup
BACKUP_FILE="/backup/odoo/db_20251017_020000.sql.gz"
sudo -u postgres dropdb cyclex_production
sudo -u postgres createdb cyclex_production -O odoo_prod
gunzip < $BACKUP_FILE | sudo -u postgres psql cyclex_production

# 3. Restore previous code
cd /opt/odoo/repo
git reset --hard HEAD~1  # Go back 1 commit

# 4. Copy previous module version
sudo cp -r custom_addons/cyclex /opt/odoo/custom_addons/

# 5. Restart Odoo
sudo supervisorctl start odoo-production

echo "Rollback completed"
```

---

## 1️⃣3️⃣ Security Hardening

### 1. Database Security:

```bash
# PostgreSQL authentication
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

**Configuration:**
```
# Only allow local connections
local   all             odoo_prod                               md5
host    all             odoo_prod       127.0.0.1/32           md5
```

---

### 2. Odoo Security:

```ini
[options]
# Disable database manager in production
list_db = False

# Strong admin password
admin_passwd = RANDOM_64_CHAR_PASSWORD

# Limit request size
limit_request = 8192

# Enable proxy mode (for correct IP logging)
proxy_mode = True
```

---

### 3. System Security:

```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Install fail2ban (prevent brute force)
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
```

---

## 1️⃣4️⃣ Production URLs

### Staging Environment:
```
Backend: https://staging.cyclex.app
API Base: https://staging.cyclex.app/api/cyclex
Database: cyclex_staging
```

### Production Environment:
```
Backend: https://admin.cyclex.app
API Base: https://api.cyclex.app/api/cyclex
Database: cyclex_production
```

### Mobile App Configuration:

**Staging:**
```dart
// Flutter app config
const String API_BASE_URL = 'https://staging.cyclex.app';
```

**Production:**
```dart
const String API_BASE_URL = 'https://api.cyclex.app';
```

---

## 1️⃣5️⃣ Maintenance Procedures

### Regular Maintenance (Monthly):

```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Update Odoo (if needed)
cd /opt/odoo/odoo18
git pull origin 18.0

# 3. Update custom module
cd /opt/odoo/repo
git pull origin main

# 4. Vacuum database
sudo -u postgres vacuumdb -z cyclex_production

# 5. Review logs
sudo journalctl -u odoo-production --since "1 month ago" | grep -i error

# 6. Check disk space
df -h

# 7. Test backups
# Restore to test server and verify

# 8. Update documentation
# Document any changes made
```

---

## 1️⃣6️⃣ Disaster Recovery

### Scenario: Complete Server Failure

**Recovery Steps:**

```bash
# 1. Provision new server
# (same specs or better)

# 2. Install all software
# (follow deployment guide)

# 3. Restore database
sudo -u postgres createdb cyclex_production -O odoo_prod
gunzip < latest_backup.sql.gz | sudo -u postgres psql cyclex_production

# 4. Restore filestore
tar -xzf filestore_backup.tar.gz -C /opt/odoo/.local/share/Odoo/filestore/

# 5. Deploy code
git clone repository
cp -r custom_addons/cyclex /opt/odoo/custom_addons/

# 6. Configure and start
# (Nginx, Supervisor, etc.)

# 7. Update DNS
# Point domain to new server IP

# 8. Test thoroughly
```

**RTO (Recovery Time Objective):** 4 hours  
**RPO (Recovery Point Objective):** 24 hours (daily backups)

---

## 1️⃣7️⃣ Environment Variables Summary

### Development:
```bash
export ODOO_RC=/media/sabry3/sabry_backup/cycle_x/odoo_conf/odoo.conf
export ODOO_DB=cyclex_db
export ODOO_PORT=10018
```

### Staging:
```bash
export ODOO_RC=/etc/odoo/odoo-staging.conf
export ODOO_DB=cyclex_staging
export ODOO_PORT=8069
export ODOO_URL=https://staging.cyclex.app
```

### Production:
```bash
export ODOO_RC=/etc/odoo/odoo-production.conf
export ODOO_DB=cyclex_production
export ODOO_PORT=8069
export ODOO_URL=https://api.cyclex.app
```

---

## 1️⃣8️⃣ Deployment Timeline

### Phase 7 (Before Mobile Launch):

**Week 1-2: Staging Deployment**
- Deploy to staging server
- Configure SMS Misr (test mode)
- Test all APIs
- Load sample data
- UAT with team

**Week 3-4: Mobile Team Coordination**
- Provide API URL to mobile team
- Wait for Firebase Server Key
- Test mobile app integration
- Fix any API issues

---

### Phase 8 (Mobile Development):

**Parallel Work:**
- Backend: Implement SMS & Firebase (Phase 7)
- Mobile: Build Flutter app (Phase 8)
- Testing: End-to-end testing

---

### Phase 9 (Production Launch):

**Week 1: Production Setup**
- Provision production servers
- Deploy to production
- Configure production SMS Misr
- Configure production Firebase

**Week 2: Beta Testing**
- Invite beta testers (50-100 users)
- Monitor closely
- Fix critical bugs
- Gather feedback

**Week 3: Public Launch**
- Remove beta restrictions
- Marketing campaign
- Monitor scaling
- 24/7 support ready

---

## 1️⃣9️⃣ Deployment Checklist

### Pre-Launch Checklist:

**Technical:**
- [ ] All automated tests passing (32 tests)
- [ ] API tested with Postman (22 endpoints)
- [ ] SSL certificate installed
- [ ] Backups automated and tested
- [ ] Monitoring configured
- [ ] Logs aggregated
- [ ] Firewall configured
- [ ] Security audit completed

**Business:**
- [ ] Admin trained
- [ ] Support team ready
- [ ] SMS Misr account funded
- [ ] Firebase configured
- [ ] Terms & conditions ready
- [ ] Privacy policy published
- [ ] Pricing finalized
- [ ] Working areas defined

**Mobile:**
- [ ] iOS app submitted to App Store
- [ ] Android app submitted to Play Store
- [ ] API URL configured in apps
- [ ] Test devices verified
- [ ] Push notifications tested

---

## 2️⃣0️⃣ Support Contacts

### Emergency Contacts:

```
Technical Lead: [Name] - [Phone]
Database Admin: [Name] - [Phone]
DevOps: [Name] - [Phone]
Mobile Team Lead: [Name] - [Phone]

On-Call Schedule:
- Week 1: [Name]
- Week 2: [Name]
```

### Vendor Support:

```
SMS Misr Support: support@smsmisr.com
Firebase Support: firebase-support@google.com
Hosting Provider: [Provider support]
```

---

## ✅ Quick Reference

### Common Commands:

| Task | Command |
|------|---------|
| Restart Odoo | `sudo supervisorctl restart odoo-production` |
| View logs | `sudo tail -f /var/log/odoo/odoo-production.log` |
| Backup database | `/opt/odoo/backup.sh` |
| Check status | `sudo supervisorctl status` |
| Reload Nginx | `sudo systemctl reload nginx` |
| Renew SSL | `sudo certbot renew` |

---

**Deployment complete! 🎉**

For technical support during deployment, refer to:
- `DATABASE_SCHEMA.md` - Database structure
- `BACKEND_WORKFLOWS.md` - Business processes
- `API_DOCUMENTATION.md` - API reference
- `USER_ROLES_PERMISSIONS.md` - Security model

**Good luck with your deployment! 🚀**

