# Crumbs - A Gist-backed kind-of CMS

Crumbs is a kind-of CMS which stores files as Gists.

## Usage:

Login to GitHub.

```
crumbs login
```

List all gists.

```
crumbs ls
```

List a specific gist.

```
crumbs ls gist_name
```

Add or update files in a gist.  Creates the gist if necessary.

```
crumbs add gist_name file_a.txt file_b.txt
```

Delete a gist.

```
crumbs rm gist_name
```

Delete files from a gist.

```
crumbs rm gist_name file_a.txt file_b.txt
```

Rename a gist.

```
crumbs mv old_gist_name new_gist_name
```

Add tags to a gist.

```
crumbs tag gist_name tag_a tag_b
```

Remove tags from a gist.

```
crumbs rmtag gist_name tag_a tag_b
```

Find gists which contain all of the tags.

```
crumbs search tag_a tag_b
```

Download a Gist to a folder named `gist_name`.

```
crumbs fetch gist_name - Download a gist_name
```

Download files from a Gist to the current folder.

```
crumbs fetch gist_name file_a.txt file_b.txt
```

Edit a single file within a Gist.

```
crumbs edit gist_name file.txt - Edit a file
```
