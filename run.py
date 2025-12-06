#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask Application Entry Point
Run this file to start the web server
"""

from app.ui import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("HOSPITAL PATIENT MANAGER - WEB APPLICATION")
    print("="*60)
    print("Starting Flask development server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("="*60 + "\n")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
