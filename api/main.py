from typing import List, Any, Dict, AnyStr, Union

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import insert

from . import crud, models, schemas
from .database import SessionLocal, engine

import pyarrow.parquet as pq # hardcoded
import pandas as pd # for upload
import numpy as np
import time
import joblib
import json


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.on_event("startup")
async def load_model():
	# Loading in model from serialized .pkl file
	file = "api/First Model.joblib"
	clf = joblib.load(file)
	app.model = clf

@app.get("/upload/")
def upload_leads(db: Session = Depends(get_db)):

	
	df = pq.read_table("ds_leads.parquet.gzip").to_pandas()
	inputs = df.to_dict('records')
	with db.bind.begin() as conn:
		t0 = time.time()
		conn.execute(insert(models.Lead), inputs)
		# conn.commit()
		print("SQLA Core", time.time() - t0)
	

	df = pq.read_table("ds_clicks.parquet.gzip").to_pandas()
	inputs = df.to_dict('records')
	with db.bind.begin() as conn:
		t0 = time.time()
		conn.execute(insert(models.Click), inputs)
		# conn.commit()
		print("SQLA Core", time.time() - t0)


	df = pq.read_table("ds_offers.parquet.gzip").to_pandas()
	inputs = df.to_dict('records')
	with db.bind.begin() as conn:
		t0 = time.time()
		conn.execute(insert(models.Offer), inputs)
		# conn.commit()
		print("SQLA Core", time.time() - t0)

	return {"Hi":"hi"}


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
@app.post("/predict")
async def predict(X: JSONStructure):
	df = pd.DataFrame(X)
	print(app.model)
	pred = app.model.predict_proba(df)
	probabilities = np.max(app.model.predict_proba(df), axis=1)
	prediction = app.model.predict(df).tolist()
	log_proba = app.model.predict_proba(df).tolist()
	return {"prediction": prediction, "log_proba": log_proba}
	
 

@app.post("/swap")
async def swap(data: schemas.Model, filepath: str = "api/model_registry.json"):
	model_name = data.model_name
	with open(filepath, "r+") as file:
		data = json.load(file)
		data['production_model'] = model_name
		file.seek(0)
		json.dump(data, file)
		file.truncate()
	file = f"api/{model_name}.joblib"
	clf = joblib.load(file)
	app.model = clf
	return {data['production_model']: data['models'][data['production_model']]}
	try:
		pass
	except Exception as err:
		raise HTTPException(status_code=404, detail="Unknown")


@app.get("/production_model")
async def production_model(filepath: str = "api/model_registry.json"):
	with open(filepath, "r") as file:
		data = json.load(file)
		return {data['production_model']: data['models'][data['production_model']]}
	


@app.post("/leads/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
	db_lead = crud.get_lead(db, lead_uuid=lead.lead_uuid)
	if db_lead:
		raise HTTPException(status_code=400, detail="Lead already registered")
	return crud.create_lead(db=db, lead=lead)


@app.get("/leads/", response_model=List[schemas.Lead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	leads = crud.get_leads(db, skip=skip, limit=limit)
	return leads


@app.get("/leads/{lead_uuid}", response_model=schemas.Lead)
def read_lead(lead_uuid: int, db: Session = Depends(get_db)):
	db_lead = crud.get_lead(db, lead_uuid=lead_uuid)
	if db_lead is None:
		raise HTTPException(status_code=404, detail="Lead not found")
	return db_lead

