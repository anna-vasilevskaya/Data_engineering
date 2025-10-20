#!/usr/bin/env python3

import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Successfully connected!")
        print(f"Database version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return False


def test_data():
    """Test data existence"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vasilevskaia;")
        result = cursor.fetchall()
        print(f"Data exists: {result}")
        cursor.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f"Error testing data: {e}")
        return False

if __name__ == "__main__":
    # environment variables
    required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing environment variables: {missing_vars}")
        print("Please set environment variables first")
        sys.exit(1)
    
    success = test_connection()
    success = test_data()
