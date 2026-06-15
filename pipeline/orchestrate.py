import logging 
import schedule
import time
from pipeline.ingest import ingest_data
from pipeline.transform import transform_data
from pipeline.load import load_data
from config import SCHEDULE_TIME

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

def run_pipeline() -> None:
    """
    Runs the full ETL pipeline:
    Extract → Transform → Load
    """
    try: 
        logger.info("Starting ETL pipeline...")

        # Step 1: Ingest data
        logger.info("Ingesting data...")
        raw_data = ingest_data()

        # Step 2: Transform data
        logger.info("Transforming data...")
        transformed_tables = transform_data(raw_data)

        # Step 3: Load data
        logger.info("Loading data...")
        load_data(transformed_tables)
        logger.info("ETL pipeline completed successfully.")

    except Exception as e:  
        logger.error(f"ETL pipeline failed: {e}")

def schedule_pipeline() -> None:
    """
    Schedules the pipeline to run daily at the configured time.
    """
    logger.info(f"Scheduling ETL pipeline to run daily at {SCHEDULE_TIME}...")
    schedule.every().day.at(SCHEDULE_TIME).do(run_pipeline)

    logger.info("Scheduler Running...")
    while True:
        schedule.run_pending()
        time.sleep(1)