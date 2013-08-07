import os, subprocess, json

from bottle import get, post, request, run, default_app


def readConfig(filename="project/repositories.json"):
	return json.load(open(filename)) if os.path.isfile(filename) else {}


def pull(path, remote="origin", branch="master"):
	
	cwd = os.getcwd()
	
	os.chdir(path)
	
	subprocess.call(["git", "checkout", branch])
	#subprocess.call(["git", "--git-dir=" + path + "/.git/", "--work-tree=" + path, "pull", remote, branch]) # Updates working tree fine, but doesn"t update remote branch ref.
	subprocess.call(["git", "fetch", remote])
	subprocess.call(["git", "merge", remote + "/" + branch])
	
	os.chdir(cwd)


@get("/")
def getIndex():
	pass


@post("/")
def postIndex():
	
	config = readConfig()
	
	rawData = request.forms.get("payload")
	
	data = json.loads(rawData) if isinstance(rawData, str) else {}
	
	if ("repository" in data) and ("name" in data["repository"]) and (data["repository"]["name"] in config):
		
		for repository in config[data["repository"]["name"]]:
			
			if ("path" in repository) and (os.path.isdir(repository["path"])):
				
				kwargs = {}
				
				if "remote" in repository:
					kwargs["remote"] = repository["remote"]
				
				if "branch" in repository:
					kwargs["branch"] = repository["branch"]
				
				pull(repository["path"], **kwargs)


if __name__ == "__main__":
	run(host="0.0.0.0", port=8080)

else:
	application = default_app()
