# Code for ETL operations on Country-GDP data

# Importing the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# Define the required entities


url='https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs_extracted=['Name','MC_USD_billion']
table_attribs_final=['Name','Market_Cap_USD_billion','MC_GBP_billion','MC_EUR_billion','MC_INR_billion']
output_file='largest_banks_data.csv'
database_name='banks.db'
table_name='largest_banks'
log_file='code_log.txt'
csv_path='exchange_rates.csv'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    with open(log_file,'a')as f:
        f.write(message+'\n')
    print(message)

def extract(url, table_attribs_extracted):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    response = requests.get(url).text
    soup = BeautifulSoup(response,"html.parser")
    
    # Find table that contains both 'wikitable' and 'sortable' classes
    tables = soup.find_all('table')
    table = None
    for t in tables:
        classes = t.get('class', [])
        if 'wikitable' in classes and 'sortable' in classes:
            table = t
            break
    
    if table is None:
        raise ValueError("Could not find a table with both 'wikitable' and 'sortable' classes")
    
    df = pd.read_html(str(table))[0]
    
    # Table has 3 columns: ['Rank', 'Bank name', 'Market cap (US$ billion)']
    # Select only Bank name (column 1) and Market cap (column 2)
    if len(df.columns) >= 3:
        df = df.iloc[:, [1, 2]]  # Select columns 1 and 2 (Bank name, Market cap)
        df.columns = table_attribs_extracted
    
    df.to_csv(output_file,index=False)
    log_progress(f"Extracted table from {url} and saved to {output_file}")
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    
    # Read exchange rates from CSV file
    exchange_rates = pd.read_csv('exchange_rate.csv')  
    
    # Create a dictionary for easy lookup: currency -> rate
    rates = dict(zip(exchange_rates['Currency'], exchange_rates['Rate']))
    
    # Clean the Market Cap data - remove any commas and convert to float
    df['MC_USD_billion'] = pd.to_numeric(df['MC_USD_billion'].astype(str).str.replace(',', ''), errors='coerce')
    
    # Add USD column (same as original)
    df['Market_Cap_USD_billion'] = df['MC_USD_billion']
    
    # Convert to other currencies using exchange rates
    df['MC_GBP_billion'] = (df['MC_USD_billion'] * rates['GBP']).round(2)
    df['MC_EUR_billion'] = (df['MC_USD_billion'] * rates['EUR']).round(2)
    df['MC_INR_billion'] = (df['MC_USD_billion'] * rates['INR']).round(2)
    
    # Reorder columns to match the final attributes
    df = df[['Name', 'Market_Cap_USD_billion', 'MC_GBP_billion', 'MC_EUR_billion', 'MC_INR_billion']]
    
    log_progress(f"Converted Market Cap to GBP, EUR, and INR using exchange rates from {csv_path}")
    
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path,index=False)
    log_progress(f"Saved data to {output_path}")


def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    log_progress(f"Loaded data to {table_name} table in database")

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    cursor = sql_connection.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    for row in result:
        print(row)
    sql_connection.commit()


''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

def main():
    df = extract(url, table_attribs_extracted)
    print(df)
    df = transform(df, csv_path)
    print("transformed data",df)
    load_to_csv(df, output_file)
    sql_connection = sqlite3.connect(database_name)
    load_to_db(df, sql_connection, table_name)
    query_statement = f"SELECT * FROM {table_name}"
    run_query(query_statement, sql_connection)
    sql_connection.close()
    log_progress('All operations completed successfully')

if __name__ == '__main__':
    main()






