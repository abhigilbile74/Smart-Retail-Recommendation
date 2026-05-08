# Deployment Configuration Guide

## Quick Start Deployment Checklist

✅ **Pre-deployment Requirements**
- [x] `.gitignore` - Excludes unnecessary files
- [x] `README.md` - Complete documentation
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `Procfile` - Heroku deployment config
- [x] `setup.sh` - Setup script for deployment
- [x] Error handling in `app.py`
- [x] Proper path handling for data files
- [x] Python version specified

## Deployment Options

### 1. **Streamlit Cloud (Recommended - Easiest)**

**Pros**: Free tier, automatic deployments, minimal configuration
**Steps**:
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New app"
# 4. Select your repository
# 5. Set main file path: app/app.py
# 6. Click "Deploy"
```

**For sensitive data**: Add secrets in Streamlit Cloud dashboard

---

### 2. **Heroku Deployment**

**Pros**: Full control, paid tier available, good for production
**Prerequisites**:
```bash
# Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
heroku login
```

**Steps**:
```bash
# 1. Create Heroku app
heroku create your-app-name

# 2. Push code
git push heroku main

# 3. View logs
heroku logs --tail

# 4. Open app
heroku open
```

**Environment Variables**:
```bash
heroku config:set PYTHONUNBUFFERED=1
```

---

### 3. **Docker Deployment (AWS, Azure, GCP)**

**Create `Dockerfile`**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/app.py"]
```

**Build & Deploy**:
```bash
docker build -t basket-recommendation .
docker run -p 8501:8501 basket-recommendation
```

---

### 4. **AWS Deployment**

**Using AWS App Runner**:
1. Push code to GitHub
2. Connect GitHub repo in AWS App Runner
3. Configure build settings: `streamlit run app/app.py`
4. Deploy

---

### 5. **Azure Deployment**

**Using Azure App Service**:
```bash
az webapp up --name your-app-name --runtime "PYTHON|3.11"
```

---

## Environment Variables

Create `.env` for local development (not committed):
```
MIN_SUPPORT=0.02
MIN_CONFIDENCE=0.3
DATA_PATH=data/grocerie.csv
```

---

## Pre-deployment Checks

Run these before deploying:

```bash
# 1. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
streamlit run app/app.py

# 4. Check file structure
tree -a -I 'venv|__pycache__|.git'

# 5. Verify data exists
ls -la data/grocerie.csv

# 6. Check Python version
python --version  # Should be 3.8+
```

---

## Troubleshooting Deployment

### Issue: "Module not found"
**Solution**: Ensure `sys.path.append()` in app.py is correct

### Issue: "Data file not found"
**Solution**: Verify data path in deployment environment

### Issue: "Out of memory"
**Solution**: Add Dyno resources or sample data for testing

### Issue: "Slow performance"
**Solution**: Optimize Apriori parameters or use smaller dataset

---

## Performance Optimization

1. **Cache data processing**:
   ```python
   @st.cache_data
   def load_and_process_data():
       ...
   ```

2. **Lazy load visualizations**:
   ```python
   if condition:
       st.plotly_chart(fig)
   ```

3. **Monitor resource usage**:
   - Streamlit Cloud: Dashboard
   - Heroku: `heroku ps`
   - Docker: `docker stats`

---

## Maintenance

- **Update dependencies**: `pip install --upgrade -r requirements.txt`
- **Monitor errors**: Check deployment logs regularly
- **Backup data**: Store CSV in reliable storage
- **Version control**: Tag releases: `git tag v1.0.0`

---

## Security Checklist

- [ ] No hardcoded credentials
- [ ] `.env` is in `.gitignore`
- [ ] Use environment variables for config
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Restrict data access if needed
- [ ] Keep dependencies updated

---

## Support Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/deploy)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: May 2026
