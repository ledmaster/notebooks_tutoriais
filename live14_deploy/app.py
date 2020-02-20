from flask import Flask, request
import joblib as jb
import json

app = Flask(__name__)

mdl = jb.load("mdl.pkl.z")

@app.route("/")  # decorator
def main():
	
	print(request.args)
	
	title = request.args.get("titulo", default='')
	res = {"titulo": title,  "p": mdl.predict_proba([title])[0][1]}
	return json.dumps(res)
	
if __name__ == "__main__":
	app.run()
	
	
#https://gunicorn.org/#quickstart