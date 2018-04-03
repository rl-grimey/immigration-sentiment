###############################################################################
# Makefile to download and convert U.S. County .shp files					  #
###############################################################################

## Variables
# Input URL: 2017 U.S. Tiger Line data
COUNTY_URL = 'https://www2.census.gov/geo/tiger/TIGER2017/COUNTY/tl_2017_us_county.zip'

# Output file
COUNTY_ZIP = us_counties.zip

# File formats
FILE_FORMATS = .cpg .dbf .prj .shp .shp.xml .shx
COUNTY_FILES = $(foreach format, $(FILE_FORMATS), counties/tl_2017_us_county$(format))


## Commands
# Download zip file from U.S. Census
$(COUNTY_ZIP):
	mkdir -p counties
	curl $(COUNTY_URL) -o $@

# Unzip file into directory
$(COUNTY_FILES): $(COUNTY_ZIP)
	unzip -n -d counties $(COUNTY_ZIP)
	touch $@

# transform: extract

# upload: transform

clean: $(COUNTY_FILES)
	rm $(COUNTY_ZIP)
