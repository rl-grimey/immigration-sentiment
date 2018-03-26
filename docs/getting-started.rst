Getting started
===============

This is where you describe how to get set up on a clean install, including the
commands necessary to get the raw data (using the `sync_data_from_s3` command,
for example), and then how to make the cleaned, final data sets.

0. Set your `.env` file variables so you can access the database. (!)
1. Install Python interpreter; `conda` + Python3.
2. Install Python environment; `make create_environment`
3. Install Python required libraries; `make requirements`
4. Create Postgres Tables, if they're not already rendered.
