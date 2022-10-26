import pickle
import joblib
import json

def save_pickle(model_name, pipeline_to_persist) -> None:
	# Prepare versioned save file name
	save_file_name = f"api/{model_name}.pkl"
	save_path = f"/{save_file_name}"

	remove_old_pipelines(files_to_keep=[save_file_name])
	pickle.dump(pipeline_to_persist, save_path)


def save_joblib(model, model_name, is_production=False, description=None, hyperparameters=None) -> None:
	save_path = f"api/{model_name}.joblib"

	joblib.dump(model, save_path)

	update_model_registry("model_registry.json", model_name, is_production, description, hyperparameters)
		


def save_json(model_name, filepath, hyperparameters): 
	saved_model = {}
	saved_model["hyperparameters"] = hyperparameters
	saved_model["X_train"] = self.X_train.tolist() if self.X_train is not None else "None",
	saved_model["y_train"] = self.y_train.tolist() if self.y_train is not None else "None"
	json_txt = json.dumps(saved_model, indent=4)
	with open(filepath, "w") as file: 
	  file.write(json_txt)


def save_tensorflow(): #do later
	pass



def update_model_registry(filepath, model_name, is_production, description, hyperparameters):
	with open(filepath, "r+") as file:
		data = json.load(file)
		if is_production:
			data['production_model'] = model_name
		if model_name not in data['models']:
			data['models'][model_name] = {}
		data['models'][model_name]['description'] = description
		data['models'][model_name]['hyperparameters'] = hyperparameters 

		file.seek(0)
		json.dump(data, file)
		file.truncate()

