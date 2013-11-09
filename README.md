# autopull

Small Python web app to track remote Git repository changes and automatically pull them. Useful for small autodeploying projects.

Compatible with Bitbucket and GitHub.

## Installation on Ubuntu

### Prerequisites

Make sure you have all the following software installed on your system:

- git
- python
- python-virtualenv (optional)
- uwsgi
- uwsgi-plugin-python
- nginx

Configuration of [uWSGI](http://projects.unbit.it/uwsgi) and [nginx](http://nginx.org) described below.

### Configuring

1. Clone this repo to your machine.

2. Go to the repo dir, make virtual environment for Python and activate it. You may skip this step if you don't need this.
>$ cd /path/to/autopull  
>$ virtualenv .env  
>$ source .env/bin/activate

3. Install [Bottle](http://bottlepy.org) framework.
>$ pip install bottle

4. Deactivate virtualenv. Skip this step if you skipped step 2.
>$ deactivate

5. Make a copy of `repositories.json.example` with name `repositories.json` and configure your repositories you want to track.

6. Make sure you set up authorization via SSH-keys.

### Configuring uWSGI

1. Install it.
>$ sudo aptitude install uwsgi uwsgi-plugin-python

2. Make configuration file for multiple interpreter mode for a local user. This user should have write permissions to local repositories.
>$ cd /etc/uwsgi/apps-available/  
>$ sudo sh -c "echo \"[uwsgi]  
>plugins=python  
>uid=username  
>gid=groupname  
>chown-socket=root:root  
>chmod-socket=666  
>umask=002  
>home=/path/to/autopull/.env/  
>chdir=/path/to/autopull/  
>module=autopull.wsgi:application\" > autopull.ini"  
>$ cd /etc/uwsgi/apps-enabled/  
>$ sudo ln -s ../apps-available/autopull.ini

3. Restart uWSGI.
>$ sudo service uwsgi restart

### Configuring nginx

1. Install it.
>$ sudo aptitude install nginx

2. Make configuration file for virtual host.
>$ cd /etc/nginx/sites-available/  
>$ sudo sh -c "echo \"server {  
>server_name yoursite.com;  
>listen 8080;  
>location / {  
>uwsgi_pass unix:/var/run/uwsgi/app/autopull/socket;  
>include uwsgi_params;  
>}  
>}\" > yoursite.com.conf"  
>$ cd /etc/nginx/sites-enabled/  
>$ sudo ln -s ../sites-available/yoursite.com.conf

3. Restart nginx.
>$ sudo service nginx restart

## Configuring GitHub and Bitbucket

To make GitHub or Bitbucket notify autopull about changes do the following:

1. Open repository settings.

2. Click `Service Hooks` on GitHub or `Services` on Bitbucket.

3. Click `WebHook URLs` on GitHub or select `POST` on Bitbucket.

4. Enter `http://yoursite.com:8080` and enjoy.
