#!/usr/bin/env python

'''
Sets the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads and puts into a
folder in the current directory.

Optional arguments:
  1. '-r', choose a random image from the current page
  2. '-i', choose a specific image by the page id
  3. '-l', limit files to images larger than 1024x748
  4. 'path=BASE_DIR', choose a directory for the photos to be put into

Based originally on code to set desktop pictures for all screens from:
https://github.com/grahamgilbert/macscripts/tree/master/set_desktops
'''

from bs4 import BeautifulSoup
from AppKit import NSWorkspace, NSScreen
from Foundation import NSURL
from optparse import OptionParser
import requests, glob, random, re, urllib, os, fnmatch, sys
from os import listdir
from os.path import isfile, join

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
parser.add_option("-l", "--large-only", dest="large_only",
                  help="only use large images", default=False,
                  action="store_true")
parser.add_option("-o", "--offline", dest="offline",
                  help="use offline", default=False,
                  action="store_true")
(options, args) = parser.parse_args()

# Create a directory for image storage
if options.base_dir:
  base_dir = options.base_dir
  if base_dir[-1] != "/":
    base_dir = base_dir + "/"
# If the base directory is not set, we use ./Pictures/Cabins instead
else:
  base_dir = os.path.dirname(os.path.realpath(__file__)) + "/Cabins/"

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Set the root URL
url = "http://cabinporn.com"
if options.image:
  url = url + "/post/" + str(options.image)

# Grab the html
r  = requests.get(url)
if r.status_code == 200:
  data = r.text
  soup = BeautifulSoup(data)

  # Get a list of all of the images of cabins
  cabins = []
  for photo in soup.find_all("div", "photo_div"):
    image = photo.find("img")
    image_src = str(image.get("src"))
    if re.search("jpg|png", image_src):
      link_str = str(image.get("title"))
      if link_str == "None":
        link_str = image.find_parent("li", "post").find("div", "fb-like").get("data-href")
      cabins.append({ "src" : image_src, "link": link_str })

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
elif r.status_code != 200:
  print('You are not connected to the internet. Choosing old cabin')

  # Select all of the cabins in the folder, and pick a random one
  cabins = [ f for f in listdir(base_dir) if isfile(join(base_dir, f)) ]
  image_file = random.choice(cabins)


def setFile():
  # generate a fileURL for the desktop picture
  file_path = NSURL.fileURLWithPath_(base_dir + image_file)

  # get shared workspace
  ws = NSWorkspace.sharedWorkspace()

  # iterate over all screens
  for screen in NSScreen.screens():
      # tell the workspace to set the desktop picture
      (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
                  file_path, screen, ws.desktopImageOptionsForScreen_(screen), None)

# Check the size of the file
if options.large_only:
  from PIL import Image
  im = Image.open(base_dir + image_file).size
  if im[0] >= 1024 and im[1] >= 768:
    print('Image is large:', im)
    setFile()
  else: 
    print('Image is too small:', im) # (width,height) tuple
else: 
  setFile()
