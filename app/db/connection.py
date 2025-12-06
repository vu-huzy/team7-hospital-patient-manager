"""
Database connection module for Hospital Patient Manager
Provides connection pooling and configuration from environment variables
"""
import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """
    Create and return a new database connection using PyMySQL
    
    Returns:
        pymysql.connections.Connection: Database connection with DictCursor
    """
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "hospital_patient_manager"),
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4'
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def execute_query(query, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Helper function to execute queries with automatic connection management
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch_one: Return single row
        fetch_all: Return all rows
        commit: Commit transaction
        
    Returns:
        Query results or lastrowid for INSERT queries
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            
            if commit:
                connection.commit()
                return cursor.lastrowid
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            
    except pymysql.Error as e:
        if commit:
            connection.rollback()
        raise e
    finally:
        connection.close()
