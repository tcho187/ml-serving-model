import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_openml
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
import sqlite3
from sqlite3 import Error

from save_models import save_joblib
def create_connection(db_file: str):
	"""
		create a database connection to the SQLite database
		specified by the db_file
		Parameters
		----------
		db_file : Filepath to sqlite db

		Returns
		-------
		db connection instance
		Notes
		-----
		pass
	"""	
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

def read_from_sql(database: str):
	"""
		Read data from sqlite db
		Parameters
		----------
		database : Filepath to sqlite db

		Returns
		-------
		Pandas dataframe
		Notes
		-----
		pass
	"""	
	conn = create_connection(database) # create a database connection
	with conn:
		cur = conn.cursor()
		cur.execute("""
			SELECT o.lead_uuid, o.offer_id,apr,lender_id,requested,loan_purpose,annual_income,credit,case when clicked_at is null then 0 else 1 end as clicked
			FROM offers o
			left join leads l on o.lead_uuid = l.lead_uuid
			left join clicks c on o.offer_id = c.offer_id""")
		rows = cur.fetchall()
		df = pd.DataFrame(rows, columns=["lead_uuid", "offer_id","apr","lender_id","requested","loan_purpose","annual_income","credit","clicked"])
		df['lender_id'] = df['lender_id'].astype('str')
		return df



def process(X,y, hyperparameters):
	"""
		Fit the model according to the given training data.
		Parameters
		----------
		X : {array-like, sparse matrix} of shape (n_samples, n_features)
			Training vector, where `n_samples` is the number of samples and
			`n_features` is the number of features.
		y : array-like of shape (n_samples,)
			Target vector relative to X.
		Returns
		-------
		self
			Fitted estimator.
		Notes
		-----
		https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?highlight=logistic
	"""
	numeric_features = ["apr", "requested", "annual_income"]
	numeric_transformer = Pipeline(
		steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
	)

	categorical_features = ["loan_purpose", "credit", "lender_id"]
	categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse=True)

	preprocessor = ColumnTransformer(
		transformers=[
			("num", numeric_transformer, numeric_features),
			("cat", categorical_transformer, categorical_features),
		],
		remainder='passthrough'
	)


	clf = Pipeline(
		steps=[("preprocessor", preprocessor), ("classifier", LogisticRegression(**hyperparameters))]
	)
	clf.fit(X, y)
	print("model score: %.3f" % clf.score(X, y))
	return clf


if __name__ == '__main__':
	# read the data
	data = read_from_sql(database="even.db")

	y=data.iloc[:,-1]
	X=data.drop(["lead_uuid", "offer_id", "clicked"],axis = 1)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=22, stratify=y)
	X_test.to_json("test.json", orient="records")

	#Build the first model
	model1 = process(X_train, y_train, hyperparameters={'C':0.01, 'max_iter':1000, 'verbose':True})
	params1 = {i:model1.get_params()[i] for i in model1.get_params() if 'classifier__' in i}
	#Build the second model
	model2 = process(X_train, y_train, hyperparameters={'solver': 'newton-cg', 'max_iter':1000, 'verbose':True})
	params2 = {i:model2.get_params()[i] for i in model2.get_params() if 'classifier__' in i}

	#Save the first model
	model_dict1 = {
	'is_production': True,
	'description': 'First Model',
	'hyperparameters': params1
	}
	save_joblib(model1, 'First Model', **model_dict1)
	#Save the second model
	model_dict2 = {
	'is_production': False,
	'description': 'Second Model',
	'hyperparameters': params2
	}
	save_joblib(model2, 'Second Model', **model_dict2)


