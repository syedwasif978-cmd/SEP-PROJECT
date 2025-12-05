#!/usr/bin/env python
"""Initialize the database with all required tables."""

import sys
import os

# Add backend directory to Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app, db

# Create all tables defined in models
with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")
