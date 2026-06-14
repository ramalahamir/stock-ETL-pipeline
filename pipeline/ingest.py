import pandas as pd
import logging 
from config import RAW_DATA_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def ingest_data() -> pd.DataFrame:
    """
    Reads the raw CSV file and returns a DataFrame.
    """
    try: 
        logger.info(f"Reading raw data from {RAW_DATA_DIR}")
        df = pd.read_csv(RAW_DATA_DIR)
        logger.info(f"Successfully ingested data with shape {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found at {RAW_DATA_DIR}")
        raise
    except Exception as e:
        logger.error(f"An error occurred while ingesting data: {e}")
        raise