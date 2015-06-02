#!/usr/bin/python3
import os
import pygit2
from flask import Flask, render_template

app = Flask(__name__)

root = '/home/lbatalha/pgit_data/repos/'

@app.route('/')
def repo_list():
	return render_template('root.html', dirlist=os.listdir(root), root=root)

@app.route('/<repo_name>')
def dir_list(repo_name):
	path = root + repo_name
	repo = pygit2.Repository(path)
	commit = repo.revparse_single('master')
	files = [];
	
	for entry in commit.tree:
		files.append(entry)
		
	return render_template('repo.html', files=files, repo=repo)


if __name__ == '__main__':
	app.debug = True
	app.run()
