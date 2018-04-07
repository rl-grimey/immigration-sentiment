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
UNZIP_SHP = counties/tl_2017_us_county.shp
COUNTY_SHP = counties/counties.shp


## Commands
all: download transform clean
download: $(COUNTY_ZIP) $(UNZIP_SHP) 
transform: $(COUNTY_SHP)
# Clean up and remove downloaded zip, unfiltered extracts.
clean:
	@echo '>>> Removing downloaded/uneeded files.'
	@rm $(COUNTY_ZIP) $(UNZIP_FILES) \
	counties/tl_2017_us_county.shp.ea.iso.xml \
	counties/tl_2017_us_county.shp.iso.xml


## Rules
# Download zip file from U.S. Census
$(COUNTY_ZIP):
	@echo '>>> Downloading U.S. County shapefile.'
	@mkdir -p counties
	@curl $(COUNTY_URL) -o $@

# Unzip file into directory
#$(UNZIP_FILES): $(COUNTY_ZIP)
$(UNZIP_SHP): $(COUNTY_ZIP)
	@echo '>>> Unzipping shapefile.'
	@unzip -q -n -d counties $(COUNTY_ZIP)
	@touch $@

# transform: extract just the columns of interest and reproject to standard
#$(COUNTY_FILES): $(UNZIP_FILES)
$(COUNTY_SHP): $(UNZIP_SHP)
	@echo '>>> Filtering and reprojecting shapefile to WGS 84.'
	@ogr2ogr -overwrite \
			-select STATEFP,COUNTYFP,GEOID,NAME \
			-t_srs "EPSG:4326" \
			$@ $< tl_2017_us_county

# Upload to Postgres

