import argparse

def make_parser():
    """ Construct the command line parser """
    description = "A Gist-backed kind-of CMS"
    parser = argparse.ArgumentParser(prog="crumbs", description=description)

    subparsers = parser.add_subparsers(help="Available commands")

    make_login_subparser(subparsers)
    make_ls_subparser(subparsers)
    make_add_subparser(subparsers)
    make_rm_subparser(subparsers)
    make_mv_subparser(subparsers)
    make_tag_subparser(subparsers)
    make_rmtag_subparser(subparsers)
    make_search_subparser(subparsers)
    make_fetch_subparser(subparsers)
    make_edit_subparser(subparsers)

    return parser

def make_login_subparser(subparsers):
    parser = subparsers.add_parser("login",
                                   help="Log in to GitHub")
    parser.set_defaults(command="login")

def make_ls_subparser(subparsers):
    parser = subparsers.add_parser("ls",
                                   help="List gists and files")
    parser.add_argument("gist_name", nargs="?", help="The name of the gist")
    parser.set_defaults(command="ls")

def make_add_subparser(subparsers):
    parser = subparsers.add_parser("add",
                                   help="Add and update files")
    parser.add_argument("gist_name", help="The name of the gist")
    parser.add_argument("filenames", nargs="+", help="The name of the files")
    parser.set_defaults(command="add")

def make_rm_subparser(subparsers):
    parser = subparsers.add_parser("rm",
                                   help="Remove gists and files")
    parser.add_argument("gist_name", help="The name of the gist")
    parser.add_argument("filenames", nargs="*", help="The name of the files")
    parser.set_defaults(command="rm")

def make_mv_subparser(subparsers):
    parser = subparsers.add_parser("mv",
                                   help="Rename a gist")
    parser.add_argument("old_gist_name", help="The old name of the gist")
    parser.add_argument("new_gist_name", help="The new name of the gist")
    parser.set_defaults(command="mv")

def make_tag_subparser(subparsers):
    parser = subparsers.add_parser("tag",
                                   help="Add tags to a gist")
    parser.add_argument("gist_name", help="The name of the gist")
    parser.add_argument("tags", nargs="*", help="The tags to add")
    parser.set_defaults(command="tag")

def make_rmtag_subparser(subparsers):
    parser = subparsers.add_parser("rmtag",
                                   help="Remove tags from a gist")
    parser.add_argument("gist_name", help="The name of the gist")
    parser.add_argument("tags", nargs="*", help="The tags to remove")
    parser.set_defaults(command="rmtag")

def make_search_subparser(subparsers):
    parser = subparsers.add_parser("search",
                                   help="Find gists with certain tags")
    parser.add_argument("tags", nargs="+", help="The tags to remove")
    parser.set_defaults(command="search")

def make_fetch_subparser(subparsers):
    parser = subparsers.add_parser("fetch",
                                   help="Fetch files from a gist")
    parser.add_argument("gist_name", help="The name of the gist")
    parser.add_argument("filenames", nargs="*", help="The name of the files")
    parser.set_defaults(command="fetch")

def make_edit_subparser(subparsers):
    parser = subparsers.add_parser("edit",
                                   help="Edit a file")
    parser.add_argument("gist_name", help="The name of the gist")
    parser.add_argument("filename", help="The name of the file")
    parser.set_defaults(command="edit")

if __name__ == "__main__":
    main()
