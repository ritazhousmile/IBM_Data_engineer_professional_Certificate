#!/usr/bin/env python3
"""
Test script to specifically run and display the detailed output of the extract function
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from banks_project import url, table_attribs_extracted, log_progress

def test_extract():
    """Test the extract function with detailed debugging output"""
    
    print("🔍 TESTING EXTRACT FUNCTION")
    print("=" * 50)
    
    print(f"📍 URL: {url}")
    print(f"📋 Target attributes: {table_attribs_extracted}")
    
    # Step 1: Get the webpage content
    print("\n🌐 Step 1: Fetching webpage...")
    response = requests.get(url)
    print(f"✅ Status code: {response.status_code}")
    
    # Step 2: Parse with BeautifulSoup
    print("\n🍲 Step 2: Parsing HTML with BeautifulSoup...")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Step 3: Find the correct table
    print("\n🔍 Step 3: Finding tables...")
    tables = soup.find_all('table')
    print(f"📊 Found {len(tables)} tables on the page")
    
    table = None
    for i, t in enumerate(tables):
        classes = t.get('class', [])
        print(f"  Table {i}: classes = {classes}")
        if 'wikitable' in classes and 'sortable' in classes:
            table = t
            print(f"  ✅ Found target table at index {i}")
            break
    
    if table is None:
        print("❌ Could not find table with both 'wikitable' and 'sortable' classes")
        return None
    
    # Step 4: Extract data with pandas
    print("\n📊 Step 4: Extracting data with pandas...")
    df = pd.read_html(str(table))[0]
    print(f"📏 Raw DataFrame shape: {df.shape}")
    print(f"📋 Raw columns: {list(df.columns)}")
    
    print("\n🔍 Raw DataFrame (first 5 rows):")
    print(df.head())
    
    # Step 5: Select relevant columns
    print("\n✂️ Step 5: Selecting relevant columns...")
    if len(df.columns) >= 3:
        df = df.iloc[:, [1, 2]]  # Select columns 1 and 2 (Bank name, Market cap)
        df.columns = table_attribs_extracted
        print(f"✅ Selected columns 1 and 2, renamed to: {list(df.columns)}")
    
    print(f"\n🎯 FINAL EXTRACTED DATAFRAME:")
    print("-" * 40)
    print(df)
    
    print(f"\n📊 DataFrame Info:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Data types: {dict(df.dtypes)}")
    
    return df

if __name__ == '__main__':
    result = test_extract()
    if result is not None:
        print(f"\n✅ Extract test completed successfully!")
    else:
        print(f"\n❌ Extract test failed!") 