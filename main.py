import logging 
from pipeline.orchestrate import run_pipeline, schedule_pipeline

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

def main():
    """
    Entry point of the pipeline.
    Change mode to "schedule" for automated daily runs.
    """
    mode = "run" # "run" to run once or "schedule" for daily runs

    if mode == "run":
        logger.info("Running ETL pipeline once...")
        run_pipeline()
    elif mode == "schedule":
        logger.info("Starting ETL pipeline scheduler...")
        schedule_pipeline()
    else:
        logger.error(f"Invalid mode: {mode}. Use 'run' or 'schedule'.")

if __name__ == "__main__":
    main()
