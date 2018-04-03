###############################################################################
# Makefile to download and convert U.S. County .shp files					  #
###############################################################################

# Globals
COUNTY_ZIP = us_counties.zip
# 2017 U.S. Tiger Line data
COUNTY_ZIP_URL = ftp://ftp2.census.gov/geo/tiger/TIGER2017/COUNTY/tl_2017_us_county.zip
COUNTY_SHP = $(wildcard counties/*)

# Download zip file from U.S. Census
$(COUNTY_ZIP):
	mkdir -p counties
	wget --no-use-server-timestamps -O $(COUNTY_ZIP) $(COUNTY_ZIP_URL)

# Unzip file into directory
extract: $(COUNTY_ZIP)
	unzip -n -d counties $(COUNTY_ZIP)

# transform: extract

# upload: transform

# clean: upload
# 

