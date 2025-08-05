import argparse
import csv
from datetime import datetime
from typing import List

from app import database
from app.crud import upsert_entity_by_name, upsert_vessel
from app.models import Document, DocumentCategory
from app.schemas import EntityCreate, VesselUpsert


def parse_args():
    parser = argparse.ArgumentParser(
        description='Load documents from CSV into the database'
    )
    parser.add_argument(
        '--path',
        type=str,
        default='documents.csv',
        help='Path to the CSV file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print what would be done without writing to DB'
    )
    return parser.parse_args()


def load_csv_data(path: str) -> List[dict]:
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def parse_category(value: str) -> DocumentCategory:
    """
    Normalize category strings and return matching DocumentCategory enum,
    using fuzzy matching if necessary.
    """
    raw = value.strip().lower()

    for category in DocumentCategory:
        if category.value.lower() == raw:
            return category

    valid_values = [cat.value for cat in DocumentCategory]
    closest = difflib.get_close_matches(value, valid_values, n=1, cutoff=0.6)

    if closest:
        match = closest[0]
        for category in DocumentCategory:
            if category.value == match:
                return category

    raise ValueError(
        f'Unknown category: {value}. Expected one of: {valid_values}')


def load_documents(args):
    data = load_csv_data(args.path)
    db = database.SessionLocal()

    created = 0
    skipped = 0
    skipped_rows = []

    for row in data:
        try:
            # Attempt to create/find vessel with minimal data
            vessel = upsert_vessel(
                db,
                VesselUpsert(
                    name=row['vessel'].strip(),
                    imo=int(row['imo']),
                ),
                commit=not args.dry_run,
            )

            provider = None
            provider_name = row.get('provider', '').strip()
            if provider_name and provider_name.lower() != 'any':
                provider = upsert_entity_by_name(
                    db,
                    EntityCreate(name=provider_name),
                    commit=not args.dry_run,
                )

            category = parse_category(row['category'])

            document = Document(
                filename=row['file'].strip(),
                vessel_id=vessel.id,
                provider_id=provider.id if provider else None,
                number=row.get('number') or None,
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                category=category,
            )

            if args.dry_run:
                print(f'[dry-run] Would insert document: {document.__dict__}')
            else:
                db.add(document)

            created += 1

        except Exception as e:
            skipped += 1
            skipped_rows.append({'row': row, 'reason': str(e)})

    if not args.dry_run:
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

    db.close()

    print(f'\nFinished processing {len(data)} rows')
    print(f'Created: {created}, Skipped: {skipped}')

    if skipped_rows:
        print('\nSkipped rows:')
        for entry in skipped_rows:
            print(f'  - Reason: {entry['reason']}\n    Row: {entry['row']}')


if __name__ == '__main__':
    args = parse_args()
    load_documents(args)
