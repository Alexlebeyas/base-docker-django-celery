# ![Nixa](https://nixaca.s3.amazonaws.com/static/nixa/images/logo-home.png)

# To create a new project from project-starter, follow these steps:

If your project will use nixa app, you need a pip configuration file
~~~~
cd ~
vim pip.conf
~~~~
Here is the content of pip.conf
~~~~
[global]
; Extra index to private pypi dependencies
extra-index-url = https://{{ USERNAME }}:{{ PASSWORD }}@pip.nixa.ca/simple/
~~~~

## 1. Create a new repo on bitbucket:
my-project.git

## 2. Create a new project based on project-starter:
~~~~
git clone git@bitbucket.org:nixateam/project-starter.git
cd project-starter
cp ~/pip.conf .
python install my-project
git init
git remote add origin git@bitbucket.org:nixateam/my-project.git
git pull origin master
git add .
git commit -m “project creation based on project-starter”
git push --set-upstream origin master
git flow init
git checkout develop
~~~~

## 3. Build docker containers:
Frist, check requirement.txt and then
~~~~
docker-compose build
~~~~

## 4. Start containers:
~~~~
docker-compose up
~~~~

## 5. Start project:
~~~~
docker exec -it my-project_web_1 bash
python manage.py startup
~~~~

### For more informations:
**[Copy your pip configuration file](#markdown-header-copy-your-pip-configuration-file)**      
**[Build docker containers](#markdown-header-build-docker-containers)**          
**[Start docker instance](#markdown-header-start-docker-instance)**       
**https://nixaca.atlassian.net/wiki/spaces/PB/pages/125041233/Ultimate+Starter+Guide+for+Django+Projects**