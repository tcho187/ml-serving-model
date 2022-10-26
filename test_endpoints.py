import requests
import json

#Test /predict
with open("test.json", "r+") as file:
	data = json.load(file)
r = requests.post("http://127.0.0.1:8000/predict", json=data)
print(r.content)

#b'{"prediction":[0,0,0],"log_proba":[[0.9769012377113903,0.0230987622886097],[0.9915082141714369,0.008491785828563145],[0.9820304217540038,0.01796957824599622]]}'


#Test /production_model

r = requests.get("http://127.0.0.1:8000/production_model")
print(r.content)
#b'{"First Model":{"description":"First Model","hyperparameters":{"classifier__C":0.01,"classifier__class_weight":null,"classifier__dual":false,"classifier__fit_intercept":true,"classifier__intercept_scaling":1,"classifier__l1_ratio":null,"classifier__max_iter":1000,"classifier__multi_class":"auto","classifier__n_jobs":null,"classifier__penalty":"l2","classifier__random_state":null,"classifier__solver":"lbfgs","classifier__tol":0.0001,"classifier__verbose":true,"classifier__warm_start":false}}}'


#Test /swap_model

data = {"model_name":"Second Model"}
r = requests.post("http://127.0.0.1:8000/swap", json=data)
print(r.content)
#b'{"Second Model":{"description":"Second Model","hyperparameters":{"classifier__C":1.0,"classifier__class_weight":null,"classifier__dual":false,"classifier__fit_intercept":true,"classifier__intercept_scaling":1,"classifier__l1_ratio":null,"classifier__max_iter":1000,"classifier__multi_class":"auto","classifier__n_jobs":null,"classifier__penalty":"l2","classifier__random_state":null,"classifier__solver":"newton-cg","classifier__tol":0.0001,"classifier__verbose":true,"classifier__warm_start":false}}}'