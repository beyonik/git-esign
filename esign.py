from dataclasses import dataclass

@dataclass
class ESignRepoEntry:
    name: str
    bundleIdentifier: str
    developerName: str
    subtitle: str
    version: str
    versionDate: str
    versionDescription: str
    downloadURL: str
    localizedDescription: str
    iconURL: str
    tintColor: str
    size: int
    beta: bool

@dataclass
class ESignRepo:
    name: str
    id: str
    apps: list[ESignRepoEntry]