# Nixa Gulp (version 4.0.0)
When Docker is running, it will run the task browsersync by default. So there is no need to start gulp manually, exept if the docker is not running or if its broken.

## Install gulp to run it manually
To install gulp, go with the terminal inside the gulp folder, and then run npm install.
~~~~
cd PROJECT/gulp/

npm install
~~~~

## Gulp Tasks

### Styles
- ```gulp watch-sass``` : Watches SASS' folders and runs styles task.
- ```gulp styles```     : Compiles the styles.
- ```gulp vendors```    : Compiles vendor fonts and css 

### Scripts
- ```gulp watchify``` : Watches JS' folders and babelify the es6 js
- ```gulp lint```     : Checks the js files for any warnings and errors

#### Watchify explained
This task watch over all the main .js file (app.js or app.es6.js) in a static/**/src/ directory.
Only the app.js is compile, so every other js script written needs to be implemented in the app.js of his Django app.
Browserify will import all the required files into app.js in the compile version.
This task uses babel to compile es6 Js into the browser-compatible Js.
The compiled js files are placed in the static/js directory of their Django app under the name app.min.js

### Global
- ```gulp watch```       : Watches the Js and the Sass, this is the default task of gulpfile
- ```gulp browsersync``` : Watches the Js and the Sass, run browsersync for live reload

## CDN and Nodes Modules

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
