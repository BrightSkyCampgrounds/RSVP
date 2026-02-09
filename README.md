# Campspots - Interim Reservation System

Temporary reservation system for Bright Sky Campgrounds (North Fork, Cave Creek, and Pikes Ridge).

## Quick Start

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Stripe keys
   ```

3. **Initialize database:**
   ```bash
   python init_db.py
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the site:**
   - Public site: http://localhost:5000
   - Admin dashboard: http://localhost:5000/admin

## Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your API keys from https://dashboard.stripe.com/test/apikeys
3. Add keys to `.env` file:
   - `STRIPE_SECRET_KEY` - starts with `sk_test_`
   - `STRIPE_PUBLISHABLE_KEY` - starts with `pk_test_`

## Exporting Data

When ready to migrate to Campspot:

```bash
# Export as CSV
python export_data.py --format csv --output migration_data

# Export as JSON
python export_data.py --format json --output migration_data

# Export both formats
python export_data.py --format both --output migration_data
```

## Project Structure

- `app.py` - Main Flask application
- `models.py` - Database models
- `config.py` - Configuration
- `templates/` - HTML templates
- `static/` - CSS, JS, images
- `init_db.py` - Database initialization
- `export_data.py` - Data export utility

## Notes

- This is a temporary solution - plan for Campspot migration
- No authentication on admin panel yet (add before production)
- Uses SQLite by default (switch to PostgreSQL for production)
- Remember to set SECRET_KEY in production

## Support

For questions: reservations@brightskycampgrounds.com
