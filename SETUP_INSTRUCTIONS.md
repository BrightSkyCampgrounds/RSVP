# Campspots Setup Instructions

## Initial Setup

### Option 1: Using WSL (Recommended for your environment)

Based on your system configuration, you use WSL (Arch Linux) for Python development.

1. **Open WSL terminal** and navigate to the project:
   ```bash
   cd /mnt/c/Users/jahhe/Dropbox/Apps/Campspots
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Get Stripe API Keys:**
   - Go to https://dashboard.stripe.com/register
   - Create an account (or login)
   - Go to https://dashboard.stripe.com/test/apikeys
   - Copy both keys (starts with `sk_test_` and `pk_test_`)

4. **Edit .env file:**
   ```bash
   nano .env  # or use your preferred editor
   ```

   Add your Stripe keys:
   ```
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
   STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
   ```

5. **Run the application:**
   ```bash
   source venv/bin/activate
   python app.py
   ```

6. **Access the site:**
   - Public site: http://localhost:5000
   - Admin panel: http://localhost:5000/admin

### Option 2: Using Windows Python

If you have Python installed on Windows:

1. **Run the setup script:**
   ```cmd
   setup.bat
   ```

2. Follow steps 3-6 from Option 1 above

## Getting Stripe Test Keys

1. Go to https://stripe.com and create a free account
2. Navigate to Developers > API Keys
3. Use the **Test mode** keys (they start with `sk_test_` and `pk_test_`)
4. Copy both the Secret Key and Publishable Key
5. Add them to your `.env` file

**Important:** Never commit real API keys to git. The `.gitignore` file already excludes `.env`.

## Testing Stripe Payments

Use these test card numbers in Stripe test mode:

- **Success:** 4242 4242 4242 4242
- **Decline:** 4000 0000 0000 0002
- Use any future expiration date and any 3-digit CVC

## Customizing Site Data

### Update Campground Information

Edit `init_db.py` to customize:
- Campground descriptions
- Number of sites per campground
- Site types (RV, Tent, Cabin, etc.)
- Pricing per site
- Hookup information

Then reinitialize the database:
```bash
rm campspots.db  # Delete old database
python init_db.py  # Create new one
```

### Update Images

Replace placeholder images in `templates/index.html`:
- Current: `https://via.placeholder.com/...`
- Add your own images to `static/` folder
- Update image paths in templates

## Deployment to Production

When ready to deploy:

1. **Switch to PostgreSQL:**
   - Update DATABASE_URL in .env
   - Example: `postgresql://user:password@localhost/campspots`

2. **Use Production Stripe Keys:**
   - Get live keys from Stripe dashboard
   - They start with `sk_live_` and `pk_live_`

3. **Set SECRET_KEY:**
   - Generate a random secret: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Add to .env

4. **Add Authentication:**
   - Admin panel currently has no auth
   - Add Flask-Login or similar before going live

5. **Deploy to hosting:**
   - Options: Heroku, DigitalOcean, Railway, Render
   - Set environment variables in hosting dashboard
   - Use gunicorn: `pip install gunicorn`
   - Run: `gunicorn app:app`

## Troubleshooting

### "Database is locked"
- SQLite limitation with concurrent users
- Switch to PostgreSQL for production

### "Stripe key not found"
- Make sure .env file exists and has your keys
- Check that keys don't have quotes around them

### Port 5000 already in use
- Change port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill process using port 5000

### Images not loading
- Make sure `static/` folder exists
- Check browser console for errors
- Verify image paths in templates

## Next Steps

1. ✅ Set up Stripe account and get test keys
2. ✅ Customize campground data in `init_db.py`
3. ✅ Replace placeholder images with real photos
4. ✅ Test booking flow end-to-end
5. ✅ Review admin panel functionality
6. ✅ Add authentication to admin panel
7. ✅ Deploy to production hosting
8. ✅ Update DNS to point to your domain
9. ✅ Monitor reservations and payments
10. ✅ Plan migration to Campspot when ready

## Support

Questions? Contact the development team or refer to:
- Flask docs: https://flask.palletsprojects.com/
- Stripe docs: https://stripe.com/docs
- Bootstrap docs: https://getbootstrap.com/docs/
