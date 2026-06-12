"""Setup script to initialize and seed the database."""

from db import init_db, seed_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("\nSeeding database with sample data...")
    seed_db()
    print("\nSetup complete! Run 'flask --app app.py run' to start the server.")

