from fastapi import FastAPI
import git_parser

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/")
async def root(repo: str=None, file: str=None):
    if repo == None: return {}
    return git_parser.Git.get_repo_from_url(repo).get_esign_repo(file)