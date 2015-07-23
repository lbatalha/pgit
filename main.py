#!/usr/bin/env python3
#########	Builtins	#########
import os, sys

from datetime import datetime
from functools import wraps

#########	External Modules	#########

import pygit2
import pygments

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

@app.route('/r/<repo_name>/<branch>')
@app.route('/r/<repo_name>/<branch>/<path:file_path>')
def file_contents(repo_name, branch, file_path=None):
	files = []
	path = ROOT + repo_name
	repo = pygit2.Repository(path)
	branches = repo.listall_branches()
	commit = repo.revparse_single(branch)
	
	if file_path == None:			#Check for Repo List
		for entry in commit.tree:
			files.append(entry)
		return render_template('repo.html', files=files, repo=repo, branch=branch, branches=branches)

	file_id = commit.tree[file_path].id
	obj = repo.get(file_id)

	if obj.type == pygit2.GIT_OBJ_TREE:	#Check if its a tree
		obj = repo[obj.id]
		for entry in obj:
			files.append(entry)
		return render_template('path.html', repo_name=repo_name, file_path=file_path, files=files, branch=branch, branches=branches)
	else:
		obj = repo[obj.id]
		content = obj.read_raw().decode('utf8')
		try:
			lexer = get_lexer_for_filename(file_path, stripall=True)
			formatter = HtmlFormatter(linenos=True, cssclass='source')
			result = highlight(content, lexer, formatter)
		except pygments.util.ClassNotFound:
			result = content
		return render_template('file.html', file_path=file_path, result=result, branch=branch)

@app.route('/r/<repo_name>/<branch>/commits')
def commit_list(repo_name, branch):
	commit_list = []
	path = ROOT + repo_name
	repo = pygit2.Repository(path)
	reference = 'refs/heads/' + branch
	reference = repo.lookup_reference(reference).resolve()	
	for commit in repo.walk(reference.target, GIT_SORT_TOPOLOGICAL):
		commit_list.append(commit)
	
	return render_template('commit_list.html', repo_name=repo_name, commit_list=commit_list)


if __name__ == '__main__':
	app.debug = True
	app.run()


