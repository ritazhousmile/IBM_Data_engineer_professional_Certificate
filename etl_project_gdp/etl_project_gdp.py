# Cleaned ETL operations on Country-GDP data

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

# Configuration
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ["Country", "GDP_USD_millions"]
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'

def extract(url, table_attribs):
    """Extract GDP data from Wikipedia table."""
    response = requests.get(url).text 
    soup = BeautifulSoup(response, 'html.parser')
    
    # Find table with both 'wikitable' and 'sortable' classes
    tables = soup.find_all('table')
    table = None
    for t in tables:
        classes = t.get('class', [])
        if 'wikitable' in classes and 'sortable' in classes:
            table = t
            break
    
    if table is None:
        raise ValueError("Could not find a table with both 'wikitable' and 'sortable' classes")
    
    # Extract and select relevant columns
    df = pd.read_html(str(table))[0]
    if len(df.columns) >= 8:
        df = df.iloc[:, [0, 2]]  # Country and IMF GDP estimate
        df.columns = table_attribs
        
        # Remove header row if it exists
        if df.iloc[0, 0] in ['Country/Territory', 'Country']:
            df = df.iloc[1:].reset_index(drop=True)
    
    return df

def transform(df):
    """Clean and transform GDP data from millions to billions USD."""
    # Clean GDP data: remove commas, dashes, and convert to numeric
    df['GDP_USD_millions'] = (df['GDP_USD_millions']
                            .astype(str)
                            .str.replace(',', '')
                            .str.replace('—', '')
                            .str.replace('–', '')
                            .str.strip())
    
    # Convert to numeric, invalid values become NaN
    df['GDP_USD_millions'] = pd.to_numeric(df['GDP_USD_millions'], errors='coerce')
    
    # Remove rows with missing GDP data
    df = df.dropna(subset=['GDP_USD_millions']).reset_index(drop=True)
    
    # Convert from millions to billions and round to 2 decimal places
    df['GDP_USD_millions'] = (df['GDP_USD_millions'] / 1000).round(2)
    
    return df

def load_to_csv(df, csv_path):
    """Save dataframe to CSV file."""
    df.to_csv(csv_path, index=False)

def load_to_db(df, sql_connection, table_name):
    """Save dataframe to database table."""
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    """Execute query and print results."""
    cursor = sql_connection.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    for row in result:
        print(row)
    sql_connection.commit()

def log_progress(message):
    """Log progress message to file."""
    with open('log.txt', 'a') as f:
        f.write(message + '\n')

def main():
    """Main ETL pipeline execution."""
    # Extract
    df = extract(url, table_attribs)
    log_progress('Data extracted successfully')
    
    # Transform
    df = transform(df)
    log_progress('Data transformed successfully')
    
    # Load to CSV
    load_to_csv(df, csv_path)
    log_progress('Data loaded to CSV successfully')
    
    # Load to Database
    sql_connection = sqlite3.connect(db_name)
    load_to_db(df, sql_connection, table_name)
    log_progress('Data loaded to database successfully')
    
    # Verify database load
    query_statement = f"SELECT COUNT(*) FROM {table_name}"
    print(f"Number of records in database: ", end="")
    run_query(query_statement, sql_connection)
    
    sql_connection.close()
    log_progress('All operations completed successfully')

if __name__ == '__main__':
    main() 