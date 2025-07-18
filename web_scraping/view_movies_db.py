import sqlite3
import pandas as pd

def view_movies_database():
    """View and analyze the Movies database"""
    
    # Connect to database
    conn = sqlite3.connect('Movies.db')
    
    # Read data into DataFrame
    df = pd.read_sql_query("SELECT * FROM Top_50", conn)
    
    # Convert columns to proper types
    df['Year'] = pd.to_numeric(df['Year'])
    df['Average Rank'] = pd.to_numeric(df['Average Rank'])
    
    print("🎬 TOP 50 MOVIES DATABASE")
    print("=" * 50)
    
    # Display basic info
    print(f"📊 Total movies: {len(df)}")
    print(f"📅 Year range: {df['Year'].min()} - {df['Year'].max()}")
    print()
    
    # Display first 15 movies
    print("🏆 TOP 15 MOVIES:")
    print("-" * 50)
    for idx, row in df.head(15).iterrows():
        print(f"{int(row['Average Rank']):2d}. {row['Film']} ({int(row['Year'])})")
    
    print()
    print("📈 DECADE BREAKDOWN:")
    print("-" * 30)
    
    # Analyze by decade
    df['Decade'] = (df['Year'] // 10) * 10
    decade_counts = df['Decade'].value_counts().sort_index()
    
    for decade, count in decade_counts.items():
        print(f"{decade}s: {count} movies")
    
    print()
    print("🎭 RECENT MOVIES (2010+):")
    print("-" * 30)
    recent_movies = df[df['Year'] >= 2010].sort_values('Average Rank')
    for idx, row in recent_movies.iterrows():
        print(f"{int(row['Average Rank']):2d}. {row['Film']} ({int(row['Year'])})")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    view_movies_database() 