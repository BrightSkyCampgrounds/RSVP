import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///campspots.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Stripe Configuration
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

    # Site Configuration
    SITE_NAME = os.environ.get('SITE_NAME', 'Bright Sky Campgrounds')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'reservations@brightskycampgrounds.com')

    # Pricing (can be adjusted per site type later)
    DEFAULT_PRICE_PER_NIGHT = 35.00  # in dollars
