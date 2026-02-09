# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Campspots** is an interim reservation system for Bright Sky Campgrounds, managing three USACE campground leases: **North Fork**, **Cave Creek**, and **Pikes Ridge**. This is a temporary solution deployed quickly to handle immediate reservation demand while the permanent Campspot management software is being prepared.

**Critical Context:**
- Press release went out Thursday for North Fork - already 20+ inquiries
- Need to deploy ASAP with minimal viable functionality
- Must support easy data migration to Campspot when ready
- Public-facing site should include disclaimer about revamped version coming soon

## Business Context

**Brand:** Bright Sky Campgrounds
**Contact Channels:**
- Email: reservations@brightskycampgrounds.com
- Dedicated phone line (handled by campground operations manager)
- Website: Basic landing page with inquiry form (currently sends to work email)

**Parent Organization:** Part of Common Capital RE Holdings portfolio (see parent CLAUDE.md at `C:\Users\jahhe\Dropbox\CLAUDE.md`)

## Core Requirements

**Functionality:**
1. Display sites vs. available dates (table/calendar view)
2. Allow customers to select sites and dates
3. Capture essential reservation data
4. Process payments online via Stripe (online-only at this time)
5. Export reservation data for Campspot migration

**Required Data Fields:**
- Contact info (name, email, phone)
- Arrival and departure dates
- Vehicle information (size, number of vehicles)
- Number of occupants
- Any special requirements or notes
- Payment/booking confirmation

## Architecture

This is intentionally a simple, straightforward web application prioritizing speed of deployment over sophisticated architecture.

**Technology Stack:**
- **Backend:** Python with Flask or FastAPI
- **Database:** SQLite for development, PostgreSQL for production
- **Payments:** Stripe API
- **Frontend:** Simple HTML/CSS/JS (Bootstrap or similar for quick responsive design)
- **Deployment:** Simple hosting solution (consider Heroku, DigitalOcean, or similar)

**Key Design Principles:**
- Simple, not over-engineered - this is temporary
- Data structure compatible with Campspot import (research their data model)
- Clear separation between campgrounds (North Fork, Cave Creek, Pikes Ridge)
- Easy to export all data as CSV/JSON for migration

## Development Commands

*Note: These will be added as the project structure is established*

**Initial Setup:**
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

**Run Development Server:**
```bash
python app.py  # or flask run / uvicorn main:app --reload
```

**Database:**
```bash
# Initialize database
python init_db.py

# Run migrations (if using Alembic/similar)
alembic upgrade head
```

**Export Data:**
```bash
# Export all reservations for Campspot migration
python export_data.py --format csv --output reservations_export.csv
```

## Database Schema Considerations

**Campgrounds Table:**
- id, name (North Fork, Cave Creek, Pikes Ridge), location, total_sites

**Sites Table:**
- id, campground_id, site_number, site_type (RV, tent, cabin, etc.), max_occupancy, hookups (electric/water/sewer)

**Reservations Table:**
- id, site_id, customer info (name, email, phone), arrival_date, departure_date, num_vehicles, vehicle_sizes, num_occupants, special_requests, total_amount, payment_status, stripe_payment_id, created_at

**Availability Logic:**
- Block out dates when sites are reserved
- Show real-time availability in table/calendar view
- Prevent double-booking

## Payment Integration

**Stripe Setup:**
- Use Stripe Checkout or Payment Intents API
- Store API keys in `.env` file (never commit)
- Capture payment before confirming reservation
- Store Stripe payment ID with reservation for reconciliation
- Consider refund policy and implementation

## Data Migration Strategy

**Export Requirements:**
- All reservation data must be exportable to CSV/JSON
- Research Campspot's data import format/API early
- Include mapping documentation from interim schema to Campspot schema
- Test migration process before Campspot goes live

## Environment Variables

Store in `.env` file (see `.env.example` for template):
```
STRIPE_SECRET_KEY=sk_...
STRIPE_PUBLISHABLE_KEY=pk_...
DATABASE_URL=postgresql://...
SECRET_KEY=...
ADMIN_EMAIL=reservations@brightskycampgrounds.com
```

## Deployment Checklist

- [ ] Set up production database
- [ ] Configure Stripe production keys
- [ ] Set up SSL certificate
- [ ] Configure email notifications (confirmation emails)
- [ ] Add disclaimer banner about temporary site/revamped version coming
- [ ] Test payment flow end-to-end
- [ ] Set up basic monitoring/error logging
- [ ] Document admin access for operations manager

## Admin Features Needed

- View all reservations by date range
- View reservations by campground
- Manual reservation entry (for phone bookings)
- Cancel/modify reservations
- Export data for accounting/reporting
- Block out dates for maintenance or special events

## Integration with Existing Systems

**Email:** Consider integrating with existing Gmail automation patterns (see `Apps/Billing Email Processor/` for examples) to:
- Send confirmation emails
- Process inquiries from reservations@brightskycampgrounds.com
- Forward notifications to operations manager

**Future:** When Campspot is ready, this system becomes read-only for historical data access while new bookings flow through Campspot.

## Important Notes

- **Time-Sensitive:** This needs to work quickly, not be perfect
- **Temporary Solution:** Plan for deprecation from day one
- **Data Integrity:** Prioritize accurate reservation data for smooth Campspot migration
- **Payment Security:** Follow Stripe best practices, never store card details locally
- **Dropbox Sync:** This directory syncs via Dropbox - be cautious with credential files to avoid conflicted copies
