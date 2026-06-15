import pandas as pd
import boto3
import logging 
from io import StringIO
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
    AWS_REGION,
    S3_RAW_DATA_FOLDER
)

logger = logging.getLogger(__name__)

def ingest_data() -> pd.DataFrame:
    """
    Ingests raw data from AWS S3 and returns a DataFrame.
    """
    try: 
        logger.info(f"Connecting to S3 bucket '{AWS_BUCKET_NAME}' in region '{AWS_REGION}'...")
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        logger.info(f"Fetching raw data from S3 key '{S3_RAW_DATA_FOLDER}'...")
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=S3_RAW_DATA_FOLDER)
        raw_data = response['Body'].read().decode('utf-8')

        logger.info("Reading raw data into DataFrame...")
        df = pd.read_csv(StringIO(raw_data))
        logger.info(f"Successfully ingested data with shape {df.shape}")
        return df

    except s3_client.exceptions.NoSuchKey:
        logger.error(f"The specified key '{S3_RAW_DATA_FOLDER}' does not exist in bucket '{AWS_BUCKET_NAME}'.")
        raise

    except Exception as e:
        logger.error(f"An error occurred while ingesting data from S3: {e}")
        raise



# def ingest_data() -> pd.DataFrame:
#     """
#     Reads the raw CSV file and returns a DataFrame.
#     """
#     try: 
#         logger.info(f"Reading raw data from {RAW_DATA_DIR}")
#         df = pd.read_csv(RAW_DATA_DIR)
#         logger.info(f"Successfully ingested data with shape {df.shape}")
#         return df
#     except FileNotFoundError:
#         logger.error(f"File not found at {RAW_DATA_DIR}")
#         raise
#     except Exception as e:
#         logger.error(f"An error occurred while ingesting data: {e}")
#         raise