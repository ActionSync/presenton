#!/usr/bin/env python
"""
Test script to verify Cloud SQL connection.
Run with: python test_db_connection.py
"""

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from utils.db_utils import get_database_url_and_connect_args


async def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    # Get connection details
    database_url, connect_args = get_database_url_and_connect_args()
    print(f"Database URL: {database_url.split('@')[0]}@...{database_url.split('@')[-1]}")
    print(f"Connect args: {connect_args}")
    
    try:
        # Create engine
        engine = create_async_engine(database_url, connect_args=connect_args)
        
        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            print("✅ Database connection successful!")
            print(f"Server response: {result.fetchone()}")
            
    except Exception as e:
        print(f"❌ Connection failed: {type(e).__name__}: {e}")
        return False
    finally:
        await engine.dispose()
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)
