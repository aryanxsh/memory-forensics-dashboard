# 🚀 Deployment Guide

This guide covers different ways to deploy your Memory Forensics Dashboard.

## 📋 Prerequisites

- Python 3.7 or higher
- Git
- GitHub account (for GitHub hosting)

## 🐙 GitHub Hosting

### 1. Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "+" → "New repository"
3. Name: `memory-forensics-dashboard`
4. Make it Public
5. **Don't** initialize with README

### 2. Push Your Code

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/memory-forensics-dashboard.git

# Push to GitHub
git push -u origin main
```

### 3. Enable GitHub Pages (Optional)

1. Go to repository Settings
2. Scroll to Pages section
3. Source: Deploy from branch
4. Branch: main, folder: root
5. Save

## ☁️ Cloud Deployment Options

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Railway Deployment

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will auto-detect Python and deploy

### Render Deployment

1. Go to [Render.com](https://render.com)
2. Connect your GitHub repository
3. Choose "Web Service"
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python app.py`

## 🔧 Environment Variables

For cloud deployment, you may need to set environment variables:

```bash
# For Heroku/Railway/Render
FLASK_ENV=production
PORT=5000
```

## 📦 Local Deployment

### Windows
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Linux/Mac
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the application
python3 app.py
```

## 🐳 Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build and Run
```bash
# Build image
docker build -t memory-forensics-dashboard .

# Run container
docker run -p 5000:5000 memory-forensics-dashboard
```

## 🔒 Security Considerations

### For Production Deployment

1. **Change Default Port**
   ```python
   # In app.py
   app.run(debug=False, host='0.0.0.0', port=8080)
   ```

2. **Add Authentication**
   ```python
   # Add basic auth
   from flask_httpauth import HTTPBasicAuth
   auth = HTTPBasicAuth()
   ```

3. **Use HTTPS**
   - Enable SSL certificates
   - Use reverse proxy (nginx)

4. **Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

## 📊 Monitoring

### Add Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### Logging Configuration
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 5000
   netstat -ano | findstr :5000
   # Kill process
   taskkill /PID <PID> /F
   ```

2. **Permission Errors**
   ```bash
   # Run as administrator (Windows)
   # Use sudo (Linux/Mac)
   ```

3. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## 📞 Support

- Create issues on GitHub
- Check deployment logs
- Verify environment variables
- Test locally before deploying

---

**🎯 Quick Start**: For GitHub hosting, just push your code and enable Pages in repository settings! 