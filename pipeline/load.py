import pandas as pd
import logging
from sqlalchemy import create_engine
from config import DB_URL, PROCESSED_DATA_DIR

logger = logging.getlogger(__name__)

def load_data(tables: dict[str, pd.DataFrame]) -> None:
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