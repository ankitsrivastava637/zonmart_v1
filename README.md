

# Zonmart

Zonmart is a Ecommerce backend project that runs locally and utilizes FastAPI and SQL for its operation.

## Features

- CRUD Operations: Zonmart offers full support for performing CRUD (Create, Read, Update, Delete) operations on users, orders, and products.
- Unit Testing: Sample unit test is implemented using pytest for unit testing.
- Optimistic Locking: Zonmart incorporates optimistic locking for users by using record versions, enhancing data integrity.
- Authentication Support: User authentication is implemented to safeguard access to the project's functionalities.
- Data Integrity: Zonmart ensures data integrity by generating unique IDs for users.

## Assumptions
- Here the get_user_by_id has been mostly used, so user_id is being used for acccessing particular user assuming that front-end developer or other developer accessing the route has user_id while calling, but it can be replcaed with username. For this the route can be replaced with username and other function could be used for getting user by username and username can be made unique.

- This project is part of a more extensive backend system that includes other features within different apps. These apps can access Zonmart's APIs through cross-origin communication.

- The project assumes that read/write operations do not require caching. It is designed to run on a multi-node database server, with at least three replicated nodes and uses sharding for ensuring data integrity and performance. Database schema definitions (DDLs) can be adapted to support multi-node engines. For instance, when using ClickHouse Cloud, the ReplicatedMergeTree engine and insert_quorum value can be employed.

- For enhanced scalability, clustering, and high availability, services like AWS and AWS Elasticache could be utilized.

- In case the project is intended to be run as microservices and serverless, then services like AWS Lambda, AWS Step Functions, AWS API Gateway, SNS service for notifications, and AWS CloudWatch for log monitoring, code modifications are needed. Boto3 library can be used to make such adjustments.

- To automate processes for scalability and monitoring, AWS services can be valuable. AWS CodeBuild, AWS CodeCommit, and AWS CLI can be used for effective deployment control.

- Additional features like rate API limiting and API access authorization are in progress for this project. Relevant code sections are commented for further modifications and improvements. The project currently considers local environment API calls to be safe until these features are implemented.

- The project also assumes that there will be no dependency errors due to version or package/software mismatches during deployment on any other platform.

- The environment variables can be further specified in deployed platform instead being hard coded in the project to make security high for the envoironment variable and secret keys. This also helps if code is used on staging server(testing server for all features tested on local), deployment server(replica of production server with cherry picked features for testing) or production server(main server for users).

>> For example in main.py:  (here default values are given if no special environments variable are given): 
""
db_username = os.environ.get('DB_USERNAME', 'root')
db_password = os.environ.get('DB_PASSWORD', 'AshaShiva#08')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = int(os.environ.get('DB_PORT', '3306'))
db_schema = os.environ.get('DB_SCHEMA', 'zonmart')
""
OR, 
Provide env variable in terminal. (for windows users)
set DB_USERNAME=$Your_custom_username
set DB_PASSWORD=$Your_custom_password
set DB_HOST=$Your_custom_host
set DB_SCHEMA=Your_custom_schema
>> USE 'export' instead of 'set' for mac
""
- Note : To use different functionalities for deployment on staging, deployment and production server many other changes are requied. USing environment variable through platform/server defined varaibale names(instead of default values) is just on of the functionality required.
## Pre-requisites

- SQL workbench installed.
- Python installed in VS Code.

## Project Setup

### Clone the project from the terminal:

```bash
git clone https://github.com/ankitsrivastava637/zonmart_v1.git
```

### Navigate to the project directory from the terminal:

```bash
cd zonmart_v1
```

### Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Install project dependencies:

```bash
pip install -r requirements.txt
```

### SQL database setup 
Run commands of SQL_Zonmart_DDLs.txt to execute database creation, table creation and modifications. 
The SQL database should run on following environment configurations: 
""
username = 'root'
password = 'AshaShiva#08'
host = 'localhost'
port = 3306
database_schema = 'zonmart' 
OR,
provide custom values and then run in terminal (for windows users) : 
set DB_USERNAME=$Your_custom_username
set DB_PASSWORD=$Your_custom_password
set DB_HOST=$Your_custom_host
set DB_SCHEMA=Your_custom_schema
>> USE 'export' instead of 'set' for mac
""
## Usage

To start the application, run:

```bash
uvicorn app.main:app --reload
```

## Testing

Run the tests using pytest:

```bash
pytest
```

You can also run tests using the Swagger UI. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser and test routes through the "Try it out" options. The UI provides a user-friendly interface and defines data schemas for developers and testing.

[Download Swagger UI User Screenshot for the project (PDF)](https://github.com/ankitsrivastava637/zonmart_v1/files/13187451/Zonmart_Swagger_UI.pdf)
