# U.S. Census TIGERLINE Data

### 2017 County Shapefile

[Technical Documentation](https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2017/TGRSHP2017_TechDoc_Ch2.pdf) from the U.S. Census.

[Data Dictionairy](https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2017/TGRSHP2017_TechDoc_Ch3.pdf) from the same. *Page 3-30* for `tl_2017_us_county.shp`.

#### Attributes

| Field | Length | Type | Description |
|---|---|---|---|
| STATEFP | 2 | String | Current state FIPS code |
| COUNTYFP | 3 | String | Current county FIPS code |
| COUNTYNS | 8 | String | Current county GNIS code |
| GEOID | 5 | String | County identifier; a concatenation of Current state FIPS code and county FIPS code |
| NAME | 100 | String | Current county name |
| NAMELSAD | 100 | String | Current name and the translated legal/statistical area description for county |
| LSAD | 2 | String | Current legal/statistical area description code for county |
| CLASSFP | 2 | String | Current FIPS class code |
| MTFCC | 5 | String | MAF/TIGER feature class code (G4020) |
| CSAFP | 3 | String | Current combined statistical area code |
| CBSAFP | 5 | String | Current metropolitan statistical area/micropolitan statistical area code |
| METDIVFP | 5 | String | Current metropolitan division code |
| FUNCSTAT | 1 | String | Current functional status |
| ALAND | 14 | Number | Current land area |
| AWATER | 14 | Number | Current water area |
| INTPTLAT | 11 | String | Current latitude of the internal point |
| INTPTLON | 12 | String | Current longitude of the internal point |