from geopy.geocoders import Nominatim
from tqdm import tqdm

tqdm.pandas()
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import pandas as pd
import argparse

"""
local run command (for me to copy and paste smile)
/usr/bin/env /Users/jack/Repos/idx-exchange-jp/.venv/bin/python /Users/jack/Repos/idx-exchange-jp/scripts/bulk_geocode.py ./data/enriched/geo_enc/address_df.csv --address_column=full_address --output_path=./data/enriched/geo_enc/address_df.csv 
"""


def bulk_geocode(csv_path, address_column, output_path):
    # 1. Load your dataset
    # df is now passed directly, no need to read from CSV
    df = pd.read_csv(csv_path, low_memory=False)

    # 2. Initialize geocoder (Replace user_agent with your application name)
    # Nominatim is free but requires a distinct user_agent string
    locator = Nominatim(user_agent="my_bulk_geocoder_application_v1")

    # 3. Create a rate limiter
    # Nominatim usage policy strictly requires a minimum 1-second delay between requests
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

    print("Starting bulk geolocation...")

    # 4. Apply geocoding with a visible progress bar
    df["location"] = df[address_column].progress_apply(geocode)

    # 5. Extract Latitude and Longitude from the location object
    df["latitude"] = df["location"].apply(lambda loc: loc.latitude if loc else None)
    df["longitude"] = df["location"].apply(lambda loc: loc.longitude if loc else None)

    # Drop the temporary raw location object column before saving
    df = df.drop(columns=["location"])

    # 6. Save the results
    df.to_csv(output_path, index=False)
    print(f"Success! Saved results to {output_path}")

    return df


parser = argparse.ArgumentParser(description="Aggregate MLS Data")
parser.add_argument("csv_path", type=str, help="The address CSV file to process")
parser.add_argument(
    "--address_column",
    type=str,
    help="The column name containing addresses",
)

parser.add_argument(
    "--output_path",
    type=str,
    help="The output path to save the results",
    default=None,
)

args = parser.parse_args()

csv_path = args.csv_path
address_column = args.address_column
output_path = args.output_path if args.output_path else "output.csv"

bulk_geocode(csv_path, address_column, output_path)
