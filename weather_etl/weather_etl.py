#!/usr/bin/env python3
"""
Weather ETL Pipeline for Casablanca, Morocco
Extracts current and forecasted temperature data from wttr.in API
Transforms data to required format and loads to log file
"""

import requests
import json
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import logging
import os
import sys

# Configuration
CITY = "casablanca"
API_URL = f"https://wttr.in/{CITY}?format=j1"
LOG_FILE = "weather_data.log"
CSV_FILE = "weather_data.csv"
DB_FILE = "weather_data.db"
TABLE_NAME = "weather_reports"

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('weather_etl.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def log_progress(message):
    """Log progress messages"""
    logger = logging.getLogger(__name__)
    logger.info(message)

def extract_weather_data(url):
    """
    Extract weather data from wttr.in API
    
    Args:
        url (str): API endpoint URL
        
    Returns:
        dict: Raw weather data from API
    """
    log_progress(f"Extracting weather data from {url}")
    
    try:
        headers = {
            'User-Agent': 'Weather ETL Pipeline/1.0'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        log_progress("Weather data extracted successfully")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        log_progress(f"Error extracting weather data: {e}")
        raise
    except json.JSONDecodeError as e:
        log_progress(f"Error parsing JSON response: {e}")
        raise

def transform_weather_data(raw_data):
    """
    Transform raw weather data to required format
    
    Args:
        raw_data (dict): Raw weather data from API
        
    Returns:
        dict: Transformed weather data with current and forecast temperatures
    """
    log_progress("Transforming weather data")
    
    try:
        # Get current date
        today = date.today()
        
        # Extract current temperature (observed temperature)
        current_temp = int(raw_data['current_condition'][0]['temp_C'])
        log_progress(f"Current temperature: {current_temp}°C")
        
        # Extract tomorrow's forecast temperature at noon
        tomorrow_forecast = None
        
        # Look for tomorrow's data (should be weather[1] if today is weather[0])
        if len(raw_data['weather']) >= 2:
            tomorrow_data = raw_data['weather'][1]
            
            # Find noon forecast (time "1200")
            for hourly in tomorrow_data['hourly']:
                if hourly['time'] == '1200':  # Noon
                    tomorrow_forecast = int(hourly['tempC'])
                    break
            
            if tomorrow_forecast is None:
                # Fallback: use average temperature if noon not found
                tomorrow_forecast = int(tomorrow_data['avgtempC'])
                log_progress("Noon forecast not found, using average temperature")
        
        if tomorrow_forecast is None:
            raise ValueError("Could not extract tomorrow's forecast temperature")
        
        log_progress(f"Tomorrow's forecast temperature at noon: {tomorrow_forecast}°C")
        
        # Create transformed data
        transformed_data = {
            'year': today.year,
            'month': today.month,
            'day': today.day,
            'obs_tmp': current_temp,
            'fc_temp': tomorrow_forecast,
            'timestamp': datetime.now().isoformat()
        }
        
        log_progress("Weather data transformed successfully")
        return transformed_data
        
    except (KeyError, IndexError, ValueError) as e:
        log_progress(f"Error transforming weather data: {e}")
        raise

def load_to_csv(data, csv_path):
    """
    Load weather data to CSV file
    
    Args:
        data (dict): Transformed weather data
        csv_path (str): Path to CSV file
    """
    log_progress(f"Loading data to CSV: {csv_path}")
    
    # Create DataFrame
    df = pd.DataFrame([data])
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(csv_path)
    
    # Append to CSV file
    df[['year', 'month', 'day', 'obs_tmp', 'fc_temp']].to_csv(
        csv_path, 
        mode='a', 
        header=not file_exists, 
        index=False,
        sep='\t'  # Tab-separated for better readability
    )
    
    log_progress("Data loaded to CSV successfully")

def load_to_log(data, log_path):
    """
    Load weather data to tabular log file
    
    Args:
        data (dict): Transformed weather data
        log_path (str): Path to log file
    """
    log_progress(f"Loading data to log file: {log_path}")
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(log_path)
    
    with open(log_path, 'a') as f:
        if not file_exists:
            # Write header
            f.write("year\tmonth\tday\tobs_tmp\tfc_temp\n")
        
        # Write data row
        f.write(f"{data['year']}\t{data['month']}\t{data['day']}\t{data['obs_tmp']}\t{data['fc_temp']}\n")
    
    log_progress("Data loaded to log file successfully")

def load_to_db(data, db_path, table_name):
    """
    Load weather data to SQLite database
    
    Args:
        data (dict): Transformed weather data
        db_path (str): Path to SQLite database
        table_name (str): Name of database table
    """
    log_progress(f"Loading data to database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Create table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL,
            obs_tmp INTEGER NOT NULL,
            fc_temp INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            UNIQUE(year, month, day)
        )
        """
        conn.execute(create_table_query)
        
        # Insert data (or replace if date already exists)
        insert_query = f"""
        INSERT OR REPLACE INTO {table_name} 
        (year, month, day, obs_tmp, fc_temp, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        conn.execute(insert_query, (
            data['year'], data['month'], data['day'],
            data['obs_tmp'], data['fc_temp'], data['timestamp']
        ))
        
        conn.commit()
        conn.close()
        
        log_progress("Data loaded to database successfully")
        
    except sqlite3.Error as e:
        log_progress(f"Database error: {e}")
        raise

def run_query(query, db_path):
    """
    Run a SQL query and return results
    
    Args:
        query (str): SQL query to execute
        db_path (str): Path to SQLite database
        
    Returns:
        list: Query results
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        log_progress(f"Query error: {e}")
        raise

def display_recent_data(db_path, table_name, limit=10):
    """
    Display recent weather data from database
    
    Args:
        db_path (str): Path to SQLite database
        table_name (str): Name of database table
        limit (int): Number of recent records to show
    """
    log_progress(f"Displaying last {limit} weather records")
    
    query = f"""
    SELECT year, month, day, obs_tmp, fc_temp, timestamp 
    FROM {table_name} 
    ORDER BY year DESC, month DESC, day DESC 
    LIMIT {limit}
    """
    
    results = run_query(query, db_path)
    
    print(f"\n{'='*70}")
    print(f"RECENT WEATHER DATA FOR CASABLANCA (Last {limit} records)")
    print(f"{'='*70}")
    print(f"{'Year':<6} {'Month':<6} {'Day':<4} {'Obs°C':<6} {'Fcst°C':<7} {'Timestamp':<20}")
    print(f"{'-'*70}")
    
    for row in results:
        year, month, day, obs_tmp, fc_temp, timestamp = row
        timestamp_short = timestamp.split('T')[0]  # Just the date part
        print(f"{year:<6} {month:<6} {day:<4} {obs_tmp:<6} {fc_temp:<7} {timestamp_short:<20}")
    
    print(f"{'='*70}\n")

def main():
    """Main ETL pipeline execution"""
    
    # Setup logging
    logger = setup_logging()
    
    log_progress("=" * 60)
    log_progress("WEATHER ETL PIPELINE STARTED")
    log_progress("=" * 60)
    log_progress(f"Target city: {CITY.title()}")
    log_progress(f"Date: {date.today()}")
    log_progress(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # Extract
        raw_data = extract_weather_data(API_URL)
        
        # Transform
        weather_data = transform_weather_data(raw_data)
        
        # Load
        load_to_log(weather_data, LOG_FILE)
        load_to_csv(weather_data, CSV_FILE)
        load_to_db(weather_data, DB_FILE, TABLE_NAME)
        
        # Display results
        print("\n🌤️  WEATHER ETL RESULTS")
        print(f"Date: {weather_data['year']}-{weather_data['month']:02d}-{weather_data['day']:02d}")
        print(f"Current Temperature: {weather_data['obs_tmp']}°C")
        print(f"Tomorrow's Forecast (noon): {weather_data['fc_temp']}°C")
        
        # Show recent data from database
        if os.path.exists(DB_FILE):
            display_recent_data(DB_FILE, TABLE_NAME, limit=5)
        
        log_progress("=" * 60)
        log_progress("WEATHER ETL PIPELINE COMPLETED SUCCESSFULLY")
        log_progress("=" * 60)
        
    except Exception as e:
        log_progress(f"PIPELINE FAILED: {e}")
        raise

if __name__ == "__main__":
    main() 