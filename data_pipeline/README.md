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

## Database Design

I created a SQLite database with two tables, `categories` and `books`.

The `categories` table contains:

- `category_id` as the primary key
- `category_name`

The `books` table contains:

- `book_id` as the primary key
- `title`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`
- `category_id`

Here `category_id` in the books table is a foreign key which refers to the `category_id` in the categories table.

I kept categories in a separate table so that the same category name does not need to be stored again and again for every book.

## SQL Queries

I have written SQL queries on the database using:

- `SELECT` and `WHERE`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `BETWEEN`
- `JOIN`

The queries and their outputs can be seen in the `data_pipeline.ipynb` notebook.

## Pandas Comparison

I also read the SQL query results into pandas DataFrames using `pd.read_sql()`.

I performed the same join using `pd.merge()` in pandas without using SQL.

Finally, I compared the SQL JOIN result with the pandas merge result and checked that both are giving the same output.

## How to Run

Install the required libraries using the `requirements.txt` file.

`pip install -r requirements.txt`

Open `data_pipeline.ipynb` in Google Colab or Jupyter Notebook and run all the cells from top to bottom.
