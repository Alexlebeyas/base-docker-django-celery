'use strict';

const gulp = require('gulp');
const util = require('gulp-util');

const babel = require('gulp-babel');
const babelify = require('babelify');
const es2015 = require('@babel/preset-env');

const browserify = require('browserify');
const streamify = require('gulp-streamify');
const source = require('vinyl-source-stream');
const sourcemaps = require('gulp-sourcemaps');
const watchify = require('watchify');
const rename = require('gulp-rename');
const minifycss = require('gulp-clean-css');
const sass = require('gulp-sass');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const es = require('event-stream');
const tap = require('gulp-tap');
const runSequence = require('run-sequence');
const buffer = require('vinyl-buffer');
const browserSync = require('browser-sync');
const reload = browserSync.reload;
const jshint = require('gulp-jshint');
const jshintSummary = require('jshint-stylish-summary');
const glob = require('glob');


/**
 *======================
 *     CDN
 * ======================
 */

/**
 * CDN Packages : https://cdnjs.com/libraries
 * Those modules can be install with npm, but it is encouraged to
 * call them in the web page with a CDN.
 *
 * If one of those packages needs to be import into one of your js file,
 * install it with npm and add the module name in the list excludedModules.
 *
 * Example of packages:
 * jquery
 * jqueryui
 * jquery.isotope
 * twitter-bootstrap
 * modernizer
 * gmap3 / gmap
 * bootstrap-datepicker
 * bootstrap-datetimepicker
 * */

const excludedModules = [
  'jquery'
];

/**
 *======================
 *     Paths
 * ======================
 */

const paths = {
  styles: {
    src: 'scss/**/*.scss',
    main: 'scss/main.scss',
    admin: 'scss/admin.scss',
    vendors: [''],
    dist: {
      css: '../apps/front/static/css/',
      admin: '../apps/custom_admin/static/custom_admin/css/'
    }
  },
  scripts: {
    src: '../apps/**/src/app*.js',
    resolveFile: '../apps/**/static/**/src/*.js',
    resolveDir: '../apps/**/static/**/src',
    dist: '../apps/front/static/js/app.min.js',
    sourceDir: 'src'
  },
  fonts: {
    vendors: [''],
    dist: '../apps/front/static/fonts/'
  }
};

const webServer = 'web';

/**
 *=======================
 *      JS
 * ======================
 */

var files = [];
var scripts = glob.sync(paths.scripts.resolveDir);

function browser(entry) {
  return browserify({
      entries: [entry],
      debug: true,
      paths: scripts.concat(['./node_modules']),
      cache: {}, packageCache: {}, fullPaths: true
    })
    .transform(babelify.configure({
        presets: [es2015]
      })
    ).external(excludedModules);
}

function watchBundle(bundler, entry) {
  return function () {
    return bundler.bundle()
      .on('error', function (err) {
        util.log(err);
        this.emit('end');
      })
      .pipe(source('app.js'))
      .pipe(buffer())
      .pipe(sourcemaps.init())
      .pipe(sourcemaps.mapSources('./'))
      .pipe(streamify(uglify()))
      .pipe(rename({extname: '.min.js'}))
      .pipe(sourcemaps.write('./'))
      .pipe(gulp.dest(function () {
        return entry.slice(0, entry.indexOf(paths.scripts.sourceDir) -1 ) + '/js';
      }));
  };
}

function loadfiles() {
  return gulp.src(paths.scripts.src)
    .pipe(tap(function (file) {
      files.push(file.path);
    }));
}

function startbrowserify(done) {
  var tasks = files.map(function (entry) {
    var bundler = watchify(browser(entry));
    var watch = watchBundle(bundler, entry);
    bundler.on('update', watch);
    bundler.on('log', util.log);
    return watch();
  });
  return es.merge(tasks), done();
}

function compilejs() {
  return gulp.src([paths.scripts.src])
    .pipe(sourcemaps.init())
    .pipe(concat('app.min.js'))
    .pipe(babel({
      "presets": ["@babel/preset-env"]
    }))
    .pipe(uglify())
    .on('error', function (err) { util.log(util.colors.red('[Error]'), err.toString()); })
    .pipe(gulp.dest(paths.scripts.dist));
}

// function lint() {
//   return gulp.src([paths.scripts.resolveFile, './gulpfile.js'])
//     .pipe(jshint('.jshintrc'))
//     .pipe(jshint.reporter('jshint-stylish'))
//     .pipe(jshintSummary.collect())
//     .on('end', jshintSummary.summarize());
// }
//
/**
 *=======================
 *      SASS / FONTS
 * ======================
 */

function styles() {
  return gulp.src([paths.styles.main])
    .pipe(sourcemaps.init())
    .pipe(sourcemaps.mapSources('./'))
    .pipe(sass({outputStyle: 'compact', sourceComments: 'map'}))
    .pipe(minifycss())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.styles.dist.css))
    .pipe(reload({stream: true}));
}

function cssadmin() {
  return gulp.src(paths.styles.admin, {sourcemap: true})
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(concat('admin.css'))
    .pipe(minifycss())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.styles.dist.admin));
}

/* to make this work, put stuff in paths.styles.vendors - but prioritise CDN! */
function cssvendors() {
  return gulp.src(paths.styles.vendors)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(concat('vendors.css'))
    .pipe(minifycss())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.styles.dist.css));
}

/* to make this work, put stuff in paths.fonts.vendors - but prioritise CDN! */
function fontsvendors() {
  return gulp.src(paths.fonts.vendors)
    .pipe(gulp.dest(paths.fonts.dist));
}

/**
 *=======================
 *      BUILD TASKS
 * ======================
 */

// function js() {
//   return gulp.parallel(
//     loadfiles,
//     compilejs
//   )
// }
//
//
// function startwatchify() {
//   return gulp.parallel(
//     loadfiles,
//     startbrowserify
//   )
// }
//

/* to make this work, put stuff in paths.styles.vendors paths.fonts.vendors - but prioritise CDN! */
function vendors(done) {
  return gulp.series(
    cssvendors,
    fontsvendors,
    (seriesDone) => {
      seriesDone();
      done();
  })();
}

function watchsass() {
  return gulp.watch(
      paths.styles.src,
      gulp.series(
          styles,
          cssadmin
      )
  );
}

// //
// gulp.task('watch', ['watch-sass', 'startwatchify'], browserSync.reload);
// //
// // gulp.task('browsersync', ['watch'], function () {
// //   browserSync({
// //     proxy: webServer + ':8000'
// //   });
// // });
// //
// // gulp.task('default', ['watch']);

/**
 *=======================
 *     GULP TASK LIST
 * ======================
 */

/* JS */
exports.loadfiles = loadfiles;
exports.startbrowserify = startbrowserify;
exports.compilejs = compilejs;
// exports.lint = lint;

/* SASS / FONTS */
exports.styles = styles;
exports.cssadmin = cssadmin;
exports.cssvendors = cssvendors;
exports.fontsvendors = fontsvendors;

/* BUILD TASKS */
// exports.js = js;
// exports.startwatchify = startwatchify;
exports.vendors = vendors;
exports.watchsass = watchsass;
