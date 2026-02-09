from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Campground(db.Model):
    """Represents a campground location"""
    __tablename__ = 'campgrounds'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sites = db.relationship('Site', backref='campground', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Campground {self.name}>'


class Site(db.Model):
    """Represents a campsite within a campground"""
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    campground_id = db.Column(db.Integer, db.ForeignKey('campgrounds.id'), nullable=False)
    site_number = db.Column(db.String(20), nullable=False)
    site_type = db.Column(db.String(50), nullable=False)  # RV, Tent, Cabin, etc.
    max_occupancy = db.Column(db.Integer, default=6)
    max_vehicles = db.Column(db.Integer, default=2)
    hookups = db.Column(db.String(100))  # e.g., "Electric, Water, Sewer"
    price_per_night = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship('Reservation', backref='site', lazy=True)

    def __repr__(self):
        return f'<Site {self.campground.name} - {self.site_number}>'

    def is_available(self, arrival_date, departure_date):
        """Check if site is available for given date range"""
        overlapping = Reservation.query.filter(
            Reservation.site_id == self.id,
            Reservation.status.in_(['pending', 'confirmed']),
            Reservation.arrival_date < departure_date,
            Reservation.departure_date > arrival_date
        ).first()
        return overlapping is None


class Reservation(db.Model):
    """Represents a campsite reservation"""
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)

    # Customer Information
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=False)

    # Reservation Details
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    num_nights = db.Column(db.Integer, nullable=False)
    num_occupants = db.Column(db.Integer, nullable=False)
    num_vehicles = db.Column(db.Integer, nullable=False)
    vehicle_info = db.Column(db.Text)  # Size, type, license plates, etc.
    special_requests = db.Column(db.Text)

    # Payment Information
    total_amount = db.Column(db.Float, nullable=False)
    stripe_payment_id = db.Column(db.String(200))
    stripe_session_id = db.Column(db.String(200))
    payment_status = db.Column(db.String(50), default='pending')  # pending, paid, refunded, failed

    # Status
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, cancelled, completed

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100), default='customer')  # customer, admin, phone
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Reservation {self.id} - {self.customer_name}>'

    @property
    def confirmation_code(self):
        """Generate a simple confirmation code"""
        return f"BS{self.id:06d}"


class BlockedDate(db.Model):
    """Represents dates when sites are blocked for maintenance or special events"""
    __tablename__ = 'blocked_dates'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=True)  # None = all sites
    campground_id = db.Column(db.Integer, db.ForeignKey('campgrounds.id'), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlockedDate {self.start_date} to {self.end_date}>'
