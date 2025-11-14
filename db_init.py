"""
SQLite Database Setup for AgriFlow
Creates farmers and loans tables
Loads sample data from CSV files
"""
import sqlite3
import pandas as pd
import os

# Create connection to SQLite
DB_PATH = 'data/agriflow.db'
conn = sqlite3.connect(DB_PATH)

def init_db():
    """Initialize database tables"""
    
    # Farmers Table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY,
        mobile TEXT UNIQUE,
        name TEXT,
        district TEXT,
        land_acres REAL,
        soil_ph REAL,
        ndvi REAL,
        dcs_score REAL
    )
    ''')
    
    # Loans Table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY,
        farmer_mobile TEXT,
        amount REAL,
        purpose TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    print("✓ Database tables created successfully")

def load_sample_data():
    """Load sample farmer data from CSV files"""
    
    try:
        # Load from PM-KISAN dataset
        df = pd.read_csv('data/raw/pmkisan_tn.csv')
        
        # Prepare data for farmers table
        farmers_data = pd.DataFrame({
            'mobile': ['9176543210', '9287654321', '9398765432', '9409876543', '9510987654'],
            'name': df['name'].head(5).values if 'name' in df.columns else ['Farmer 1', 'Farmer 2', 'Farmer 3', 'Farmer 4', 'Farmer 5'],
            'district': df['district'].head(5).values if 'district' in df.columns else ['Madurai', 'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli'],
            'land_acres': (df['land_size_ha'].head(5).values * 2.471) if 'land_size_ha' in df.columns else [6.17, 4.45, 7.86, 4.94, 3.71],  # Convert ha to acres
            'soil_ph': [6.8, 6.5, 7.2, 6.9, 7.0],
            'ndvi': [0.78, 0.65, 0.82, 0.70, 0.75],
            'dcs_score': [0.0, 0.0, 0.0, 0.0, 0.0]
        })
        
        # Insert data into database
        farmers_data.to_sql('farmers', conn, if_exists='replace', index=False)
        print(f"✓ Loaded {len(farmers_data)} farmer records")
        
    except FileNotFoundError as e:
        print(f"⚠ CSV file not found: {e}")
        print("Creating sample farmers with mock data...")
        
        # Create mock data if CSV not available
        mock_farmers = pd.DataFrame({
            'mobile': ['9176543210', '9287654321', '9398765432', '9409876543', '9510987654'],
            'name': ['Raj Kumar', 'Priya Singh', 'Arjun Patel', 'Lakshmi Devi', 'Vikram Sharma'],
            'district': ['Madurai', 'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli'],
            'land_acres': [6.17, 4.45, 7.86, 4.94, 3.71],
            'soil_ph': [6.8, 6.5, 7.2, 6.9, 7.0],
            'ndvi': [0.78, 0.65, 0.82, 0.70, 0.75],
            'dcs_score': [0.0, 0.0, 0.0, 0.0, 0.0]
        })
        
        mock_farmers.to_sql('farmers', conn, if_exists='replace', index=False)
        print(f"✓ Loaded {len(mock_farmers)} mock farmer records")
    
    conn.commit()

def get_farmer_by_mobile(mobile):
    """Query farmer by mobile number"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farmers WHERE mobile LIKE ?", (f'%{mobile[-4:]}%',))
    result = cursor.fetchone()
    return result

if __name__ == "__main__":
    print("Initializing AgriFlow Database...")
    init_db()
    load_sample_data()
    print(f"✓ Database ready at: {DB_PATH}")
    
    # Test query
    farmer = get_farmer_by_mobile('9176543210')
    if farmer:
        print(f"\nTest query result: {farmer}")
