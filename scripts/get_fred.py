# Step 1 – Fetch the mortgage rate data from FRED
import pandas as pd
from get_mls import sold, listings
import ssl
import urllib.request
import certifi

# Create an SSL context using certifi's certificate bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
SOLD_DF = sold()
LISTINGS_DF = listings()

with urllib.request.urlopen(URL, context=ssl_context) as response:
    mortgage = pd.read_csv(response, parse_dates=["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

# Step 2 – Resample weekly rates to monthly averages
mortgage["year_month"] = mortgage["date"].dt.to_period("M")
mortgage_monthly = (
    mortgage.groupby("year_month")["rate_30yr_fixed"].mean().reset_index()
)

# Step 3 – Create a matching year_month key on the MLS datasets
# Sold dataset — key off CloseDate
SOLD_DF["year_month"] = pd.to_datetime(SOLD_DF["CloseDate"]).dt.to_period("M")
# Listings dataset — key off ListingContractDate
LISTINGS_DF["year_month"] = pd.to_datetime(
    LISTINGS_DF["ListingContractDate"]
).dt.to_period("M")

# Step 4 – Merge
sold_with_rates = SOLD_DF.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = LISTINGS_DF.merge(mortgage_monthly, on="year_month", how="left")

# Step 5 – Validate the merge
# Check for any unmatched rows (rate should not be null)
print(sold_with_rates["rate_30yr_fixed"].isnull().sum())
print(listings_with_rates["rate_30yr_fixed"].isnull().sum())

# Preview
print(
    sold_with_rates[["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]].head()
)

SOLD_DF.to_csv("data/enriched/sold_with_rates.csv", index=False)
LISTINGS_DF.to_csv("data/enriched/listings_with_rates.csv", index=False)
