# Module 1 - Data Pipeline

## Overview

It scrapes book data from Books to Scrape, cleaned the data collected, converted prices from GBP then 
to INR, stored the cleaned data in a normalized SQLite database, and queries the database using SQL and pandas.

## Data Source

The data is scraped from Books to Scrape. It is given in the assignment.

The following fields are collected:

- Title
- Price
- Star rating
- Availability
- Category

I have collected 100 books. And here I have taken all the books that are in first 5 pages. 

## Data Cleaning

The price scraped is cleaned by removing the currency symbol and converting the value to a float data type.

Mapped Star ratings to integer values from 1 to 5.

Availability is converted into a boolean `in_stock` column.

For categorical columns like category and title if there is any missing field I directly dropped the row

For numerical columns like price and rating.
1) First converted Invalid numeric values to missing values (`NaN`) using
`pd.to_numeric(..., errors="coerce")`
2) Calculated the percentage of missing. If the percentage of data missing less than 5%, then I dropped the rows else did median imputation.


## Currency Conversion

Fixed Conversion as defined in project:

**1 GBP = 105.50 INR**

The INR price is calculated as:

`price_inr = price_gbp * 105.50`

I did round off to 2 decimal points.



Open `data_pipeline.ipynb` in Google Colab or Jupyter Notebook and run
all cells from top to bottom.
