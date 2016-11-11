'use strict';
var gulp = require('gulp');
var sass = require('gulp-ruby-sass');

// load plugins
var $ = require('gulp-load-plugins')();
var gutil = require('gulp-util');
var runSequence = require('run-sequence');
var pjson = require('./package.json');
var plumber = require('gulp-plumber');

var src_path = "";
var dest_path = "../apps/front/static/";

// paths to resources
var paths = {
  scss: src_path + 'scss/**/*.scss',
  scripts: src_path + 'js/**/*.js',
  main: src_path + 'js/main.js',
  modernizr: ['node_modules/gulp-modernizr/build/modernizr-custom.js'],
  vendors: ['node_modules/jquery/dist/jquery.js', 'node_modules/bootstrap-sass/assets/javascripts/bootstrap.js'],
  plugins: [''],
  cssvendors: [
  // Load Bootstrap
  'node_modules/bootstrap-sass/assets/stylesheets/bootstrap.scss',
  // Fontawesome
  'node_modules/font-awesome/scss/font-awesome.scss'
  ],
  cssplugins: [''],
  images: src_path + 'img/**/*',
  php: '**/*.php',
  css: '**/*.css',
  js: 'js/**/*.js',
  fontsvendors: ['node_modules/font-awesome/fonts/fontawesome-webfont.ttf', 'node_modules/font-awesome/fonts/fontawesome-webfont.woff',
            'node_modules/font-awesome/fonts/fontawesome-webfont.woff2', 'node_modules/font-awesome/fonts/fontawesome-webfont.eot', 'node_modules/font-awesome/fonts/fontawesome-webfont.svg']
};

// destinations for resources
var dest = {
  css: dest_path + 'css/',
  scripts: dest_path + 'js/',
  images: dest_path + 'img/',
  fonts: dest_path + 'fonts/'
};

// process scss file
gulp.task('styles', function () {
  return sass(paths.scss, {
      precision: 10
    })
    .pipe($.autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
    .on('error', sass.logError)
    .pipe(gulp.dest(dest.css))
    ;
});

// process vendors scss file
gulp.task('styles_vendors', function () {
  return sass(paths.cssvendors, {
      precision: 10
    })
    .pipe($.concat('vendors.css'))
    .pipe($.rename('vendors.css'))
    .on('error', sass.logError)
    .pipe(gulp.dest(dest.css))
    ;
});

// process plugins scss file
gulp.task('styles_plugins', function () {
  return sass(paths.cssplugins, {
      precision: 10
    })
    .pipe($.concat('plugins.css'))
    .pipe($.rename('plugins.css'))
    .on('error', sass.logError)
    .pipe(gulp.dest(dest.css))
    ;
});

// JSMAIN task is not used in Django project
// Uncomment it if you want to use for another type of project
// You also need to uncomment jsmain in watch task

// uglify, rename and move destination of the main.js file
// gulp.task('jsmain', function(){
//   return gulp.src(paths.main)
//     .pipe($.rename('main.js'))
//     .pipe(gulp.dest(dest.scripts))
// });

// Compress modernizer, concat, rename, move
gulp.task('jsmodernizr', function(){
  return gulp.src(paths.modernizr)
    .pipe($.concat('modernizr.js'))
    .pipe($.rename('modernizr.js'))
    .pipe(gulp.dest(dest.scripts))
});

// Combine vendors js, concat, rename, move
gulp.task('jsvendors', function(){
  return gulp.src(paths.vendors)
    .pipe($.concat('vendors.js'))
    .pipe($.rename('vendors.js'))
    .pipe(gulp.dest(dest.scripts))
});


// Combine plugins js, concat, rename, move
gulp.task('jsplugins', function(){
  return gulp.src(paths.plugins)
    .pipe($.concat('plugins.js'))
    .pipe($.rename('plugins.js'))
    .pipe(gulp.dest(dest.scripts))
});

// Compress images
gulp.task('images', function () {
  return gulp.src(paths.images)
    .pipe($.cache($.imagemin({
      optimizationLevel: 3,
      progressive: true,
      interlaced: true
    })))
    .pipe(gulp.dest(dest.images))
});

gulp.task('fonts_vendors',function(){
   return gulp.src(paths.fontsvendors)
       .pipe(gulp.dest(dest.fonts))
});

// Clean up dist and temporary
gulp.task('clean', function(){
  return gulp.src(['.tmp', 'dist'], { read: false }).pipe($.clean());
});

gulp.task('build', ['styles', 'styles_vendors', 'jsmodernizr', 'jsplugins', 'jsvendors', 'images', 'fonts_vendors']);

gulp.task('default', ['clean'], function(){
  gulp.start('build');
});


gulp.task('watch', function(){
  gulp.watch(paths.scss, ['styles']);
  gulp.watch(paths.cssvendors, ['styles_vendors'])
  // gulp.watch(paths.main, ['jsmain']);
  gulp.watch(paths.images, ['images']);
});
