import os
import sys
import getpass
import json
import os.path
import tempfile
import subprocess

import appdirs
import requests
from requests.exceptions import HTTPError

import util
from urls import *
from gist import *


CONFIG_DIR = appdirs.user_config_dir("Crumbs", "oampo")
TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")

def login():
    username = raw_input("GitHub username: ")
    password = getpass.getpass("GitHub password: ")

    data = {
        "scopes": ["gist"],
        "note": "Crumbs"
    }
    response = requests.post(AUTHORIZATIONS_URL, data=json.dumps(data),
                            auth=(username, password))
    if response.status_code == 401 and "X-GitHub-OTP" in reponse.headers:
        tfa_code = raw_input("2-factor auth code: ")
        headers = {"X-GitHub-OTP": tfa_code}
        response = requests.post(AUTHORIZATIONS_URL, data=json.dumps(data),
                                headers=headers, auth=(username, password))

    if response.status_code == 201:
        util.make_directory(CONFIG_DIR)
        with open(TOKEN_FILE, "w") as f:
            data = {"username": username,
                    "token": response.json()["token"]}
            json.dump(data, f)
        print "Login successful"
    else:
        print "Error: {}".format(response.json()["message"])

def get_auth():
    with open(TOKEN_FILE, "r") as f:
        auth = json.load(f)
        return auth

def print_gist(gist):
    print "{}".format(gist["title"]),
    for tag in gist["tags"]:
        if tag == "crumbs":
            continue
        print "#{}".format(tag),
    print "({})".format(gist["id"])

    for file in gist["files"]:
        print "- {}".format(file)

def ls(gist_name=None):
    auth = get_auth()

    if gist_name:
        gist = get_gist(auth, gist_name)
        gists = [gist]
    else:
        gists = get_gists(auth)

    for gist in gists:
        print_gist(gist)
        if gist != gists[-1]:
            print ""

def add(gist_name, filenames):
    auth = get_auth()
    try:
        gist = get_gist(auth, gist_name)
    except KeyError:
        gist = add_gist(auth, gist_name, filenames)
    else:
        gist = add_files(auth, gist_name, filenames)

def rm(gist_name, filenames):
    auth = get_auth()
    if not len(filenames):
        remove_gist(auth, gist_name)
    else:
        remove_files(auth, gist_name, filenames)

def mv(old_gist_name, new_gist_name):
    auth = get_auth()
    rename_gist(auth, old_gist_name, new_gist_name)

def tag(gist_name, tags):
    auth = get_auth()
    tag_gist(auth, gist_name, tags)


def rmtag(gist_name, tags):
    auth = get_auth()
    remove_tags(auth, gist_name, tags)

def search(tags):
    auth = get_auth()
    gists = get_gists(auth)

    gists = [gist for gist in gists if set(tags) <= set(gist["tags"])]
    for gist in gists:
        print_gist(gist)
        if gist != gists[-1]:
            print ""

def fetch(gist_name, filenames=None):
    auth = get_auth()
    files = fetch_from_gist(auth, gist_name, filenames)

    if not filenames:
        directory = gist_name
        util.make_directory(directory)
    else:
        directory = ""

    for filename in files:
        with open(os.path.join(directory, filename), "w") as f:
            f.write(files[filename])

def edit(gist_name, filename):
    auth = get_auth()
    files = fetch_from_gist(auth, gist_name, [filename])

    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile("r+") as f:
        f.write(files[filename])
        f.flush()
        subprocess.call([editor, f.name])
        f.seek(0)
        gist = write_file(auth, gist_name, filename, f.read())


