#!/usr/bin/env python3
"""
Script to test and display the first row details from extract function
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from banks_project import url, table_attribs_extracted

def test_extract_first_row():
    """Extract data and focus on the first row details"""
    
    print("🎯 TESTING EXTRACT FUNCTION - FIRST ROW FOCUS")
    print("=" * 60)
    
    print(f"📍 URL: {url}")
    print(f"📋 Target attributes: {table_attribs_extracted}")
    
    # Perform the extract process
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the correct table
    tables = soup.find_all('table')
    table = None
    for t in tables:
        classes = t.get('class', [])
        if 'wikitable' in classes and 'sortable' in classes:
            table = t
            break
    
    if table is None:
        print("❌ Could not find target table!")
        return
    
    # Extract with pandas
    df = pd.read_html(str(table))[0]
    
    print(f"\n🔍 RAW TABLE INFO:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    
    print(f"\n📊 RAW FIRST ROW:")
    print("-" * 30)
    first_row_raw = df.iloc[0]
    for i, (col, val) in enumerate(first_row_raw.items()):
        print(f"  Column {i}: '{col}' = '{val}'")
    
    # Apply column selection (like in extract function)
    if len(df.columns) >= 3:
        df_selected = df.iloc[:, [1, 2]]  # Select columns 1 and 2
        df_selected.columns = table_attribs_extracted
        
        print(f"\n✂️ AFTER COLUMN SELECTION:")
        print(f"  Selected columns: {list(df_selected.columns)}")
        
        print(f"\n🎯 PROCESSED FIRST ROW:")
        print("-" * 30)
        first_row_processed = df_selected.iloc[0]
        for col, val in first_row_processed.items():
            print(f"  {col}: '{val}' (type: {type(val).__name__})")
        
        # Show the actual first row data that would be in the final DataFrame
        print(f"\n📋 FIRST ROW AS SERIES:")
        print(first_row_processed)
        
        print(f"\n📋 FIRST ROW AS DICT:")
        print(first_row_processed.to_dict())
        
        return df_selected
    
    return df

if __name__ == '__main__':
    result = test_extract_first_row()
    print(f"\n✅ Test completed! First row extracted successfully.") 