#!/usr/bin/python3
import os
import pygit2
from flask import Flask, render_template, url_for

app = Flask(__name__)

root = '/home/lbatalha/pgit_data/repos/'

@app.route('/')
def repo_list():
	return render_template('root.html', dirlist=os.listdir(root), root=root)

@app.route('/<repo_name>/')
def dir_list(repo_name):
	path = root + repo_name
	repo = pygit2.Repository(path)
	commit = repo.revparse_single('master')
	files = [];
	
	for entry in commit.tree:
		files.append(entry)
		
	return render_template('repo.html', files=files, repo=repo)

@app.route('/<repo_name>/<path:file_path>')
def file_contents(repo_name, file_path):
	url_for('static', filename='styles/file.css')
	path = root + repo_name
	repo = pygit2.Repository(path)
	commit = repo.revparse_single('master')
	file_id = commit.tree[file_path].id
	obj = repo.get(file_id)

	return render_template('file.html', file_path=file_path, obj=obj)

if __name__ == '__main__':
	app.debug = True
	app.run()
