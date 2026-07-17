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


# ================================================
# DATA CLEANING
# ===============================================

# hopefully listing/sold agnostic but yet to be checked
COLS_TO_DROP = [
    "AboveGradeFinishedArea",
    "BelowGradeFinishedArea",
    "TaxAnnualAmount",
    "BuilderName",
    "ElementarySchoolDistrict",
    "BusinessType",
    "CoveredSpaces",
    "MiddleOrJuniorSchool",
    "MiddleOrJuniorSchoolDistrict",
    "Latitude.1",
    "Longitude.1",
    "UnparsedAddress.1",
    "FireplacesTotal",
    "DaysOnMarket.1",
    "LivingArea.1",
    "ListPrice.1",
    "CloseDate.1",
    "BuyerOfficeName.1",
    "PropertyType.1",
    "HighSchool",
    "ElementarySchool",
    "ListAgentEmail",
    "ListAgentFirstName",
    "ListAgentLastName",
    "ListAgentFirstName.1",
    "ListAgentLastName.1",
]

DT_COLS = [  # cols to convert to datetime
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate",
]

INT_COLS = [  # cols to convert to integers
    "YearBuilt",
    "StreetNumberNumeric",
    "BathroomsTotalInteger",
    "TaxYear",
    "Stories",
]

NON_PREDICTIVE_COLS = [
    "ListingKey",
    "CloseDate",
    "ClosePrice",
    "Latitude",
    "Longitude",
    "UnparsedAddress",
    "ListOfficeName",
    "BuyerOfficeName",
    "CoListOfficeName",
    "ListAgentFullName",
    "CoListAgentFirstName",
    "CoListAgentLastName",
    "BuyerAgentMlsId",
    "BuyerAgentFirstName",
    "BuyerAgentLastName",
    "ListingKeyNumeric",
    "SubdivisionName",
    "BuyerOfficeAOR",
    "StreetNumberNumeric",
    "ListingId",
    "ContractStatusChangeDate",
    "CoBuyerAgentFirstName",
    "PurchaseContractDate",
    "ListingContractDate",
    "LotSizeDimensions",
    "BuyerAgencyCompensationType",
    "BuyerAgencyCompensation",
]  # columns with minimal use in modeling

NON_ANALYSIS_COLS = [
    "ListAgentFullName",
    "CoListAgentFirstName",
    "CoListAgentLastName",
    "BuyerAgentMlsId",
    "BuyerAgentFirstName",
    "BuyerAgentLastName",
    "SubdivisionName",
    "BuyerOfficeAOR",
    "ContractStatusChangeDate",
]  # columns not to be used in analysis (as of friday july 17th 2026)

NON_NEG_FLAG_COLS = [
    "OriginalListPrice",
    "LivingArea",
    "ListPrice",
    "DaysOnMarket",
    "ParkingTotal",
    "LotSizeAcres",
    "BathroomsTotalInteger",
    "BuildingAreaTotal",
    "BedroomsTotal",
    "LotSizeArea",
    "MainLevelBedrooms",
    "GarageSpaces",
    "LotSizeSquareFeet",
    "ClosePrice",  # added mostly for sold data
]
