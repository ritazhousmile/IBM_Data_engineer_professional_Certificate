#!/usr/bin/env python3
"""
Script to show the actual HTML structure of the banks table
This helps understand what the web scraping code sees
"""

import requests
from bs4 import BeautifulSoup
from banks_project import url

def show_html_structure():
    """Show the HTML structure of the target table"""
    
    print("🔍 ANALYZING HTML STRUCTURE OF BANKS TABLE")
    print("=" * 60)
    
    print(f"📍 URL: {url}")
    
    # Get the webpage content
    print("\n🌐 Fetching webpage...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the target table
    print("\n🔍 Finding target table...")
    tables = soup.find_all('table')
    
    target_table = None
    for i, table in enumerate(tables):
        classes = table.get('class', [])
        if 'wikitable' in classes and 'sortable' in classes:
            target_table = table
            print(f"✅ Found target table at index {i}")
            print(f"🏷️ Table classes: {classes}")
            break
    
    if target_table is None:
        print("❌ Target table not found!")
        return
    
    # Show table structure
    print(f"\n📋 TABLE STRUCTURE:")
    print("-" * 40)
    
    # Show table tag
    print(f"<table class=\"{' '.join(target_table.get('class', []))}\">")
    
    # Find and show header
    thead = target_table.find('thead')
    if thead:
        print("  <thead>")
        header_rows = thead.find_all('tr')
        for i, row in enumerate(header_rows):
            print(f"    <tr> <!-- Header row {i+1} -->")
            cells = row.find_all(['th', 'td'])
            for j, cell in enumerate(cells):
                text = cell.get_text(strip=True)
                print(f"      <th>{text}</th> <!-- Column {j+1} -->")
            print("    </tr>")
        print("  </thead>")
    
    # Find and show body (first few rows)
    tbody = target_table.find('tbody')
    if tbody:
        print("  <tbody>")
        data_rows = tbody.find_all('tr')
        print(f"    <!-- Total data rows: {len(data_rows)} -->")
        
        # Show first 3 data rows in detail
        for i, row in enumerate(data_rows[:3]):
            print(f"    <tr> <!-- Data row {i+1} -->")
            cells = row.find_all(['td', 'th'])
            for j, cell in enumerate(cells):
                text = cell.get_text(strip=True)
                print(f"      <td>{text}</td> <!-- Column {j+1} -->")
            print("    </tr>")
        
        if len(data_rows) > 3:
            print(f"    <!-- ... {len(data_rows) - 3} more rows ... -->")
        
        print("  </tbody>")
    
    print("</table>")
    
    # Show first row expanded details
    print(f"\n🎯 FIRST DATA ROW EXPANDED:")
    print("-" * 40)
    
    if tbody:
        first_row = tbody.find('tr')
        if first_row:
            cells = first_row.find_all(['td', 'th'])
            print(f"📊 First row has {len(cells)} cells:")
            for i, cell in enumerate(cells):
                text = cell.get_text(strip=True)
                attrs = dict(cell.attrs)
                print(f"  Cell {i}: '{text}' (attributes: {attrs})")
            
            print(f"\n🔍 Raw HTML of first row:")
            print(first_row.prettify())

if __name__ == '__main__':
    show_html_structure() 