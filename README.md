# gardener
Raspberry Pi / Flask automatic plant waterer.

## Requirements:
This uses python 3.5, the default python for Raspbian (as of 2019-01-27).

See `requirements.txt` for python package requirements.

## Running locally:
To run the app, you first need to tell Flask where to find the app. In the `gardener` directory run the following:

```
$> export FLASK_APP=app  
$> flask run
```

Or run it with `gunicorn`:

```
gunicorn -c gunicorn_config.py wsgi:app
```

Note: to run with `gunicorn` as above you need to [follow the steps below](#environment-variables).

## Setup on the Pi:
Start by cloning the repo remotely.

[Set up Github SSH keys](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-linux).

Then run:

```
$> git clone git@github.com:jamesmaniscalco/gardener
```

`cd` into `gardener`. Create a python virtual environment:

```
$> python3 -m venv .
```

Install the required packages:

```
$> pip install -r requirements.txt
```


## Access web interface remotely:
To start with, I'm using Dataplicity to access the web interface. I want to use nginx/gunicorn. Here's what I run on the Pi to get it working.

I followed the beginning of [this blog post](https://www.e-tinkers.com/2018/08/how-to-properly-host-flask-application-with-nginx-and-guincorn/), just the part about installing nginx and making modifications to the http and event blocks in the nginx configuration file, detailed in the "Setup Nginx" section.

Next is the setup for the site itself. I followed these two posts:

- [How to Run Flask Applications with Nginx Using Gunicorn](http://www.onurguzel.com/how-to-run-flask-applications-with-nginx-using-gunicorn/)
- [Managing Gunicorn Processes With Supervisor](http://www.onurguzel.com/managing-gunicorn-processes-with-supervisor/)

For the first post above, I only really followed the middle section. On the Pi server I have the following in my `/etc/nginx/sites-available/gardener.conf`:

```
server {
    listen 80;
    server_name zaniest-dingo-8263.dataplicity.io;

    root /home/pi/code/gardener;

    access_log /home/pi/code/gardener/logs/access.log;
    error_log /home/pi/code/gardener/logs/error.log;

    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Then I symlinked this into the `sites-enabled` directory:

```
$> sudo ln -s /etc/nginx/sites-available/gardener.conf /etc/nginx/sites-enabled/
```

And I removed the existing link to the default site:

```
$> rm /etc/nginx/sites-enabled/default
```

Then reload `nginx`:

```
$> sudo service nginx reload
```

For `supervisord`, I have the following configuration in `/etc/supervisor/conf.d/gardener.conf`:

```
[program:gardener]
command = /home/pi/code/gardener/bin/python /home/pi/code/gardener/bin/gunicorn -c gunicorn_config.py wsgi:app
directory = /home/pi/code/gardener
user = pi
```

Here the `command` line ensures we are activating the python virtual environment.

Then I ran the following commands to update `supervisor` and get the server running automatically:

```
$> sudo supervisorctl reread
$> sudo supervisorctl update
$> sudo supervisorctl start gardener
```

Now the server should start automatically when the Pi reboots.

For the Dataplicity setup, I made an account and followed the directions there for getting started on the Raspberry Pi, then enabled the 'Wormhole' to my Pi. This exposes port 80 (where nginx is serving the gunicorn application) to the web. There is [information out there](https://www.digitalocean.com/community/tutorials/how-to-set-up-http-authentication-with-nginx-on-ubuntu-12-10) on setting up basic authentication for nginx. In the future maybe the app itself will have authentication.

## Environment variables
Copy the file `gunicorn_config_example.py` to `gunicorn_config.py` (the latter of which is not tracked by git) and update the environment variables as desired:

- `FLASK_ENV`: `production` or `development`. `development` simulates sensor input.



