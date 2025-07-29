#!/usr/bin/env python3
"""
Script to run ONLY the extract method from banks_project.py
This will show the exact output for screenshot purposes
"""

# Import the extract method and required variables from banks_project.py
from banks_project import extract, url, table_attribs_extracted

def main():
    """Run the extract method and show its output"""
    
    print("🚀 RUNNING EXTRACT METHOD FROM banks_project.py")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Table attributes to extract: {table_attribs_extracted}")
    print("=" * 60)
    
    # Call the extract method (same as in original script)
    print("\n📊 Calling extract(url, table_attribs_extracted)...")
    result_df = extract(url, table_attribs_extracted)
    
    print(f"\n✅ Extract method completed!")
    print(f"📊 DataFrame shape: {result_df.shape}")
    print(f"📋 Column names: {list(result_df.columns)}")
    
    print(f"\n🎯 EXTRACT METHOD OUTPUT (DataFrame):")
    print("-" * 50)
    print(result_df)
    
    print(f"\n📈 DataFrame Info:")
    print(f"Data types: {dict(result_df.dtypes)}")
    print(f"Total rows: {len(result_df)}")
    
    print(f"\n📁 Files created:")
    print(f"- CSV file: largest_banks_data.csv")
    print(f"- Log file: code_log.txt")

if __name__ == '__main__':
    main() 