#!/usr/bin/env python3 
# vim: sts=4 sw=4 ai et
# PYTHON_ARGCOMPLETE_OK

# Copyright 2013 Alexey Kardapoltsev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json, sys, os
from vkdownloader import VkDownloader

arg_help_strings = {
    "user": "specify VK user id to log in as",
    "destdir": "specify destination directory to download to. Defaults to current directory",
    "clean_destdir": "clean destination directory before downloading",
    "friendlist_action": "Possible friendlist actions. Not much of them yet",
    "music_action": "All the things about music"
}

def process(section, action, user, **kwargs):
    if section == "music":
        if action in ("load", "dl"):
            vk.load(user, destdir, clean_destdir)
        elif action == "list":
            vk.show(user)
        elif action == "play":
            vk.play(user)
        else:
            print("Unknown action", file=sys.stderr)
    elif section == "friends":
        if action == "list":
            vk.show_friends(user)
        else:
            print("Unknown action", file=sys.stderr)

main_parser = argparse.ArgumentParser()

main_parser.add_argument("-u", "--user", metavar="user_id", help=arg_help_strings["user"])
subParsers = main_parser.add_subparsers(title="Command sections")
musicp = subParsers.add_parser("music", description="Actions related to music")
friendsp = subParsers.add_parser("friends", description="Actions related to friendlist")

friendsp.add_argument("action", help=arg_help_strings["friendlist_action"], choices=["list"])
friendsp.set_defaults(section="friends")

musicp.add_argument("action", help=arg_help_strings["music_action"],
        choices=["list", "load", "dl", "play"])
musicp.add_argument("-d", "--dest", "--destination", dest="destdir", help=arg_help_strings["destdir"])
musicp.add_argument("-c", "--clean", dest='clean_destdir', action='store_true', help=arg_help_strings["clean_destdir"])
musicp.set_defaults(clean_destdir=False)
musicp.set_defaults(destdir=os.getcwd())
musicp.set_defaults(section="music")

try:
    import argcomplete
    argcomplete.autocomplete(main_parser)
except ImportError:
    pass

args = main_parser.parse_args()
vk = VkDownloader()

try:
    process(**vars(args))
except AttributeError:
    print("Nothing specified, nothing to do.", file=sys.stderr)
    main_parser.print_help(file=sys.stderr)
    sys.exit(1)

