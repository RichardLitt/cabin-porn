#!/usr/bin/env python

'''
Sets the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads and puts into a
folder in the current directory.

Optional arguments:
  1. '-r', choose a random image from the current page
  2. '-i', choose a specific image by the page id
  3. 'path=BASE_DIR', choose a directory for the photos to be put into

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
parser.add_option("-i", "--image", dest="image",
                  type="int", default=0,
                  help="pick a specific cabin, by image id")
(options, args) = parser.parse_args()

# Create a directory for image storage
if options.base_dir:
  base_dir = options.base_dir
  if base_dir[-1] != '/':
    base_dir = base_dir + '/'
# If the base directory is not set, we use ./Pictures/Cabins instead
else:
  base_dir = os.path.dirname(os.path.realpath(__file__)) + '/Pictures/Cabins/'

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Set the root URL
url = "http://cabinporn.com"
if options.image:
  url = url + "/post/" + str(options.image)

# Grab the html
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

# Get a list of all of the images of cabins
cabins = []
for image in soup.find_all('img'):
  image_src = image.get('src')
  if not re.search("cabin_porn", image_src) and re.search("jpg|png", image_src):
    cabins.append({ "src" : str(image_src), "link": str(image.get('title')) })
    # print(image.get('src'))
    # print(image.get('title'))

# Choose one of the pictures to download. If random is flagged, pick one from
# the top page. Else, just choose the most recent.
if options.random_cabin:
  cabin = random.choice(cabins)
else:
  cabin = cabins[0]

# Local filename for the image is the descriptive post link
post_name = re.search('/post/(.+)$', cabin["link"]).group(1)
image_ext = os.path.splitext(cabin["src"])[1]

# eg: 12345-some-cool-place.jpg
image_file = post_name.replace('/', '-') + image_ext

# Previously, images were stored using the raw image name, so if an older image
# exists, just move the old file to the new location
old_file = cabin["src"].split('/')[-1]
if os.path.isfile(base_dir + old_file):
  os.rename(base_dir + old_file, base_dir + image_file)

# If the image has not already been downloaded, get it now
if not os.path.isfile(base_dir + image_file):
  urllib.urlretrieve(cabin["src"], base_dir + image_file)

# generate a fileURL for the desktop picture
file_url = NSURL.fileURLWithPath_(base_dir + image_file)

# get shared workspace
ws = NSWorkspace.sharedWorkspace()

# iterate over all screens
for screen in NSScreen.screens():
    # tell the workspace to set the desktop picture
    (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
                file_url, screen, ws.desktopImageOptionsForScreen_(screen), None)
