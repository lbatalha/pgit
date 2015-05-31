
import os
from flask import Flask
app = Flask(__name__)


@app.route('/')
def repo_list():
	return '\n'.join(os.listdir()) 
		

if __name__ == '__main__':
	app.run()
