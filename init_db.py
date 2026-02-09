"""Initialize the database with campgrounds and sites"""
from app import app, db
from models import Campground, Site

def init_database():
    """Create tables and populate with initial data"""
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if data already exists
        try:
            if Campground.query.first():
                print("Database already initialized. Skipping.")
                return
        except Exception as e:
            print(f"Error checking database: {e}")
            print("Continuing with initialization...")

        print("Initializing database...")

        # Create the three campgrounds
        campgrounds_data = [
            {
                'name': 'North Fork',
                'description': 'Scenic campground along the North Fork.',
                'location': 'USACE Lease Location'
            },
            {
                'name': 'Cave Creek',
                'description': 'Beautiful campground near Cave Creek.',
                'location': 'USACE Lease Location'
            },
            {
                'name': 'Pikes Ridge',
                'description': 'Mountain campground at Pikes Ridge.',
                'location': 'USACE Lease Location'
            }
        ]

        for cg_data in campgrounds_data:
            campground = Campground(**cg_data)
            db.session.add(campground)
            db.session.flush()  # Get the ID

            # Add sample sites for each campground
            # TODO: Replace with actual site data
            for i in range(1, 21):  # 20 sites per campground as placeholder
                site = Site(
                    campground_id=campground.id,
                    site_number=f"{i:03d}",
                    site_type="RV" if i <= 15 else "Tent",
                    max_occupancy=6 if i <= 15 else 4,
                    max_vehicles=2,
                    hookups="Electric, Water, Sewer" if i <= 10 else "Electric, Water" if i <= 15 else "None",
                    price_per_night=45.00 if i <= 10 else 35.00 if i <= 15 else 25.00,
                    active=True
                )
                db.session.add(site)

            print(f"Created campground: {campground.name} with 20 sites")

        db.session.commit()
        print("Database initialization complete!")
        print("\nCampgrounds created:")
        for cg in Campground.query.all():
            print(f"  - {cg.name}: {cg.sites.count()} sites")


if __name__ == '__main__':
    init_database()
