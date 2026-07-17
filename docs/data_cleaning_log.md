# Data Cleaning Log

All Changes made during data cleaning dataframe(s). Both start with the enriched datasets

Written in order of occurance.

Columns `'CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate'` were changed to datetime types

Dropped the **following** columns:

**1st Pass** (85 cols -> 77 cols)

- "AboveGradeFinishedArea" : 100% Missing
- "BelowGradeFinishedArea" : >99% Missing
- "TaxAnnualAmount" : >99% Missing
- "BuilderName" : 97% Missing
- "ElementarySchoolDistrict" : 100% Missing
- "BusinessType" : >99% Missing
- "CoveredSpaces" : 100% Missing
- "MiddleOrJuniorSchool" : 91% Missing
- "MiddleOrJuniorSchoolDistrict" : 100% Missing

**2nd Pass** (77 cols -> 64 cols)

- ListAgentEmail" : Not important to any analysis or visualizations
- "ListAgentFirstName" : redudant as ListAgentFullName exists
- "ListAgentLastName" : see above
- "ListAgentFirstName.1" : duplicate of ListAgentFirstName column (which is also being removed)
- "ListAgentLastName.1" : see above
- "Latitude.1" : duplicate of Latitude
- "Longitude.1" : duplicate of Longitude
- "UnparsedAddress.1", : Also a dupe
- FireplacesTotal : 100% Missing
- PropertyType.1 : Duplicate
- `DaysOnMarket.1` : dupe
- `LivingArea.1`: dupe
- `ListPrice.1` : dupe
- `CloseDate.1`: dupe
- `BuyerOfficeName.1` : dupe
- `PropertyType.1`: dupe
- HighSchool : mostly missing and `HighSchoolDistrict` exists (and is more full)
- ElementarySchool : 91% missing

Noted: AttachedGarageYN should be convered to binary int (currently True False object)

The following type conversions were compelted to prevent impossible values (Float64 to Int64):

`YearBuilt`,`StreetNumberNumeric`, `BathroomsTotalInteger`(why was it not an integer its in the name), `TaxYear`, `Stories`
