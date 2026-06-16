import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_data(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Cleans and transforms raw stock data.
    Returns a dictionary of DataFrames split by asset category.
    """
    try:
        logger.info("Starting data transformation...")

        # step 1: drop unnamed index column if it exists
        df.drop(columns=[col for col in df.columns if "unnamed" in col.lower()], inplace=True)
        logger.info("Dropped unnamed index column if it existed.")

        # step 2: Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(".", "", regex=False)
            .str.replace("&", "and")
        )
        logger.info(f"Cleaned column names: {list(df.columns)}")

        # Step 3: Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, format="mixed")
        logger.info("Converted date column to datetime")

        # Step 4: Sort by date
        df = df.sort_values("date").reset_index(drop=True)
        logger.info("Sorted data by date")

        # Step 5: Remove duplicate rows
        before = len(df)
        df.drop_duplicates(inplace=True)
        logger.info(f"Removed {before - len(df)} duplicate rows")

        # Step 6: Forward fill missing values 
        # Price columns → forward fill (carry last known price)
        price_cols = [col for col in df.columns if "price" in col]
        df[price_cols] = df[price_cols].ffill().bfill()
        logger.info("Forward filled missing price values")

        # Volume columns → fill with 0 (no trading = zero volume)
        vol_cols = [col for col in df.columns if "vol" in col]
        df[vol_cols] = df[vol_cols].fillna(0)
        logger.info("Filled missing volume values with 0")

        # Step 7: Convert price and volume columns to numeric
        numeric_cols = [col for col in df.columns if col != "date"]
        for col in numeric_cols:
            df[col] = df[col].astype(str).str.replace(",", "", regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Step 8: Calculate S&P 500 daily % change
        df["sandp_500_pct_change"] = df["sandp_500_price"].pct_change() * 100
        logger.info("Calculated S&P 500 daily percentage change")

        # Step 9: Flag Significant market moves (> 2% change in either direction)
        df["sandp_500_significant_move"] = df["sandp_500_pct_change"].abs() > 2
        logger.info("Flagged significant market moves")

        # Step 10: Calculate 7-day rolling average for S&P 500 price
        df["sandp_500_7day_avg"] = df["sandp_500_price"].rolling(window=7).mean()
        logger.info("Calculated 7-day rolling average for S&P 500 price")

        # Step 11: Split into asset category tables
        tables = split_into_tables(df)
        logger.info(f"Split data into {len(tables)} asset category tables")
        
        return tables

    except Exception as e:
        logger.error(f"Error occurred during data transformation: {e}")
        raise
 
def split_into_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Splits the cleaned DataFrame into separate tables by asset category.
    """
    tables = {
        "indices": df[["date", "sandp_500_price", "nasdaq_100_price", "nasdaq_100_vol",
                        "sandp_500_pct_change", "sandp_500_significant_move", "sandp_500_7day_avg"]],

        "commodities": df[["date", "natural_gas_price", "natural_gas_vol",
                            "crude_oil_price", "crude_oil_vol", "copper_price", "copper_vol",
                            "platinum_price", "platinum_vol", "silver_price", "silver_vol",
                            "gold_price", "gold_vol"]],

        "crypto": df[["date", "bitcoin_price", "bitcoin_vol",
                      "ethereum_price", "ethereum_vol"]],

        "stocks": df[["date", "apple_price", "apple_vol", "tesla_price", "tesla_vol",
                      "microsoft_price", "microsoft_vol", "google_price", "google_vol",
                      "nvidia_price", "nvidia_vol", "berkshire_price", "berkshire_vol",
                      "netflix_price", "netflix_vol", "amazon_price", "amazon_vol",
                      "meta_price", "meta_vol"]]
    }

    for name, table in tables.items():
        logger.info(f"Table '{name}': {table.shape[0]} rows, {table.shape[1]} columns")

    return tables