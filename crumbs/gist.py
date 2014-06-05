import os.path
import json
from urlparse import urlparse

import requests

from urls import *

def parse_description(gist):
    if gist["description"] == None:
        gist["title"] = ""
        gist["tags"] = []
        return

    split = gist["description"].split("#")
    title = split[0].strip()
    tags = split[1:]
    tags = [tag.strip() for tag in tags]

    gist["title"] = title
    gist["tags"] = tags

def get_gists(auth):
    url = LIST_GISTS_URL.format(user=auth["username"])
    params = {
        "page": 1,
        "per_page": 100,
        "access_token": auth["token"]
    }

    gists = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print response.json()["message"]
            break
        new_gists = response.json()
        if not len(new_gists):
            break
        gists += new_gists
        params["page"] += 1

    for gist in gists:
        parse_description(gist)
    gists = [gist for gist in gists if "crumbs" in gist["tags"]]
    return gists

def get_gist(auth, title):
    gists = get_gists(auth)
    try:
        gist = next(gist for gist in gists
                    if gist["id"] == title or gist["title"] == title)
    except StopIteration:
        raise KeyError("Could not find Gist")
    return gist

def add_gist(auth, title, filenames):
    url = CREATE_GIST_URL
    params = {
        "access_token": auth["token"]
    }

    files = {}
    for filename in filenames:
        with open(filename, "r") as f:
            files[os.path.basename(filename)] = {"content": f.read()}

    description = "{} {}".format(title.strip(), "#crumbs")

    data = {
        "files": files,
        "description": description,
        "public": True
    }

    response = requests.post(url, data=json.dumps(data), params=params)
    if response.status_code != 201:
        response.raise_for_status()

    return response.json()

def remove_gist(auth, title):
    gist = get_gist(auth, title)

    url = DELETE_GIST_URL.format(id=gist["id"])
    params = params = {
        "access_token": auth["token"]
    }
    response = requests.delete(url, params=params)
    if response.status_code != 204:
        response.raise_for_status()

    return None

def add_files(auth, title, filenames):
    gist = get_gist(auth, title)

    url = EDIT_GIST_URL.format(id=gist["id"])
    params = {
        "access_token": auth["token"]
    }

    files = {}
    for filename in filenames:
        with open(filename, "r") as f:
            files[os.path.basename(filename)]  = {"content": f.read()}

    data = {"files": files}

    response = requests.patch(url, data=json.dumps(data), params=params)
    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def remove_files(auth, title, filenames):
    gist = get_gist(auth, title)

    url = EDIT_GIST_URL.format(id=gist["id"])
    params = {
        "access_token": auth["token"]
    }

    files = {}
    for filename in filenames:
        filename = os.path.basename(filename)
        if filename in gist["files"]:
            files[filename]  = {"content": None}

    if not files:
        raise KeyError("Could not find files to remove")

    data = {"files": files}

    response = requests.patch(url, data=json.dumps(data), params=params)
    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

def rename_gist(auth, old_title, new_title):
    gist = get_gist(auth, old_title)
    gist["title"] = new_title

    url = EDIT_GIST_URL.format(id=gist["id"])
    params = {
        "access_token": auth["token"]
    }

    description = "{} #{}".format(gist["title"], " #".join(gist["tags"]))

    data = {
        "description": description
    }

    response = requests.patch(url, data=json.dumps(data), params=params)
    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

def tag_gist(auth, title, tags):
    gist = get_gist(auth, title)
    gist["tags"] = list(set(gist["tags"]) | set(tags))

    url = EDIT_GIST_URL.format(id=gist["id"])
    params = {
        "access_token": auth["token"]
    }

    description = "{} #{}".format(gist["title"], " #".join(gist["tags"]))

    data = {
        "description": description
    }

    response = requests.patch(url, data=json.dumps(data), params=params)
    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

def remove_tags(auth, title, tags):
    gist = get_gist(auth, title)
    gist["tags"] = list(set(gist["tags"]) - set(tags))

    url = EDIT_GIST_URL.format(id=gist["id"])
    params = {
        "access_token": auth["token"]
    }

    description = "{} #{}".format(gist["title"], " #".join(gist["tags"]))

    data = {
        "description": description
    }

    response = requests.patch(url, data=json.dumps(data), params=params)
    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

def fetch_from_gist(auth, title, filenames=None):
    gist = get_gist(auth, title)
    if not filenames:
        filenames = gist["files"].keys()
    else:
        filenames = list(set(gist["files"]) & set(filenames))

    files = {}
    for filename in filenames:
        url = gist["files"][filename]["raw_url"]
        parsed = urlparse(url)
        url = "https://cdn.rawgit.com" + parsed.path
        response = requests.get(url)

        if response.status_code != 200:
            response.raise_for_status()

        files[filename] = response.text
    return files

def write_file(auth, title, filename, content):
    gist = get_gist(auth, title)

    url = EDIT_GIST_URL.format(id=gist["id"])
    params = {
        "access_token": auth["token"]
    }

    files = {filename: {"content": content}}

    data = {"files": files}

    response = requests.patch(url, data=json.dumps(data), params=params)
    if response.status_code != 200:
        response.raise_for_status()

    return response.json()
