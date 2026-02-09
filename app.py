"""Main Flask application for Campspots interim reservation system"""
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import stripe

from config import Config
from models import db, Campground, Site, Reservation, BlockedDate

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Configure Stripe
stripe.api_key = app.config['STRIPE_SECRET_KEY']


# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Landing page"""
    campgrounds = Campground.query.filter_by(active=True).all()
    return render_template('index.html', campgrounds=campgrounds)


@app.route('/availability')
def availability():
    """Show availability calendar/table"""
    campground_id = request.args.get('campground', type=int)

    campgrounds = Campground.query.filter_by(active=True).all()
    selected_campground = None
    sites = []

    if campground_id:
        selected_campground = Campground.query.get_or_404(campground_id)
        sites = Site.query.filter_by(campground_id=campground_id, active=True).all()

    return render_template(
        'availability.html',
        campgrounds=campgrounds,
        selected_campground=selected_campground,
        sites=sites
    )


@app.route('/api/check-availability')
def api_check_availability():
    """API endpoint to check site availability for date range"""
    site_id = request.args.get('site_id', type=int)
    arrival = request.args.get('arrival')
    departure = request.args.get('departure')

    if not all([site_id, arrival, departure]):
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        arrival_date = datetime.strptime(arrival, '%Y-%m-%d').date()
        departure_date = datetime.strptime(departure, '%Y-%m-%d').date()

        if arrival_date >= departure_date:
            return jsonify({'available': False, 'error': 'Departure must be after arrival'}), 400

        if arrival_date < datetime.now().date():
            return jsonify({'available': False, 'error': 'Cannot book dates in the past'}), 400

        site = Site.query.get_or_404(site_id)
        is_available = site.is_available(arrival_date, departure_date)

        num_nights = (departure_date - arrival_date).days
        total_price = site.price_per_night * num_nights

        return jsonify({
            'available': is_available,
            'num_nights': num_nights,
            'price_per_night': site.price_per_night,
            'total_price': total_price
        })

    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400


@app.route('/book/<int:site_id>', methods=['GET', 'POST'])
def book(site_id):
    """Booking form for a specific site"""
    site = Site.query.get_or_404(site_id)

    if request.method == 'POST':
        # Get form data
        arrival = request.form.get('arrival')
        departure = request.form.get('departure')
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        num_occupants = request.form.get('num_occupants', type=int)
        num_vehicles = request.form.get('num_vehicles', type=int)
        vehicle_info = request.form.get('vehicle_info', '')
        special_requests = request.form.get('special_requests', '')

        try:
            arrival_date = datetime.strptime(arrival, '%Y-%m-%d').date()
            departure_date = datetime.strptime(departure, '%Y-%m-%d').date()

            # Validate dates
            if arrival_date >= departure_date:
                flash('Departure date must be after arrival date.', 'error')
                return redirect(url_for('book', site_id=site_id))

            if arrival_date < datetime.now().date():
                flash('Cannot book dates in the past.', 'error')
                return redirect(url_for('book', site_id=site_id))

            # Check availability
            if not site.is_available(arrival_date, departure_date):
                flash('Sorry, this site is not available for the selected dates.', 'error')
                return redirect(url_for('availability'))

            # Calculate total
            num_nights = (departure_date - arrival_date).days
            total_amount = site.price_per_night * num_nights

            # Create reservation (pending payment)
            reservation = Reservation(
                site_id=site.id,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                arrival_date=arrival_date,
                departure_date=departure_date,
                num_nights=num_nights,
                num_occupants=num_occupants,
                num_vehicles=num_vehicles,
                vehicle_info=vehicle_info,
                special_requests=special_requests,
                total_amount=total_amount,
                status='pending',
                payment_status='pending'
            )

            db.session.add(reservation)
            db.session.commit()

            # Create Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(total_amount * 100),  # Convert to cents
                        'product_data': {
                            'name': f'{site.campground.name} - Site {site.site_number}',
                            'description': f'{num_nights} nights: {arrival} to {departure}',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=url_for('payment_success', reservation_id=reservation.id, _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_cancel', reservation_id=reservation.id, _external=True),
                customer_email=customer_email,
                metadata={
                    'reservation_id': reservation.id
                }
            )

            # Update reservation with Stripe session ID
            reservation.stripe_session_id = checkout_session.id
            db.session.commit()

            # Redirect to Stripe Checkout
            return redirect(checkout_session.url, code=303)

        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('book', site_id=site_id))

    # GET request - show booking form
    arrival = request.args.get('arrival', '')
    departure = request.args.get('departure', '')

    return render_template('book.html', site=site, arrival=arrival, departure=departure)


@app.route('/payment/success/<int:reservation_id>')
def payment_success(reservation_id):
    """Handle successful payment"""
    session_id = request.args.get('session_id')

    reservation = Reservation.query.get_or_404(reservation_id)

    # Verify payment with Stripe
    if session_id:
        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)

            if checkout_session.payment_status == 'paid':
                reservation.payment_status = 'paid'
                reservation.status = 'confirmed'
                reservation.stripe_payment_id = checkout_session.payment_intent
                db.session.commit()

                return render_template('confirmation.html', reservation=reservation)

        except Exception as e:
            app.logger.error(f"Error verifying payment: {str(e)}")
            flash('Payment verification failed. Please contact us.', 'error')

    return redirect(url_for('index'))


@app.route('/payment/cancel/<int:reservation_id>')
def payment_cancel(reservation_id):
    """Handle cancelled payment"""
    reservation = Reservation.query.get_or_404(reservation_id)

    # Update reservation status
    reservation.payment_status = 'cancelled'
    reservation.status = 'cancelled'
    db.session.commit()

    flash('Payment was cancelled. Your reservation was not completed.', 'warning')
    return redirect(url_for('availability'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')

        # Check password against environment variable
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Default for development

        if password == admin_password:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password. Please try again.', 'error')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard - simple authentication would be needed for production"""
    # TODO: Add proper authentication

    total_reservations = Reservation.query.count()
    confirmed_reservations = Reservation.query.filter_by(status='confirmed').count()
    pending_reservations = Reservation.query.filter_by(status='pending').count()

    recent_reservations = Reservation.query.order_by(
        Reservation.created_at.desc()
    ).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        total_reservations=total_reservations,
        confirmed_reservations=confirmed_reservations,
        pending_reservations=pending_reservations,
        recent_reservations=recent_reservations
    )


@app.route('/admin/reservations')
@admin_required
def admin_reservations():
    """View all reservations"""
    # TODO: Add proper authentication

    campground_id = request.args.get('campground', type=int)
    status = request.args.get('status')

    query = Reservation.query

    if campground_id:
        query = query.join(Site).filter(Site.campground_id == campground_id)

    if status:
        query = query.filter(Reservation.status == status)

    reservations = query.order_by(Reservation.arrival_date.desc()).all()
    campgrounds = Campground.query.all()

    return render_template(
        'admin/reservations.html',
        reservations=reservations,
        campgrounds=campgrounds,
        selected_campground=campground_id,
        selected_status=status
    )


@app.template_filter('currency')
def currency_filter(value):
    """Format value as currency"""
    return f"${value:,.2f}"


@app.context_processor
def inject_globals():
    """Inject global variables into templates"""
    return {
        'site_name': app.config['SITE_NAME'],
        'stripe_publishable_key': app.config['STRIPE_PUBLISHABLE_KEY'],
        'now': datetime.now,
        'timedelta': timedelta
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
