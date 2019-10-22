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

# Frontend informations - CSS and JS

Both CSS and JS are compiled using [Gulp.js](https://gulpjs.com/ "Gulp.js documentation").
The gulp folder is located at the root of the projet. The gulpfile.js is located here: PROJECT/gulp/gulpfile.js

## 1 - CSS
SASS is used for the CSS. SASS files are located here: PROJECT/gulp/scss. To compile SASS into regular CSS, see point 3 - gulp.

## 2 - JS
We write JS with ES6 syntax, who is converted and minified.

## 3 - Nixa Gulp (version 4.0.0)
When Docker is running, it will run the task browsersync by default. So there is no need to start gulp manually, exept if the docker is not running or if its broken.

### Install gulp to run it manually
To install gulp, go with the terminal inside the gulp folder, and then run npm install.
~~~~
cd PROJECT/gulp/

npm install
~~~~

### Gulp Tasks

#### Styles
- ```gulp watch-sass``` : Watches SASS' folders and runs styles task.
- ```gulp styles```     : Compiles the styles.
- ```gulp vendors```    : Compiles vendor fonts and css

#### Scripts
- ```gulp watchify``` : Watches JS' folders and babelify the es6 js
- ```gulp lint```     : Checks the js files for any warnings and errors

##### Watchify explained
This task watch over all the main .js file (app.js or app.es6.js) in a static/**/src/ directory.
Only the app.js is compile, so every other js script written needs to be implemented in the app.js of his Django app.
Browserify will import all the required files into app.js in the compile version.
This task uses babel to compile es6 Js into the browser-compatible Js.
The compiled js files are placed in the static/js directory of their Django app under the name app.min.js

#### Global
- ```gulp watch```       : Watches the Js and the Sass, this is the default task of gulpfile
- ```gulp browsersync``` : Watches the Js and the Sass, run browsersync for live reload

### CDN and Nodes Modules

CDN Packages : https://cdnjs.com/libraries

Those modules can be install with npm, but it is encouraged to
call them in the web page with a CDN.

If one of those packages needs to be import into one of your js file,
install it with npm and add the module name in the list excludedModules.

Example of packages:
* jquery
* jqueryui
* jquery.isotope
* twitter-bootstrap
* modernizer
* gmap3 / gmap
* bootstrap-datepicker
* bootstrap-datetimepicker