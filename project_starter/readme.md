# ![Nixa](https://nixaca.s3.amazonaws.com/static/nixa2/images/logo-nixa.png)

### PROJECT
**[Copy your pip configuration file](#markdown-header-copy-your-pip-configuration-file)**      
**[Build docker containers](#markdown-header-build-docker-containers)**          
**[Start web instance](#markdown-header-start-web-instance)**          
**[Start gulp instance](#markdown-header-start-gulp-instance)**          


### Copy your pip configuration file
1. If you have not made a pip.config file on your user folder, you must make a new directory inside the user folder and call it ‘pip’. 
2. Inside this pip folder, create a file called ‘pip.conf’
3. Copy this file and put is inside the project folder
4. Take the following code and put it in the file, and replace the placeholder text (e.g. USERNAME, PASSWORD) with the appropriate information.
~~~~
[global]
; Extra index to private pypi dependencies
extra-index-url = https://{{ USERNAME }}:{{ PASSWORD }}@pip.nixa.ca/simple/
trusted-host = pip.nixa.ca
~~~~

### Build docker containers
1. Build docker containers: 
~~~~
docker-compose build
~~~~
2. This will set up the instance for gulp and web instances.

### Start web instance
1. Make web startup, **only the first time**:
~~~~
docker-compose up web-startup
~~~~
2. Startup docker instance:
~~~~
docker-compose up web
~~~~

### Start gulp instance
1. Startup docker instance:
~~~~
docker-compose up gulp
~~~~
2. The first time will be longer, because it install node modules.