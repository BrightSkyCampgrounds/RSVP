"""Export reservation data for Campspot migration"""
import csv
import json
import argparse
from datetime import datetime
from app import app, db
from models import Reservation, Site, Campground

def export_to_csv(filename='reservations_export.csv'):
    """Export all reservations to CSV format"""
    with app.app_context():
        reservations = Reservation.query.order_by(Reservation.created_at).all()

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'confirmation_code', 'campground', 'site_number', 'site_type',
                'customer_name', 'customer_email', 'customer_phone',
                'arrival_date', 'departure_date', 'num_nights',
                'num_occupants', 'num_vehicles', 'vehicle_info',
                'special_requests', 'total_amount', 'payment_status',
                'stripe_payment_id', 'status', 'created_at', 'created_by'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for res in reservations:
                writer.writerow({
                    'confirmation_code': res.confirmation_code,
                    'campground': res.site.campground.name,
                    'site_number': res.site.site_number,
                    'site_type': res.site.site_type,
                    'customer_name': res.customer_name,
                    'customer_email': res.customer_email,
                    'customer_phone': res.customer_phone,
                    'arrival_date': res.arrival_date.isoformat(),
                    'departure_date': res.departure_date.isoformat(),
                    'num_nights': res.num_nights,
                    'num_occupants': res.num_occupants,
                    'num_vehicles': res.num_vehicles,
                    'vehicle_info': res.vehicle_info or '',
                    'special_requests': res.special_requests or '',
                    'total_amount': res.total_amount,
                    'payment_status': res.payment_status,
                    'stripe_payment_id': res.stripe_payment_id or '',
                    'status': res.status,
                    'created_at': res.created_at.isoformat(),
                    'created_by': res.created_by
                })

        print(f"Exported {len(reservations)} reservations to {filename}")


def export_to_json(filename='reservations_export.json'):
    """Export all reservations to JSON format"""
    with app.app_context():
        reservations = Reservation.query.order_by(Reservation.created_at).all()

        data = {
            'export_date': datetime.now().isoformat(),
            'total_reservations': len(reservations),
            'reservations': []
        }

        for res in reservations:
            data['reservations'].append({
                'confirmation_code': res.confirmation_code,
                'campground': {
                    'name': res.site.campground.name,
                    'id': res.site.campground.id
                },
                'site': {
                    'number': res.site.site_number,
                    'type': res.site.site_type,
                    'hookups': res.site.hookups,
                    'price_per_night': res.site.price_per_night
                },
                'customer': {
                    'name': res.customer_name,
                    'email': res.customer_email,
                    'phone': res.customer_phone
                },
                'dates': {
                    'arrival': res.arrival_date.isoformat(),
                    'departure': res.departure_date.isoformat(),
                    'num_nights': res.num_nights
                },
                'details': {
                    'num_occupants': res.num_occupants,
                    'num_vehicles': res.num_vehicles,
                    'vehicle_info': res.vehicle_info,
                    'special_requests': res.special_requests
                },
                'payment': {
                    'total_amount': res.total_amount,
                    'payment_status': res.payment_status,
                    'stripe_payment_id': res.stripe_payment_id
                },
                'status': res.status,
                'metadata': {
                    'created_at': res.created_at.isoformat(),
                    'created_by': res.created_by
                }
            })

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)

        print(f"Exported {len(reservations)} reservations to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Export reservation data')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='csv',
                        help='Export format (default: csv)')
    parser.add_argument('--output', default='reservations_export',
                        help='Output filename (without extension)')

    args = parser.parse_args()

    if args.format in ['csv', 'both']:
        export_to_csv(f"{args.output}.csv")

    if args.format in ['json', 'both']:
        export_to_json(f"{args.output}.json")


if __name__ == '__main__':
    main()
