# `CSE_6242-Project` 
## Team: __The Last Airbender's__

_Joseph McAndrews, Colleen Morse, Sunil Prasad, Valerie Schnapp, Jonathan Yang_

-----------

## About
Breathing clean fresh air is vital to life. From traditional
medicinal practices to modern disease control, access
to fresh air has long been integral to a healthy life. Un-
fortunately, human beings have been adding toxins and
chemicals to the air as byproducts of our transportation,
manufacture, and consumption. This project seeks to
explore the relationship between specific air pollutants
and the possible mortality effects they may have on the
population that breathes the contaminated air.

Our project seeks to answer the following questions:
- How does air pollution correlate to cardiopulmonary-
associated mortality?
- Are certain air pollutants more associated with
mortality rates?
- Can mortality predictions be made from air qual-
ity data?

Initial AQI data set can be found [here](https://www.kaggle.com/threnjen/40-years-of-air-quality-index-from-the-epa-daily)

We will be using a variety of different tools for our analysis:
- GCP --> to host our data
- MySQL --> for database
- Python --> data wrangling, EDA, and modeling
  - Jupyter Notebook
- R --> data wrangling and EDA
- Qlik --> for front-end visualization and dashboarding
- LaTex --> to write our reports

-----------

## Quickstart

Install all packages to a python virtual environment

```bash
pip install -r requirements.txt
```
------------

## Sections

###   Configurations `config.py`

Connect to the MySQL database. 

** To get it to the work, you must add the 3 `.pem` files to the `ssl_keys` folder.

###   Database Management  `db_management`

Connect to the MySQL database and be able to add tables

- Functions included: 
    - `create_table`: Creates a table in MySQL database
    - `csv_to_rows`: Adds rows of a CSV into database table

###   Modeling

Machine Learning models built customized for the AQI dataset. 

- Models include:
    - Random Forest Regression `RFRRegressor`
    - Time series model `TimeSeriesForecaster`
    
Example can be found here: [notebooks](https://github.com/schnappv/CSE_6242_Project/tree/main/notebooks)

### Dashboards

We created our dashboards using QlikSense. To view the dashboards, follow this [link](https://53d1461or2ndxqa.us.qlikcloud.com/sense/app/2291b7fa-41bb-417e-9f3e-5951c0b390b2/overview). 

To log in to the view only account please use:
- Username: gatech.lastairbenders@gmail.com
- password: #cse6242


