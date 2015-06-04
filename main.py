import os
import pygit2
from flask import Flask, render_template, url_for

app = Flask(__name__)

ROOT = '/home/lbatalha/pgit_data/repos/'

@app.route('/')
def repo_list():
	return render_template('root.html', dirlist=os.listdir(ROOT), ROOT=ROOT)

@app.route('/<repo_name>/')
def dir_list(repo_name):
	path = ROOT + repo_name
	repo = pygit2.Repository(path)
	commit = repo.revparse_single('master')
	files = []

	for entry in commit.tree:
		files.append(entry)

	return render_template('repo.html', files=files, repo=repo)

@app.route('/<repo_name>/<path:file_path>')
def file_contents(repo_name, file_path):
	path = ROOT + repo_name
	repo = pygit2.Repository(path)
	commit = repo.revparse_single('master')

	file_id = commit.tree[file_path].id
	obj = repo.get(file_id)

	if obj.type == pygit2.GIT_OBJ_TREE:
		files = []
		file_path += '/'
		obj = repo[obj.id]
		for entry in obj:
			files.append(entry)
		return render_template('path.html', file_path=file_path, files=files)
	else:
		obj = repo[obj.id]
		return render_template('file.html', file_path=file_path, obj=obj)

if __name__ == '__main__':
	app.debug = True
	app.run()
