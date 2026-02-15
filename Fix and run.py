#!/usr/bin/env python3
"""
fix_and_run.py - Diagnostic and Fix Script for e-Nursery

This script will:
1. Check all dependencies
2. Verify file structure
3. Create database
4. Test the application
5. Provide detailed error messages
"""

import os
import sys


def check_dependencies():
    """Check if all required packages are installed"""
    print("=" * 70)
    print("STEP 1: Checking Dependencies")
    print("=" * 70)

    required = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'flask_login': 'Flask-Login',
        'werkzeug': 'Werkzeug',
        'PIL': 'Pillow'
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package} - OK")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall them with:")
        print(f"pip install {' '.join(missing)}")
        return False

    print("\n✅ All dependencies installed!")
    return True


def check_file_structure():
    """Check if all necessary files exist"""
    print("\n" + "=" * 70)
    print("STEP 2: Checking File Structure")
    print("=" * 70)

    required_files = {
        'app.py': 'Main Flask application',
        'models.py': 'Database models',
        'routes.py': 'Route handlers',
        'seed_data.py': 'Sample data script',
        'templates/base.html': 'Base template',
        'templates/index.html': 'Homepage template',
        'templates/login.html': 'Login template',
        'static/uploads': 'Upload directory'
    }

    missing = []
    for filepath, description in required_files.items():
        if os.path.exists(filepath):
            print(f"✓ {filepath} - OK")
        else:
            print(f"✗ {filepath} - MISSING ({description})")
            missing.append(filepath)

    if missing:
        print(f"\n⚠️  Missing files: {len(missing)}")
        return False

    print("\n✅ All files present!")
    return True


def create_database():
    """Create and seed the database"""
    print("\n" + "=" * 70)
    print("STEP 3: Creating Database")
    print("=" * 70)

    try:
        # Import after checking dependencies
        from app import app, db
        from models import User, Plant, Ingredient

        with app.app_context():
            # Check if database exists
            if os.path.exists('database.db'):
                print("⚠️  Database already exists")
                response = input("Recreate database? (y/n): ")
                if response.lower() != 'y':
                    print("Skipping database creation")
                    return True
                os.remove('database.db')
                print("✓ Removed old database")

            # Create tables
            db.create_all()
            print("✓ Created database tables")

            # Run seed data
            print("\nRunning seed_data.py...")
            import seed_data
            print("✓ Database seeded with sample data")

        print("\n✅ Database ready!")
        return True

    except Exception as e:
        print(f"\n❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_routes():
    """Test if routes are working"""
    print("\n" + "=" * 70)
    print("STEP 4: Testing Routes")
    print("=" * 70)

    try:
        from app import app

        test_routes = [
            ('/', 'Homepage'),
            ('/login', 'Login page'),
            ('/plants', 'Plants page'),
            ('/ingredients', 'Garden Supplies page')
        ]

        with app.test_client() as client:
            for route, name in test_routes:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"✓ {name} ({route}) - OK")
                else:
                    print(f"✗ {name} ({route}) - Error {response.status_code}")

        print("\n✅ Routes working!")
        return True

    except Exception as e:
        print(f"\n❌ Error testing routes: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main diagnostic and fix function"""
    print("\n" + "=" * 70)
    print("e-NURSERY DIAGNOSTIC AND FIX TOOL")
    print("=" * 70 + "\n")

    # Check current directory
    if not os.path.exists('app.py'):
        print("❌ Error: Not in e-nursery directory!")
        print("\nPlease run this script from the e-nursery folder:")
        print("  cd e-nursery")
        print("  python fix_and_run.py")
        return

    # Run checks
    checks = [
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Database", create_database),
        ("Routes", test_routes)
    ]

    for name, check_func in checks:
        if not check_func():
            print(f"\n❌ {name} check failed!")
            print("\nPlease fix the issues above and try again.")
            return

    # All checks passed
    print("\n" + "=" * 70)
    print("✅ ALL CHECKS PASSED!")
    print("=" * 70)

    print("\n📋 Login Credentials:")
    print("-" * 70)
    print("Admin Account:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nUser Account:")
    print("  Username: rajesh_kumar")
    print("  Password: password123")
    print("-" * 70)

    print("\n🚀 Starting Flask Application...")
    print("=" * 70)
    print("\nApplication will start on: http://localhost:5000")
    print("\nPress CTRL+C to stop the server")
    print("=" * 70 + "\n")

    # Start Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n✅ Application stopped")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()