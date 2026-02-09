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

        print("Initializing database with real campground data...")

        # ===== NORTH FORK (81 sites) =====
        north_fork = Campground(
            name='North Fork',
            description='Scenic campground along the North Fork with 81 sites including electric and primitive camping.',
            location='Rough River Lake, KY'
        )
        db.session.add(north_fork)
        db.session.flush()

        # North Fork: Sites 1-48, 81 are electric
        for i in range(1, 49):
            is_multi_family = i in [18, 19, 24, 25, 47, 48]
            is_long_term = 26 <= i <= 32

            notes = []
            if is_multi_family:
                notes.append("Multi-family site")
            if is_long_term:
                notes.append("Long-term camping available")

            site = Site(
                campground_id=north_fork.id,
                site_number=str(i),
                site_type="RV - Electric",
                max_occupancy=12 if is_multi_family else 6,
                max_vehicles=4 if is_multi_family else 2,
                hookups="Electric",
                price_per_night=35.00,
                active=True,
                notes=" | ".join(notes) if notes else None
            )
            db.session.add(site)

        # North Fork: Sites 49-80 are primitive
        for i in range(49, 81):
            site = Site(
                campground_id=north_fork.id,
                site_number=str(i),
                site_type="Primitive",
                max_occupancy=6,
                max_vehicles=2,
                hookups="None",
                price_per_night=25.00,
                active=True
            )
            db.session.add(site)

        # North Fork: Site 81 is electric and handicap accessible
        site = Site(
            campground_id=north_fork.id,
            site_number="81",
            site_type="RV - Electric",
            max_occupancy=6,
            max_vehicles=2,
            hookups="Electric",
            price_per_night=35.00,
            active=True,
            notes="Handicap accessible"
        )
        db.session.add(site)

        print(f"Created campground: {north_fork.name} with 81 sites")

        # ===== CAVE CREEK (65 sites) =====
        cave_creek = Campground(
            name='Cave Creek',
            description='Beautiful campground near Cave Creek with 65 sites including electric, primitive, and walk-in tent sites.',
            location='Rough River Lake, KY'
        )
        db.session.add(cave_creek)
        db.session.flush()

        # Cave Creek: Sites 1-37 are electric
        for i in range(1, 38):
            is_pull_thru = i in [7, 37]
            is_multi_family = i in [21, 22, 25, 26]
            is_long_term = 1 <= i <= 13
            is_handicap = i == 28

            notes = []
            if is_pull_thru:
                notes.append("Pull-thru site")
            if is_multi_family:
                notes.append("Multi-family site")
            if is_long_term:
                notes.append("Long-term camping available")
            if is_handicap:
                notes.append("Handicap accessible")

            site = Site(
                campground_id=cave_creek.id,
                site_number=str(i),
                site_type="RV - Electric" + (" Pull-thru" if is_pull_thru else ""),
                max_occupancy=12 if is_multi_family else 6,
                max_vehicles=4 if is_multi_family else 2,
                hookups="Electric",
                price_per_night=35.00,
                active=True,
                notes=" | ".join(notes) if notes else None
            )
            db.session.add(site)

        # Cave Creek: Sites 38-48 are primitive
        for i in range(38, 49):
            is_pull_thru = i in [43, 45]

            site = Site(
                campground_id=cave_creek.id,
                site_number=str(i),
                site_type="Primitive" + (" Pull-thru" if is_pull_thru else ""),
                max_occupancy=6,
                max_vehicles=2,
                hookups="None",
                price_per_night=25.00,
                active=True,
                notes="Pull-thru site" if is_pull_thru else None
            )
            db.session.add(site)

        # Cave Creek: Sites 49-60 are electric
        for i in range(49, 61):
            is_pull_thru = i in [49, 53, 56]

            site = Site(
                campground_id=cave_creek.id,
                site_number=str(i),
                site_type="RV - Electric" + (" Pull-thru" if is_pull_thru else ""),
                max_occupancy=6,
                max_vehicles=2,
                hookups="Electric",
                price_per_night=35.00,
                active=True,
                notes="Pull-thru site" if is_pull_thru else None
            )
            db.session.add(site)

        # Cave Creek: Sites 61-65 are walk-in tent sites
        for i in range(61, 66):
            site = Site(
                campground_id=cave_creek.id,
                site_number=str(i),
                site_type="Walk-in Tent",
                max_occupancy=6,
                max_vehicles=1,
                hookups="None",
                price_per_night=20.00,
                active=True,
                notes="Walk-in tent site - parking nearby"
            )
            db.session.add(site)

        print(f"Created campground: {cave_creek.name} with 65 sites")

        # ===== PIKES RIDGE (60 sites) =====
        pikes_ridge = Campground(
            name='Pikes Ridge',
            description='Mountain campground at Pikes Ridge with 60 sites offering electric and non-electric camping.',
            location='Green River Lake, KY'
        )
        db.session.add(pikes_ridge)
        db.session.flush()

        # Pikes Ridge: Sites 1-20 are electric
        for i in range(1, 21):
            site = Site(
                campground_id=pikes_ridge.id,
                site_number=str(i),
                site_type="RV - Electric",
                max_occupancy=6,
                max_vehicles=2,
                hookups="Electric",
                price_per_night=35.00,
                active=True
            )
            db.session.add(site)

        # Pikes Ridge: Sites 21-27 are non-electric
        for i in range(21, 28):
            site = Site(
                campground_id=pikes_ridge.id,
                site_number=str(i),
                site_type="Non-electric",
                max_occupancy=6,
                max_vehicles=2,
                hookups="None",
                price_per_night=25.00,
                active=True
            )
            db.session.add(site)

        # Pikes Ridge: Sites 28-29 are handicap accessible non-electric
        for i in [28, 29]:
            site = Site(
                campground_id=pikes_ridge.id,
                site_number=str(i),
                site_type="Non-electric",
                max_occupancy=6,
                max_vehicles=2,
                hookups="None",
                price_per_night=25.00,
                active=True,
                notes="Handicap accessible"
            )
            db.session.add(site)

        # Pikes Ridge: Sites 30-51 are non-electric
        for i in range(30, 52):
            site = Site(
                campground_id=pikes_ridge.id,
                site_number=str(i),
                site_type="Non-electric",
                max_occupancy=6,
                max_vehicles=2,
                hookups="None",
                price_per_night=25.00,
                active=True
            )
            db.session.add(site)

        # Pikes Ridge: Site 52 is handicap accessible non-electric
        site = Site(
            campground_id=pikes_ridge.id,
            site_number="52",
            site_type="Non-electric",
            max_occupancy=6,
            max_vehicles=2,
            hookups="None",
            price_per_night=25.00,
            active=True,
            notes="Handicap accessible"
        )
        db.session.add(site)

        # Pikes Ridge: Sites 53-60 are non-electric
        for i in range(53, 61):
            site = Site(
                campground_id=pikes_ridge.id,
                site_number=str(i),
                site_type="Non-electric",
                max_occupancy=6,
                max_vehicles=2,
                hookups="None",
                price_per_night=25.00,
                active=True
            )
            db.session.add(site)

        print(f"Created campground: {pikes_ridge.name} with 60 sites")

        db.session.commit()
        print("\n" + "="*60)
        print("Database initialization complete!")
        print("="*60)
        print("\nCampgrounds created:")
        for cg in Campground.query.all():
            site_count = Site.query.filter_by(campground_id=cg.id).count()
            print(f"  - {cg.name}: {site_count} sites")

        total_sites = Site.query.count()
        print(f"\n  TOTAL: {total_sites} sites across all campgrounds")
        print("="*60)


if __name__ == '__main__':
    init_database()
