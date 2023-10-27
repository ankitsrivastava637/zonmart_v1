# Zonmart

Runs on Local. Uses FastAPI and SQL to create the project.

# Features

# > crud operations: for users, orders, products
# > unit test using pytest
# > Optmisic locking for user using record versions
# > Authentication support for users
# > Data integtrity support to generate unique id for users 

# Assumptions 
This project is part of bigger backend project which have other features installed in other apps which can access this project's APIs through Cross origin communication.

The project considers read/write operations to not require caching and runs on multi-node database server, with atleast 3 replicated nodes and also uses sharding for enuring data integrity and performance. (The DDLs need to be modified to support multi-node engine support. Here for example if Clickhouse Cloud is used the ReplicatedMergeTree engine( while declaring DDls ) can be used to replicate on nodes and insert_quorum value can be used while inserting values in the database.)

For more scalability, clustering and  high availability services like  AWS, AWS elasticache could be used.

The project assumes that further modifications need to be made in code if project is to be run microservice serverless services like AWS Lambda, AWS step functions, AWS API gateway, SNS service for notification and AWS cloudwatch service for monitoring logs. Here for making such modfications boto3 library can be used.

For automating processes for scalability and monitoring AWS services would be good. And AWS codebuid, AWS codecommit, AWS CLI could be used to control deployments effectively. 

Extra features like rate API limiting and API access authorization are features which in progress for this project. Hence have been commented in code for further modification and improvements. So, it considers local environment api calls to be safe until it's built.

This project assumes that there no dependency errors due to version or package/software mistmatch while deployment on any other platform.

# Pre-requisites 
SQL workbench installed
Python installed in vs-code

# Project Setup
## Clone the project from terminal: 
   git clone  https://github.com/ankitsrivastava637/zonmart_v1.git

## Naviagate to the project directory from terminal
cd zonmart_v1

## Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

## Install project dependencies:
pip install -r requirements.txt

# Ussage
## To start the application, run:
uvicorn app.main:app --reload

# Testing
## Run the test using pytest:
pytest

## Run test using swagger UI 
run http://127.0.0.1:8000/docs in browser and test routes through try it out options.

