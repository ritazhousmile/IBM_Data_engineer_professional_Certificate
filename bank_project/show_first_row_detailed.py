#!/usr/bin/env python3
"""
Script to show detailed first row information with expanded HTML structure
Perfect for screenshots of the first row data
"""

import requests
from bs4 import BeautifulSoup
from banks_project import url

def show_first_row_detailed():
    """Show detailed first row information with HTML structure"""
    
    print("🔍 DETAILED FIRST ROW ANALYSIS")
    print("=" * 60)
    
    print(f"📍 URL: {url}")
    
    # Get the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the target table
    tables = soup.find_all('table')
    target_table = None
    for table in tables:
        classes = table.get('class', [])
        if 'wikitable' in classes and 'sortable' in classes:
            target_table = table
            break
    
    if target_table is None:
        print("❌ Target table not found!")
        return
    
    # Find the first data row
    tbody = target_table.find('tbody')
    if not tbody:
        print("❌ Table body not found!")
        return
    
    first_row = tbody.find('tr')
    if not first_row:
        print("❌ First data row not found!")
        return
    
    print(f"\n🎯 FIRST DATA ROW - EXPANDED VIEW")
    print("=" * 50)
    
    # Show detailed cell information
    cells = first_row.find_all(['td', 'th'])
    print(f"📊 First row contains {len(cells)} cells:")
    
    for i, cell in enumerate(cells):
        text = cell.get_text(strip=True)
        attrs = dict(cell.attrs) if cell.attrs else {}
        tag_name = cell.name
        
        print(f"\n  📋 Cell {i+1}:")
        print(f"    Tag: <{tag_name}>")
        print(f"    Text: '{text}'")
        print(f"    Attributes: {attrs}")
        print(f"    Raw HTML: {str(cell)}")
    
    print(f"\n🔍 COMPLETE FIRST ROW HTML (Expanded):")
    print("-" * 50)
    print(first_row.prettify())
    
    print(f"\n📊 EXTRACTED DATA FROM FIRST ROW:")
    print("-" * 40)
    print(f"Column 0 (Rank): '{cells[0].get_text(strip=True)}'")
    print(f"Column 1 (Bank Name): '{cells[1].get_text(strip=True)}'")  # This is what we extract
    print(f"Column 2 (Market Cap): '{cells[2].get_text(strip=True)}'")  # This is what we extract
    
    print(f"\n✅ FINAL EXTRACTED VALUES (Used in ETL):")
    print("-" * 45)
    print(f"Name: '{cells[1].get_text(strip=True)}'")
    print(f"MC_USD_billion: '{cells[2].get_text(strip=True)}'")

if __name__ == '__main__':
    show_first_row_detailed() 