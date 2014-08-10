Cabin Porn It
==========

Set the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads and puts into a
folder in the current directory.

To run: `python cabin-porn-it.py`.

Possible arguments:
  1. '-r', choose a random image from the current page
  2. 'path=BASE_DIR', choose a directory for the photos to be put into

This is a very simple script. It sets the current picture. It doesn't look through the CP archives. It only works on Mac OSX Mavericks. It does not run itself, although setting a cron job up is totally possible. You need to specify random if you want a different base dir (of course, you could also just edit the file.)

I just wanted a way to do this automatically. And I've got that. PRs accepted but not expected.

Based originally on code to set desktop pictures for all screens from:
https://github.com/grahamgilbert/macscripts/tree/master/set_desktops