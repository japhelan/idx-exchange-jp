from pathlib import Path

DATA_DIR = Path("./data/raw")
RAW_LISTINGS_DIR = DATA_DIR / "concated/listings.csv"
RAW_SOLD_DIR = DATA_DIR / "concated/sold.csv"
NUMERIC_ANALYSIS_FIELDS = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
]
DISTRIBUTION_COLS = ["ClosePrice", "LivingArea", "DaysOnMarket"]
ENRICHED_DATA_DIR = Path("./data/enriched")
