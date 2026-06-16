import pandas as pd
import boto3
import logging
from io import StringIO
from sqlalchemy import create_engine
from config import (
    DB_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    AWS_REGION,
    S3_PROCESSED_DATA_FOLDER
)

logger = logging.getLogger(__name__)

def load_data(tables: dict[str, pd.DataFrame]) -> None:
    """
    Loads all transformed tables into SQLite database and uploads to S3.
    """
    try:
        load_to_database(tables)
        upload_to_s3(tables)
    except Exception as e:
        logger.error(f"Error during loading: {e}")
        raise


def load_to_database(tables: dict[str, pd.DataFrame]) -> None:
    """
    Loads all transformed tables into SQLite database.
    """
    try: 
        logger.info(f"connecting to database at {DB_URL}...")
        engine = create_engine(DB_URL)

        for table_name, df in tables.items():
            logger.info(f"Loading table '{table_name}' into database...")
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            logger.info(f"Table '{table_name}' loaded successfully.")
        
        logger.info("All tables loaded successfully into the database.")
    except Exception as e:
        logger.error(f"Error occurred while loading data into the database: {e}")
        raise

def upload_to_s3(tables: dict[str, pd.DataFrame]) -> None:
    """
    Uploads all processed tables as CSVs to S3 processed/ folder.
    """
    try:
        logger.info("Connecting to S3...")
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        for table_name, df in tables.items():
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            s3_key = f"{S3_PROCESSED_DATA_FOLDER}/{table_name}.csv"
            logger.info(f"Uploading '{table_name}' to S3 at '{s3_key}'...")
            s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=s3_key, Body=csv_buffer.getvalue().encode('utf-8'))
            logger.info(f"Table '{table_name}' uploaded successfully to S3.")
        
        logger.info("All tables uploaded successfully to S3.")
    except Exception as e:
        logger.error(f"Error occurred while uploading data to S3: {e}")
        raise
    