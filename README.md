# Thomas Cho Even Financial Take Home


## Name

Model Serving Prototype


##Description

1. Creating a Feature Database

There's an endpoint `/upload` in main.py that reads the parquet files in memory and writes to a sqlite database using SqlAlchemy. The data is saved to even.db. models.py describes the DDL or the table schemas.


2. Model Training

Two models are trained. The script is in `ml.py`. The data is read in from the database, and created into a pandas dataframe. Training and testing data are created. Testing data is saved to a json file for testing the endpoint later. Two models are trained and saved to joblib files. The metadata is saved to a json called `model_repository.json`. A user input is the model ID ie. "First Model" "Second Model". To do - create hash out of the metadata to capture unique model ID.

3. Model Server

The api is using FastApi. Once you deploy the docker container, the api is served [http://127.0.0.1:8000/](http://127.0.0.1:8000/).  

Endpoints
/upload = upload parquet files to sqlite
/predict = predict json body
/swap = swap production model id
/production_mode = get production model id
/leads = get leads


## Installation

You will need Docker Desktop or Docker.

```bash
docker build -t even .

docker run -p 8000:8000 even
```

## Usage

The test script `test_endpoints.py` tests all 3 endpoints.

```bash

docker ps

docker exec -it [docker image] /bin/bash

python3 test_endpoints.py
```

## Contributing
Thomas Cho

## License
[MIT](https://choosealicense.com/licenses/mit/)