from datetime import datetime

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")

    login: str


class PullRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    number: int
    title: str
    html_url: str
    user: User
    created_at: datetime
    updated_at: datetime
    mergeable: bool | None = None


class Issue(BaseModel):
    model_config = ConfigDict(extra="ignore")

    number: int
    title: str
    html_url: str
    user: User
    created_at: datetime
    updated_at: datetime
    comments: int


class CommitAuthor(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    date: datetime


class CommitDetails(BaseModel):
    model_config = ConfigDict(extra="ignore")

    message: str
    author: CommitAuthor


class Commit(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sha: str
    html_url: str
    commit: CommitDetails
