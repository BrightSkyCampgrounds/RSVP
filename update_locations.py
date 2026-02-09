"""Update campground locations in database"""
from app import app, db
from models import Campground

def update_locations():
    """Update campground location information"""
    with app.app_context():
        # Update North Fork
        north_fork = Campground.query.filter_by(name='North Fork').first()
        if north_fork:
            north_fork.location = 'Rough River Lake, KY'
            print(f"Updated {north_fork.name} location to: {north_fork.location}")

        # Update Cave Creek
        cave_creek = Campground.query.filter_by(name='Cave Creek').first()
        if cave_creek:
            cave_creek.location = 'Rough River Lake, KY'
            print(f"Updated {cave_creek.name} location to: {cave_creek.location}")

        # Update Pikes Ridge
        pikes_ridge = Campground.query.filter_by(name='Pikes Ridge').first()
        if pikes_ridge:
            pikes_ridge.location = 'Green River Lake, KY'
            print(f"Updated {pikes_ridge.name} location to: {pikes_ridge.location}")

        db.session.commit()
        print("\n✅ All campground locations updated successfully!")


if __name__ == '__main__':
    update_locations()
