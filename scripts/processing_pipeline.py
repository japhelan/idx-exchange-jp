"""
script that runs the entire pipleine of processing dataframe aka work from all of notebooks
present in repo simplified
"""

import pandas as pd
from idx.components import ingest, preprocessing, feature_engineering, cleaning
from sklearn.pipeline import Pipeline
import geopandas as gpd
from idx import config

# making school district geodataframe
district_gdf = gpd.read_file(config.DISTRICT_SHAPEFILE_PATH)
district_gdf = district_gdf.to_crs(epsg=4326)

# initializing pipeline components
ingestor = ingest.MLSIngestor(input_path="./data/raw/")
fred_ingestor = ingest.FredMerger()
cleaner = preprocessing.DataCleaner()
flagger = preprocessing.BadDataFlagger()
market_maker = feature_engineering.CreateMarketMetrics()
cleanup = feature_engineering.CleanUpTransformer()
null = feature_engineering.NullDropper()
dist_merger = feature_engineering.DistrictMerger(district_gdf=district_gdf)
iqr_flagger = cleaning.OutlierFlagger(
    subset=["OriginalListPrice", "LivingArea", "LotSizeArea"]
)
iqr_dropper = cleaning.OutlierRemover(
    subset=["OriginalListPrice", "LivingArea", "LotSizeArea"]
)
price_corrector = cleaning.PriceCorrector()


flagging_pipeline = Pipeline(
    [
        ("ingestor", ingestor),
        ("fred_ingestor", fred_ingestor),
        ("cleaner", cleaner),
        ("flagger", flagger),
        ("market_maker", market_maker),
        ("cleanup", cleanup),
        ("null", null),
        ("dist_merger", dist_merger),
        ("price_corrector", price_corrector),
        ("iqr_flagger", iqr_flagger),
    ]
)
dropping_pipeline = Pipeline(
    [
        ("ingestor", ingestor),
        ("fred_ingestor", fred_ingestor),
        ("cleaner", cleaner),
        ("flagger", flagger),
        ("market_maker", market_maker),
        ("cleanup", cleanup),
        ("null", null),
        ("dist_merger", dist_merger),
        ("price_corrector", price_corrector),
        ("iqr_flagger", iqr_flagger),
        ("iqr_dropper", iqr_dropper),
    ]
)

df_sold_full, df_listings_full = flagging_pipeline.fit_transform(X=None, y=None)
print(
    f"Pipeline completed. Full data shapes: sold_df: {df_sold_full.shape}, listings_df: {df_listings_full.shape}"
)
df_sold_clean, df_listings_clean = dropping_pipeline.fit_transform(X=None, y=None)
print(
    f"Pipeline completed. Clean data shapes: sold_df: {df_sold_clean.shape}, listings_df: {df_listings_clean.shape}"
)

df_sold_full.to_csv("./data/processed/sold_full.csv", index=False)
df_listings_full.to_csv("./data/processed/listings_full.csv", index=False)
df_sold_clean.to_csv("./data/processed/sold_clean.csv", index=False)
df_listings_clean.to_csv("./data/processed/listings_clean.csv", index=False)
print("Data saved to ./data/processed/")
