#!/usr/bin/env python3
"""
Agent Arthritis Backend Server
Run this script to start the FastAPI server
"""
import uvicorn
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.seed_data import create_default_exercises

def main():
    """Main function to start the server"""
    print("🚀 Starting Agent Arthritis Backend Server...")
    
    # Create default exercises if database is empty
    print("📝 Checking for default exercises...")
    create_default_exercises()
    
    # Start the server
    print("🌐 Starting FastAPI server on http://0.0.0.0:8000")
    print("📚 API Documentation available at http://0.0.0.0:8000/docs")
    print("🔄 Interactive API docs at http://0.0.0.0:8000/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()