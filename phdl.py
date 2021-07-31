#!/usr/bin/env python3

# phdl.py: single-handedly download and organize videos from a popular video sharing website
# Copyright (C) 2021 George Whiteside

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import configparser
import os
import time
import urllib.request

import watchdog.events
import watchdog.observers
import youtube_dl

from bs4 import BeautifulSoup

# handle bad directories, files instead of directories, links deleted before completion, etc.

ARGS = None

def main():
	"""Processes command line arguments, sets up file watchdog, and enters main loop."""
	global ARGS

	argparser = argparse.ArgumentParser(
		description="Saves some videos in a tidy directory structure"
	)

	argparser.add_argument(
		"--keeplinks",
		action="store_true",
		help="Don't delete shortcut files after download"
	)

	argparser.add_argument(
		"--watchdir",
		default=os.getcwd(),
		help="The directory that will be watched for new download links"
		     " [default: outdir]"
	)

	argparser.add_argument(
		"outdir",
		nargs="?",
		default=os.getcwd(),
		help="The root directory where saved videos will be organized"
		     " [default: ./]"
	)

	ARGS = argparser.parse_args()

	event_handler = watchdog.events.PatternMatchingEventHandler(
		["*.url"], None, True, False
	)

	event_handler.on_created = on_created

	observer = watchdog.observers.Observer()
	observer.schedule(event_handler, ARGS.watchdir, recursive=False)

	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

def on_created(event):
	"""Watchdog callback function handles shortcut files and downloads videos."""

	time.sleep(0.1) # there's no clean way to wait for file to write, so...

	# Windows internet shortcuts are a lot like Windows .ini files, which in
	# turn are a lot like Python ConfigParser configuration files, so I'm just
	# going to go ahead and jam this square peg in that rectangle hole

	config = configparser.ConfigParser()
	config.read(event.src_path)

	url = config['InternetShortcut']['URL']

	with urllib.request.urlopen(url) as page:
		soup = BeautifulSoup(page, 'html.parser')

	# select the anchor element containing the user name

	element = (soup
		.find("div", class_="userInfo")
		.div
		.a
	)

	username = element.get_text()
	dirname = element["href"].rsplit("/",1)[1]

	print(username)
	print(dirname)

	outpath = f'./{dirname}/'
	if not os.path.isdir(outpath):
		os.mkdir(outpath)

	ydl_opts = {
		'format': 'best[height=1080]/best[height=720]/best[height=480]/best',
		'outtmpl': f'{outpath}%(title)s.%(ext)s'
	}

	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
	except Exception:
		print("Something went wrong")
		return

	if not ARGS.keeplinks:
		os.remove(event.src_path)

if __name__ == "__main__":
	main()
