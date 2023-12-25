from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	return 'Ready for Winter Project! Testing wp'

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=80,debug=False)
