Cabin Porn It
==========

Set the current screen to a cabin from CabinPorn.com.

Default is set to the most recent picture, which it downloads and puts into a
folder in the current directory.

To run: `python cabin-porn-it.py`.

You may also need to install bs4. That should be: `$ pip install BeautifulSoup4`.

Alternatively, if you want to set it up to be automatic:

```
chmod a+x cabin-porn-it.py
export PATH=$PATH:`pwd`
ln -s /path/to/cabin-porn-it.py /usr/bin/cabin
```

This will allow you to type `$ cabin` whenever you, you know, want a new cabin.

If you want it to happen a few times a day, type: `env EDITOR=nano crontab -e`. From there, enter in `* */3 * * * /path/to/cabin-porn-it.py`. Save and you should be good: it'll check every two hours if there is a new picture for you or not. If you want a random picture, just add an ` -r` at the end, of course.

_Requires_: Python 2.7+, Mac OSX Mavericks

Possible arguments:

* '-r', choose a random image from the current page
* '-i', choose a specific image by the post id
* 'path=BASE_DIR', choose a directory for the photos to be put into

This is a very simple script. It only works on Mac OSX Mavericks. It does not run itself, although setting a cron job up is totally possible. I just wanted a way to do this automatically. PRs accepted but not expected.
