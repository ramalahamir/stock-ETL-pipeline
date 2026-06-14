import os

# Base directory of the project (the stock_pipeline folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# database
DB_PATH = os.path.join(BASE_DIR, 'stock_pipeline.db')
DB_URL = f'sqlite:///{DB_PATH}'
DB_TABLE_NAME = 'stock_data'

# Schedule (24 hours format)
SCHEDULE_TIME = '08:00'  # Run every day at 8 AM