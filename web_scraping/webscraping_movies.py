import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_50'
csv_path = 'top_50_films.csv'  # Current directory
df = pd.DataFrame(columns=["Average Rank","Film","Year"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

# Find the first table (movie rankings table)
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

# Extract data from each row
for row in rows:
    if count < 50:  # Only get top 50 as specified
        cols = row.find_all('td')
        if len(cols) >= 3:  # Make sure row has enough columns
            try:
                # Extract rank, film name, and year
                rank = cols[0].get_text(strip=True)
                film = cols[1].get_text(strip=True)
                year = cols[2].get_text(strip=True)
                
                # Add to DataFrame
                new_row = {"Average Rank": rank, "Film": film, "Year": year}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                
                count += 1
                print(f"Added: {rank}. {film} ({year})")
                
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

# Save to CSV
df.to_csv(csv_path, index=False)
print(f"\n✅ Successfully saved {len(df)} movies to {csv_path}")

# Display the first few entries
print("\n📊 First 10 movies:")
print(df.head(10))

# Save to SQLite database
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
print(f"\n💾 Data also saved to SQLite database: {db_name}")

print(f"\n📈 Total movies processed: {count}") 