# CycleX - Odoo 18 Setup Instructions

This guide will help you set up the development environment for CycleX with Odoo 18.

---

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.10+** installed
2. **PostgreSQL** installed and running
3. **System dependencies** for Odoo:

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    git \
    postgresql \
    postgresql-client \
    wkhtmltopdf
```

---

## 🚀 Quick Setup

### Method 1: Using the Setup Script (Recommended)

```bash
# Make the script executable
chmod +x setup_venv.sh

# Run the setup script
./setup_venv.sh
```

### Method 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip setuptools wheel

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 📂 Project Structure

After setup, your project structure should look like:

```
cycle_x/
├── venv/                      # Virtual environment (created by setup)
├── cyclex/                    # CycleX Odoo module
│   ├── models/
│   ├── views/
│   ├── controllers/
│   ├── security/
│   └── ...
├── planning/                  # Project documentation
├── requirements.txt           # Python dependencies
├── setup_venv.sh             # Setup script
└── SETUP_INSTRUCTIONS.md     # This file
```

---

## 🔧 Odoo 18 Installation

### Option 1: Using Existing Odoo Installation

If you already have Odoo 18 installed at `/home/edafa/odoo-dev/`:

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Add CycleX to addons path in your Odoo config:**
   ```ini
   # Edit: /home/edafa/odoo-dev/conf/odoo18.conf
   [options]
   addons_path = /home/edafa/odoo-dev/odoo/addons,/media/sabry3/sabry_backup/cycle_x
   ```

3. **Restart Odoo via PyCharm** (as per your preference)

### Option 2: Clone Odoo 18

If you need to set up Odoo 18 from scratch:

```bash
# 1. Navigate to your development directory
cd /home/edafa/odoo-dev/

# 2. Clone Odoo 18
git clone https://github.com/odoo/odoo.git --branch 18.0 --depth 1

# 3. Activate CycleX virtual environment
cd /media/sabry3/sabry_backup/cycle_x
source venv/bin/activate

# 4. Install Odoo requirements
pip install -r /home/edafa/odoo-dev/odoo/requirements.txt

# 5. Create Odoo configuration file
# (Use your existing config at /home/edafa/odoo-dev/conf/odoo18.conf)
```

---

## 🗄️ Database Setup

### Create PostgreSQL Database

```bash
# 1. Create database user (if not exists)
sudo -u postgres createuser -s $USER

# 2. Create database for CycleX
createdb cyclex_dev
```

### Update Odoo Configuration

Edit your Odoo config file (`/home/edafa/odoo-dev/conf/odoo18.conf`):

```ini
[options]
addons_path = /home/edafa/odoo-dev/odoo/addons,/media/sabry3/sabry_backup/cycle_x
db_host = localhost
db_port = 5432
db_user = YOUR_USERNAME
db_password = YOUR_PASSWORD
db_name = cyclex_dev
```

---

## 🎯 Installing CycleX Module

### Via PyCharm (Your Preferred Method)

1. **Start Odoo** via PyCharm with your configuration
2. **Navigate to Apps** in Odoo web interface
3. **Remove Apps filter** (search for "CycleX")
4. **Install the CycleX module**

### Via Command Line (Alternative)

```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to Odoo directory
cd /home/edafa/odoo-dev/odoo

# Install CycleX module
python odoo-bin -c /home/edafa/odoo-dev/conf/odoo18.conf -d cyclex_dev -i cyclex --stop-after-init
```

---

## 🧪 Verify Installation

After installation, verify:

1. ✅ **CycleX menu appears** in Odoo backend
2. ✅ **Security groups created**:
   - Settings → Users & Companies → Groups
   - Look for: CycleX / Customer, Collector, Manager, Administrator
3. ✅ **Views accessible**:
   - CycleX → Customers
   - CycleX → Collectors
   - CycleX → Configuration → Working Areas
4. ✅ **No errors in logs**

---

## 🔄 Development Workflow

### Activating Virtual Environment

Every time you work on the project:

```bash
cd /media/sabry3/sabry_backup/cycle_x
source venv/bin/activate
```

### Updating the Module

When you make changes to CycleX:

1. **Via PyCharm**: Use the built-in Odoo tools to upgrade the module
2. **Via Command Line**:
   ```bash
   python odoo-bin -c /path/to/config.conf -d cyclex_dev -u cyclex --stop-after-init
   ```

### Deactivating Virtual Environment

```bash
deactivate
```

---

## 📦 Installing Additional Packages

If you need to install more Python packages:

```bash
# Activate virtual environment
source venv/bin/activate

# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

---

## 🐛 Troubleshooting

### Python Version Issues

```bash
# Check Python version
python3 --version

# If wrong version, specify:
python3.10 -m venv venv
```

### Missing System Dependencies

```bash
# If you encounter errors about missing headers:
sudo apt-get install python3-dev libpq-dev libldap2-dev libsasl2-dev
```

### PostgreSQL Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start if needed
sudo systemctl start postgresql
```

### Module Not Found

```bash
# Verify addons path includes CycleX directory
# Check Odoo config file:
cat /home/edafa/odoo-dev/conf/odoo18.conf | grep addons_path
```

---

## 📚 Additional Resources

- **Odoo 18 Documentation**: https://www.odoo.com/documentation/18.0/
- **Python Virtual Environments**: https://docs.python.org/3/library/venv.html
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

---

## 💡 Tips

1. **Always activate the virtual environment** before running Odoo or installing packages
2. **Use PyCharm's Odoo integration** for easier development
3. **Keep requirements.txt updated** when adding new dependencies
4. **Run module upgrades** after making model or view changes
5. **Check logs** for detailed error messages

---

## 🆘 Need Help?

If you encounter issues:

1. Check the Odoo logs (usually in `~/.local/share/Odoo/` or configured log path)
2. Verify all dependencies are installed: `pip list`
3. Ensure database is accessible
4. Check file permissions on the CycleX module directory

---

**Happy Coding! 🚀**

