import os, sys
from datetime import datetime

import pygit2

from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE

from flask import Flask, render_template, url_for

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter


app = Flask(__name__)

ROOT = '/home/lbatalha/pgit_data/repos/'

@app.route('/')
def repo_list():
	return render_template('root.html', dirlist=os.listdir(ROOT), ROOT=ROOT)

@app.route('/<repo_name>/')
@app.route('/<repo_name>/<path:file_path>')
def file_contents(repo_name, file_path=None):
	files = []
	path = ROOT + repo_name
	repo = pygit2.Repository(path)
	commit = repo.revparse_single('master')

	if file_path == None:			#Check for Repo List
		for entry in commit.tree:
			files.append(entry)
		return render_template('repo.html', files=files, repo=repo, repo_name=repo_name)

	file_id = commit.tree[file_path].id
	obj = repo.get(file_id)

	if obj.type == pygit2.GIT_OBJ_TREE:	#Check if its a directory
		file_path += '/'
		obj = repo[obj.id]
		for entry in obj:
			files.append(entry)
		return render_template('path.html', repo_name=repo_name, file_path=file_path, files=files)
	else:
		obj = repo[obj.id]
		content = obj.read_raw().decode('utf8')
		lexer = get_lexer_for_filename(file_path, stripall=True)
		formatter = HtmlFormatter(linenos=True, cssclass='source')
		result = highlight(content, lexer, formatter)
		return render_template('file.html', file_path=file_path, result=result)

@app.route('/<repo_name>/commits')
def commit_list(repo_name):
	commit_list = []
	path = ROOT + repo_name
	repo = pygit2.Repository(path)
	
	for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
		commit_list.append(commit)
	
	return render_template('commit_list.html', repo_name=repo_name, commit_list=commit_list)


if __name__ == '__main__':
	app.debug = True
	app.run()
