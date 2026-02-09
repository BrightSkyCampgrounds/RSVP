# Deployment Guide for Campspots

## Option 1: Railway (Recommended - Fastest)

Railway offers easy deployment with PostgreSQL included. Free trial available with $5 credit.

### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Install Railway CLI** (optional but recommended)
   ```bash
   # Using npm
   npm install -g @railway/cli

   # Or using curl
   curl -fsSL https://railway.app/install.sh | sh
   ```

3. **Initialize Git Repository**
   ```bash
   cd /mnt/c/Users/jahhe/Dropbox/Apps/Campspots
   git init
   git add .
   git commit -m "Initial commit - Campspots reservation system"
   ```

4. **Deploy to Railway**

   **Option A: Using Railway CLI** (Fastest)
   ```bash
   railway login
   railway init
   railway up
   ```

   **Option B: Using Railway Dashboard**
   - Go to https://railway.app/new
   - Click "Deploy from GitHub repo"
   - Connect your GitHub account
   - Push code to GitHub first:
     ```bash
     # Create a new repo on GitHub, then:
     git remote add origin https://github.com/yourusername/campspots.git
     git push -u origin main
     ```
   - Select the repository
   - Railway will auto-detect it's a Python app

5. **Add PostgreSQL Database**
   - In Railway dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically set DATABASE_URL

6. **Set Environment Variables**

   In Railway dashboard, go to Variables tab and add:
   ```
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
   FLASK_ENV=production
   SITE_NAME=Bright Sky Campgrounds
   ADMIN_EMAIL=reservations@brightskycampgrounds.com
   ```

7. **Deploy!**
   - Railway will automatically deploy
   - Get your URL from the dashboard (e.g., `campspots-production.up.railway.app`)

---

## Option 2: Render (Also Easy + Free Tier)

Render has a generous free tier (slower startup but works well).

### Steps:

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Push to GitHub** (if not already)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   # Create repo on GitHub, then:
   git remote add origin https://github.com/yourusername/campspots.git
   git push -u origin main
   ```

3. **Create Web Service**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** campspots
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python init_db.py && gunicorn app:app`
     - **Plan:** Free

4. **Add PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name it `campspots-db`
   - Plan: Free
   - Copy the "Internal Database URL"

5. **Set Environment Variables**

   In your web service settings, add:
   ```
   DATABASE_URL=<paste Internal Database URL from step 4>
   SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
   FLASK_ENV=production
   SITE_NAME=Bright Sky Campgrounds
   ADMIN_EMAIL=reservations@brightskycampgrounds.com
   ```

6. **Deploy!**
   - Render will automatically deploy
   - Your URL will be `campspots.onrender.com`

---

## Option 3: DigitalOcean App Platform ($5/month)

More reliable than free tiers, but costs $5/month.

### Steps:

1. **Create DigitalOcean Account**
   - Go to https://digitalocean.com
   - Sign up and add payment method

2. **Push to GitHub** (if not already)

3. **Create App**
   - Go to Apps → Create App
   - Connect GitHub repository
   - DigitalOcean will auto-detect Python

4. **Add Database**
   - In app settings, add PostgreSQL database ($7/month for managed)
   - Or use SQLite for testing (not recommended for production)

5. **Set Environment Variables** (same as above)

6. **Deploy!**

---

## Quick Deploy with Railway CLI (Fastest Method)

If you want to deploy RIGHT NOW:

```bash
# From WSL
cd /mnt/c/Users/jahhe/Dropbox/Apps/Campspots

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login and deploy
railway login
railway init
railway add --database postgresql
railway up

# Set environment variables
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
railway variables set STRIPE_SECRET_KEY=sk_test_your_key_here
railway variables set STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
railway variables set FLASK_ENV=production

# Get your URL
railway open
```

---

## Post-Deployment Checklist

After deploying:

- [ ] Test the homepage loads
- [ ] Test availability checker works
- [ ] Make a test booking with Stripe test card (4242 4242 4242 4242)
- [ ] Verify confirmation page shows
- [ ] Check admin dashboard works
- [ ] Set up custom domain (optional)
- [ ] Add admin authentication before going live with real bookings!
- [ ] Switch to Stripe live keys when ready for real payments

---

## Custom Domain Setup

### Railway:
1. Go to Settings → Domains
2. Add custom domain: `reservations.brightskycampgrounds.com`
3. Add CNAME record in your DNS:
   - Name: `reservations`
   - Value: `<your-app>.up.railway.app`

### Render:
1. Go to Settings → Custom Domain
2. Add domain
3. Update DNS with provided CNAME

---

## Troubleshooting

**Database not initializing?**
- Check logs for errors
- Make sure DATABASE_URL is set correctly
- Try manual init: `railway run python init_db.py`

**Static files not loading?**
- Flask serves them automatically in production
- Check browser console for 404 errors

**Stripe errors?**
- Verify keys are set correctly
- Make sure they start with `sk_test_` and `pk_test_`
- No quotes or spaces in environment variables

---

## Monitoring

**Railway:**
- Logs: `railway logs`
- Metrics: Available in dashboard

**Render:**
- Logs available in dashboard
- Set up alerts for errors

---

## Scaling for Production

When you start getting real traffic:

1. **Upgrade database** - Move from free tier to paid
2. **Add monitoring** - Use Sentry or similar for error tracking
3. **Add email service** - SendGrid, Mailgun for confirmation emails
4. **Enable HTTPS** - Automatic on Railway/Render
5. **Add admin auth** - Critical before going live!
6. **Set up backups** - Database backup schedule
7. **Use live Stripe keys** - Switch from test to production mode

---

## Need Help?

- Railway docs: https://docs.railway.app
- Render docs: https://render.com/docs
- Flask deployment: https://flask.palletsprojects.com/en/3.0.x/deploying/
