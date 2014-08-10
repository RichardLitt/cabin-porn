#!/usr/bin/python

'''
Sets the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads and puts into a
folder in the current directory.

Optional arguments:
  1. '-r', choose a random image from the current page
  2. 'path=BASE_DIR', choose a directory for the photos to be put into

Based originally on code to set desktop pictures for all screens from:
https://github.com/grahamgilbert/macscripts/tree/master/set_desktops
'''

from bs4 import BeautifulSoup
from AppKit import NSWorkspace, NSScreen
from Foundation import NSURL
from optparse import OptionParser
import requests, glob, random, re, urllib, os, fnmatch, sys

# Set the options
parser = OptionParser()
parser.add_option("-p", "--path", dest="base_dir",
                  help="write cabins to PATH", metavar="PATH")
parser.add_option("-r", "--random", action="store_true",
                  dest="random_cabin", default=False,
                  help="pick a random cabin")
(options, args) = parser.parse_args()

# Grab the html
r  = requests.get("http://cabinporn.com")
data = r.text
soup = BeautifulSoup(data)

# Get a list of all of the images of cabins
cabin_images = []
for image in soup.find_all('img'):
  image_src = image.get('src')
  if not re.search("cabin_porn", image_src) and re.search("jpg", image_src):
    cabin_images.append(str(image_src))
    # output.write("\"" +  credits_no.group(0) + "\",",)
    # print(image.get('src'))

# Choose one of the pictures to download. If random is flagged, pick one from
# the top page. Else, just choose the most recent.
if options.random_cabin:
  picture_path = random.choice(cabin_images)
else:
  picture_path = cabin_images[0]

# Isolate the filename
picture_name = picture_path.split('/')[-1]

# Create a directory for it. Set second arg as directory if given.
if options.base_dir:
  base_dir = options.base_dir
  if base_dir[-1] != '/':
    base_dir = base_dir + '/'
else:
  base_dir = './cabin-porn/'

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Download the file if you haven't already
if not os.path.isfile(base_dir + picture_name):
  urllib.urlretrieve(picture_path, base_dir + picture_name)

# generate a fileURL for the desktop picture
file_url = NSURL.fileURLWithPath_(base_dir + picture_name)

# make image options dictionary
# we just make an empty one because the defaults are fine
options = {}

# get shared workspace
ws = NSWorkspace.sharedWorkspace()

# iterate over all screens
for screen in NSScreen.screens():
    # tell the workspace to set the desktop picture
    (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
                file_url, screen, options, None)