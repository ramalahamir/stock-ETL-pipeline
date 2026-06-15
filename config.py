import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project (the stock_pipeline folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw", "US_Stock_Data.csv")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# database
DB_PATH = os.path.join(BASE_DIR, 'stock_pipeline.db')
DB_URL = f'sqlite:///{DB_PATH}'
DB_TABLE_NAME = 'stock_data'

# Schedule (24 hours format)
SCHEDULE_TIME = '08:00'  # Run every day at 8 AM

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

# GROQ API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# S3 folder paths
S3_RAW_DATA_FOLDER = "raw/US_Stock_Data.csv"
S3_PROCESSED_DATA_FOLDER = "processed/"