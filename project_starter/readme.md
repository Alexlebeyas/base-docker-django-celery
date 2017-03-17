# ![Nixa](https://nixaca.s3.amazonaws.com/static/nixa2/images/logo-nixa.png)

### PROJECT
**[Copy your pip configuration file](#markdown-header-copy-your-pip-configuration-file)**      
**[Build docker containers](#markdown-header-build-docker-containers)**          
**[Start web instance](#markdown-header-start-web-instance)**          
**[Start gulp instance](#markdown-header-start-gulp-instance)**          


### Copy your pip configuration file
1. Your file must be located in ~.pip/pip.conf
2. Copy it in the project at root (this file is ignore)
3. It must contains:
~~~~
[global]
; Extra index to private pypi dependencies
extra-index-url = https://{{ USERNAME }}:{{ PASSWORD }}@{{ NIXA_HOST }}/simple/
trusted-host = {{ NIXA_HOST }}
~~~~

### Build docker containers
1. Build docker containers: 
~~~~
sudo docker-compose build
~~~~
2. This will set up the instance for gulp and web instances.

### Start web instance
1. Make web startup, **only the first time**:
~~~~
sudo docker-compose up web-startup
~~~~
2. Startup docker instance:
~~~~
sudo docker-compose up web
~~~~

### Start gulp instance
1. Startup docker instance:
~~~~
sudo docker-compose up gulp
~~~~
2. The first time will be longer, because it install node modules.