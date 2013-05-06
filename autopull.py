import os, subprocess, json

from ConfigParser import ConfigParser

from bottle import get, post, request, run, default_app


def readRepos(filename="repos.ini"):
    
    config = ConfigParser()
    config.read(filename)
    
    repos = {}
    
    for section in config.sections():
        
        repo = {}
        
        for item in config.items(section):
            repo[item[0]] = item[1]
        
        repos[section] = repo
    
    return repos


def pull(path, remote="origin", branch="master"):
    
    subprocess.call(["git", "--git-dir=" + path + "/.git/", "--work-tree=" + path, "checkout", branch])
    #subprocess.call(["git", "--git-dir=" + path + "/.git/", "--work-tree=" + path, "pull", remote, branch]) # Updates working tree fine, but doesn"t update remote branch ref.
    subprocess.call(["git", "--git-dir=" + path + "/.git/", "--work-tree=" + path, "fetch", remote])
    subprocess.call(["git", "--git-dir=" + path + "/.git/", "--work-tree=" + path, "merge", remote + "/" + branch])


@get("/")
def getIndex():
    
    pass


@post("/")
def postIndex():
    
    repos = readRepos();
    
    raw = request.forms.get("payload")
    
    data = json.loads(raw) if isinstance(raw, str) else {}
    
    if ("repository" in data) and ("name" in data["repository"]) and (data["repository"]["name"] in repos):
        
        repo = repos[data["repository"]["name"]]
        
        if ("path" in repo) and (os.path.isdir(repo["path"])):
            
            kwargs = {}
            
            if "remote" in repo:
                kwargs["remote"] = repo["remote"]
            
            if "branch" in repo:
                kwargs["branch"] = repo["branch"]
            
            pull(repo["path"], **kwargs)


if __name__ == "__main__":
    run(host="0.0.0.0", port=8080)
    
else:
    application = default_app()
