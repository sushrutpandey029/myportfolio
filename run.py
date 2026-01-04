"""
Application Entry Point
Main script to run the Flask application
- Loads environment variables
- Initializes Flask app
- Runs development server
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
import os

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from dotenv import load_dotenv

# =========================================
# ENVIRONMENT SETUP
# =========================================
# Load environment variables from .env file
load_dotenv()

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app import create_app

# =========================================
# APPLICATION INITIALIZATION
# =========================================
app = create_app()

# =========================================
# MAIN EXECUTION
# =========================================
if __name__ == '__main__':
    app.run(debug=True)