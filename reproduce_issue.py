import sys
import os

# Add current directory to sys.path just in case, though it should be there.
sys.path.append(os.getcwd())

try:
    print("Attempting to import from routes...")
    from routes import header_router, footer_router, home_router, api_router
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
