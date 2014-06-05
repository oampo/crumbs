from distutils.core import setup

config = {
     "name": "Crumbs",
     "description": "A Gist-backed kind-of CMS",
     "author": "Joe Turner",
     "author_email": "joe@oampo.co.uk",
     "version": "0.1",
     "packages": ["crumbs"],
     "scripts": ["bin/crumbs"],
}

setup(**config)
