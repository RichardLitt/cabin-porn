Cabin Porn It
==========

Set the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads and puts into a
folder in the current directory.

PRs accepted but not expected.

###Installation

Download cabin-porn-it.py to wherever you want, or clone this entire repository.

To run: `python cabin-porn-it.py`.

You may also need to install bs4 and requests. To do so, run: `sudo pip install requests beautifulsoup4`.

_Requirements_: Python 2.7+, Mac OSX Mavericks

###Automate

Alternatively, if you want to set it up to be automatic:

```
chmod a+x cabin-porn-it.py
export PATH=$PATH:`pwd`
ln -s /path/to/cabin-porn-it.py /usr/bin/cabin
```

This will allow you to type `$ cabin` whenever you, you know, want a new cabin. Note: If you set this up, the base dir will be relative to your home folder. Adding in a complete path as the base directory will stop this from putting pictures into your base Pictures/ folder. For instance: `$ cabin path=/Users/richard/Pictures/cabins`. 

####Launchctl

If you want this to run automatically, put the `com.burntfen.cabin-porn-it.plist` file in your Library/LaunchAgents/ folder. plist files are the preferred way in Mac OSX of running cronjobs - using the native launchctrl program. Edit the file by adding a `<script>-r</script>` line if you want a random photo, and change the integer number to whatever amount of seconds you want (3600 is one hour). Then, run: 
`launchctl load ~/Library/LaunchAgent/com.burntfen.cabin-porn-it.plist`. For troubleshooting and more configuration options, see this [excellent explanation](http://stackoverflow.com/a/15820488/1166929) of launchctl. 

####Crontab
If you want to use the old crontab, type: `env EDITOR=nano crontab -e`. From there, enter in `* */3 * * * /path/to/cabin-porn-it.py`. Save and you should be good: it'll check every two hours if there is a new picture for you or not. If you want a random picture, just add an ` -r` at the end, of course.

###Options

* '-r', choose a random image from the current page
* '-i', choose a specific image by the post id
* 'path=BASE_DIR', choose a directory for the photos to be put into
