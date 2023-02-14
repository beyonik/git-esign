import re
import esign
import requests
import json

class GitRepo:
    def __init__(self, repo_id):
        self.repo_id = repo_id

    def get_releases(self):
        releases = json.loads(requests.get(
            f"https://api.github.com/repos/{self.repo_id}/releases", 
            headers = {
                'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28'
            }
        ).content)
        return releases

    def get_esign_repo_entries(self, filename_filter:str=None):
        entries = []
        for release in self.get_releases():
            for asset in release['assets']:
                if asset['browser_download_url'][-4:] != '.ipa': continue
                if filename_filter and asset['name'].lower() != filename_filter.lower(): continue

                entries.append(
                    esign.ESignRepoEntry(
                        name=f"{release['tag_name']} - {asset['name']}",
                        bundleIdentifier=None,
                        developerName=asset['uploader']['login'],
                        subtitle=None, 
                        iconURL=None,
                        version=release['tag_name'], 
                        versionDate=release['published_at'].split("T")[0], 
                        versionDescription=f"{asset['name']} @ {release['tag_name']}",
                        downloadURL=asset['browser_download_url'],
                        localizedDescription=None,
                        tintColor=None,
                        size=asset['size'],
                        beta=False
                    )
                )
        return entries

    def get_esign_repo(self, filename_filter:str=None):
        return esign.ESignRepo(name=self.repo_id, id=self.repo_id, apps=self.get_esign_repo_entries(filename_filter))

class Git:
    @staticmethod
    def get_repo_from_url(url):
        git_re = re.search(r"(?:git@|https://)github.com[:/](.*)", url).groups()
        if not git_re: return None

        return GitRepo(git_re[0])