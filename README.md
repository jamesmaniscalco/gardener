# gardener
Raspberry Pi / Flask automatic plant waterer.

## Requirements:
This uses python 3.5, the default python for Raspbian (as of 2019-01-27).

See `requirements.txt` for python package requirements.

## Running:
To run the app, you first need to tell Flask where to find the app. In the `gardener` directory run the following:

```
$> export FLASK_APP=app  
$> flask run
```

## Setup on the Pi
Start by cloning the repo remotely.

[Set up Github SSH keys](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-linux).

Then run:

```
$> git clone git@github.com:jamesmaniscalco/gardener
```

## Access web interface remotely:
To start with, I'm using Dataplicity to access the web interface. I want to use nginx/gunicorn. Here's what I run on the Pi to get it working.

I followed the beginning of [this blog post](https://www.e-tinkers.com/2018/08/how-to-properly-host-flask-application-with-nginx-and-guincorn/), just the part about installing nginx and making modifications to the http and event blocks in the nginx configuration file, detailed in the "Setup Nginx" section.
