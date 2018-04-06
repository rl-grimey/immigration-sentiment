###############################################################################
# Makefile to download and convert U.S. County .shp files					  #
###############################################################################

## Variables
# Input URL: 2017 U.S. Tiger Line data
COUNTY_URL = 'https://www2.census.gov/geo/tiger/TIGER2017/COUNTY/tl_2017_us_county.zip'

# Output file
COUNTY_ZIP = us_counties.zip

# File formats
FILE_FORMATS = cpg dbf prj shp shp.xml shx
UNZIP_FILES  = $(foreach format, $(FILE_FORMATS), counties/tl_2017_us_county.$(format))
COUNTY_FILES = $(foreach format, $(FILE_FORMATS), counties/counties.$(format))


## Commands
# Download zip file from U.S. Census
$(COUNTY_ZIP):
	@echo '>>> Downloading U.S. County shapefile.'
	@mkdir -p counties
	@curl $(COUNTY_URL) -o $@

# Unzip file into directory
$(UNZIP_FILES): $(COUNTY_ZIP)
	@unzip -q -n -d counties $(COUNTY_ZIP)

# transform: extract just the columns of interest and reproject to standard
$(COUNTY_FILES): $(UNZIP_FILES)
	@echo '>>> Filtering and reprojecting shapefile to WGS 84.'
	@ogr2ogr -overwrite \
			-select STATEFP,COUNTYFP,GEOID,NAME \
			-t_srs "EPSG:4326" \
			counties/counties.shp counties/tl_2017_us_county.shp \
			tl_2017_us_county

# Upload to Postgres
# python script?


## Steps for getting file into database.
download: $(COUNTY_ZIP) $(UNZIP_FILES)
transform: $(COUNTY_FILES)
all: download transform clean 

# Clean up and remove downloaded zip, unfiltered extracts.
clean:
	@echo '>>> Removing downloaded/uneeded files.'
	@rm $(COUNTY_ZIP) $(UNZIP_FILES) \
	counties/tl_2017_us_county.shp.ea.iso.xml \
	counties/tl_2017_us_county.shp.iso.xml
