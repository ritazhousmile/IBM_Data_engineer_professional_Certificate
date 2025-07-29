#!/usr/bin/env python3
"""
Script to run SQL queries on the banks database and show complete output
"""

import sqlite3
import pandas as pd

def run_sql_queries():
    """Run various SQL queries on the banks database"""
    
    database_name = 'banks.db'
    table_name = 'largest_banks'
    
    print("=== BANKS DATABASE SQL QUERIES ===\n")
    
    try:
        # Connect to database
        conn = sqlite3.connect(database_name)
        print(f"✅ Connected to database: {database_name}")
        
        # Query 1: Show all data
        print(f"\n🗄️  QUERY 1: SELECT * FROM {table_name}")
        print("=" * 80)
        query1 = f"SELECT * FROM {table_name}"
        df1 = pd.read_sql_query(query1, conn)
        print(df1.to_string(index=False))
        
        # Query 2: Count total records
        print(f"\n📊 QUERY 2: SELECT COUNT(*) FROM {table_name}")
        print("=" * 50)
        query2 = f"SELECT COUNT(*) as Total_Banks FROM {table_name}"
        df2 = pd.read_sql_query(query2, conn)
        print(df2.to_string(index=False))
        
        # Query 3: Top 5 banks by USD Market Cap
        print(f"\n🏆 QUERY 3: TOP 5 BANKS BY USD MARKET CAP")
        print("=" * 60)
        query3 = f"""
        SELECT Name, Market_Cap_USD_billion 
        FROM {table_name} 
        ORDER BY Market_Cap_USD_billion DESC 
        LIMIT 5
        """
        df3 = pd.read_sql_query(query3, conn)
        print(df3.to_string(index=False))
        
        # Query 4: Banks with Market Cap > 200B USD
        print(f"\n💰 QUERY 4: BANKS WITH MARKET CAP > $200B USD")
        print("=" * 60)
        query4 = f"""
        SELECT Name, Market_Cap_USD_billion 
        FROM {table_name} 
        WHERE Market_Cap_USD_billion > 200
        ORDER BY Market_Cap_USD_billion DESC
        """
        df4 = pd.read_sql_query(query4, conn)
        print(df4.to_string(index=False))
        
        # Query 5: Average Market Cap by currency
        print(f"\n📈 QUERY 5: AVERAGE MARKET CAP BY CURRENCY")
        print("=" * 60)
        query5 = f"""
        SELECT 
            ROUND(AVG(Market_Cap_USD_billion), 2) as Avg_USD_Billion,
            ROUND(AVG(MC_GBP_billion), 2) as Avg_GBP_Billion,
            ROUND(AVG(MC_EUR_billion), 2) as Avg_EUR_Billion,
            ROUND(AVG(MC_INR_billion), 2) as Avg_INR_Billion
        FROM {table_name}
        """
        df5 = pd.read_sql_query(query5, conn)
        print(df5.to_string(index=False))
        
        # Query 6: Specific bank details
        print(f"\n🏦 QUERY 6: JPMORGAN CHASE DETAILS (ALL CURRENCIES)")
        print("=" * 70)
        query6 = f"""
        SELECT Name, Market_Cap_USD_billion, MC_GBP_billion, MC_EUR_billion, MC_INR_billion
        FROM {table_name} 
        WHERE Name LIKE '%JPMorgan%'
        """
        df6 = pd.read_sql_query(query6, conn)
        print(df6.to_string(index=False))
        
        # Query 7: Chinese banks
        print(f"\n🇨🇳 QUERY 7: CHINESE BANKS")
        print("=" * 50)
        query7 = f"""
        SELECT Name, Market_Cap_USD_billion 
        FROM {table_name} 
        WHERE Name LIKE '%China%' OR Name LIKE '%Chinese%'
        ORDER BY Market_Cap_USD_billion DESC
        """
        df7 = pd.read_sql_query(query7, conn)
        print(df7.to_string(index=False))
        
        # Query 8: Banks ranked by GBP Market Cap
        print(f"\n💷 QUERY 8: BANKS RANKED BY GBP MARKET CAP")
        print("=" * 60)
        query8 = f"""
        SELECT Name, MC_GBP_billion 
        FROM {table_name} 
        ORDER BY MC_GBP_billion DESC
        """
        df8 = pd.read_sql_query(query8, conn)
        print(df8.to_string(index=False))
        
        # Query 9: Database schema info
        print(f"\n🔧 QUERY 9: TABLE SCHEMA INFORMATION")
        print("=" * 50)
        query9 = f"PRAGMA table_info({table_name})"
        cursor = conn.execute(query9)
        schema_info = cursor.fetchall()
        print("Column_ID | Column_Name              | Data_Type | Not_Null | Default | Primary_Key")
        print("-" * 80)
        for row in schema_info:
            print(f"{row[0]:<9} | {row[1]:<24} | {row[2]:<9} | {row[3]:<8} | {row[4]:<7} | {row[5]}")
        
        # Query 10: Min and Max values
        print(f"\n📊 QUERY 10: MIN/MAX MARKET CAP VALUES")
        print("=" * 60)
        query10 = f"""
        SELECT 
            MIN(Market_Cap_USD_billion) as Min_USD,
            MAX(Market_Cap_USD_billion) as Max_USD,
            MIN(MC_GBP_billion) as Min_GBP,
            MAX(MC_GBP_billion) as Max_GBP
        FROM {table_name}
        """
        df10 = pd.read_sql_query(query10, conn)
        print(df10.to_string(index=False))
        
        print(f"\n✅ All SQL queries completed successfully!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error running SQL queries: {e}")

if __name__ == '__main__':
    run_sql_queries() 