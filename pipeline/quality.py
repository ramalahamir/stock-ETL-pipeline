import pandas as pd
import logging 

logger = logging.getLogger(__name__)

# Thresholds
MIN_ROW_COUNT = 900          # we ingested 1013 rows, losing more than ~10% is suspicious
MAX_DAILY_CHANGE_PCT = 50    # S&P 500 has never moved more than 50% in a day in history
MIN_PRICE = 0                # prices can never be negative

def run_quality_checks(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Runs data quality checks on all tables.
    Soft issues: fix and continue
    Hard issues: raise error and stop pipeline
    """
    logger.info("Running data quality checks...")

    tables = check_row_count(tables)
    tables = check_null_values(tables)
    tables = check_negative_prices(tables)
    tables = check_sp500_daily_change(tables)

    logger.info("All quality checks passed.")

    return tables

def check_row_count(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    HARD CHECK: Checks if any table has an unexpectedly low row count.
    """
    for name, df in tables.items():
        if len(df) < MIN_ROW_COUNT:
            raise ValueError(f"CRITICAL: Table '{name}' has unexpectedly low row count: {len(df)} rows."
                             f"min expected: {MIN_ROW_COUNT}. PIPELINE STOPPED.")
        logger.info(f"Table '{name}' row count check passed: {len(df)} rows.")
    return tables

def check_null_values(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    HARD CHECK: If more than 50% of a column is null, stop pipeline.
    SOFT CHECK: If minor nulls remain, warn but continue.
    """
    for table_name, df in tables.items():
        for col in df.columns:
            if col == "date":
                continue

            null_count = df[col].isnull().sum()
            null_pct = (null_count / len(df)) * 100

            if null_pct > 50:
                raise ValueError(
                    f"CRITICAL: Column '{col}' in '{table_name}' is {null_pct:.1f}% null. "
                    f"PIPELINE STOPPED."
                )
            elif null_count > 0:
                logger.warning(
                    f"WARNING: '{col}' in '{table_name}' still has {null_count} nulls "
                    f"({null_pct:.1f}%) after transform"
                )

    logger.info("Null value checks completed")
    return tables

def check_negative_prices(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    SOFT CHECK: Negative prices are impossible — replace with NaN and forward fill.
    """
    for table_name, df in tables.items():
        price_cols = [col for col in df.columns if "price" in col]

        for col in price_cols:
            negative_count = (df[col] < MIN_PRICE).sum()

            if negative_count > 0:
                logger.warning(
                    f"WARNING: '{col}' in '{table_name}' has {negative_count} "
                    f"negative values found replacing with NaN and forward filling"
                )
                df.loc[df[col] < MIN_PRICE, col] = None
                df[col] = df[col].ffill().bfill()

        tables[table_name] = df

    logger.info("Negative price checks completed")
    return tables


def check_sp500_daily_change(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    SOFT CHECK: Flag unrealistic S&P 500 daily moves but don't stop pipeline.
    HARD CHECK: If more than 10 days show impossible moves, something is wrong.
    """
    indices = tables.get("indices")

    if indices is None or "sp500_daily_change_pct" not in indices.columns:
        logger.warning("WARNING: Could not find indices table or sp500_daily_change_pct column")
        return tables

    extreme_moves = indices["sp500_daily_change_pct"].abs() > MAX_DAILY_CHANGE_PCT
    extreme_count = extreme_moves.sum()

    if extreme_count > 10:
        raise ValueError(
            f"CRITICAL: {extreme_count} days show S&P 500 moves over {MAX_DAILY_CHANGE_PCT}%. "
            f"Data may be corrupted. Pipeline stopped."
        )
    elif extreme_count > 0:
        logger.warning(
            f"WARNING: {extreme_count} days show S&P 500 moves over "
            f"{MAX_DAILY_CHANGE_PCT}% — flagged but continuing"
        )
    else:
        logger.info("S&P 500 daily change check passed")

    return tables