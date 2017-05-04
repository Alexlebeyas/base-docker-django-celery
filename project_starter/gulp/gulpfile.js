'use strict';

const gulp = require('gulp');
const util = require('gulp-util');
const babelify = require('babelify');
const es2015 = require('babel-preset-es2015');
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
    vendors: ['vendors/bootstrap.scss', 'node_modules/font-awesome/scss/font-awesome.scss'],
    dist: {
      css: '../apps/front/static/css/',
      admin: '../apps/custom_admin/static/custom_admin/css/'
    }
  },
  scripts: {
    src: '../apps/**/src/app*.js',
    resolveFile: '../apps/**/static/**/src/*.js',
    resolveDir: '../apps/**/static/**/src',
    dist: 'static'
  },
  fonts: {
    vendors: ['node_modules/font-awesome/fonts/fontawesome-webfont.ttf', 'node_modules/font-awesome/fonts/fontawesome-webfont.woff',
      'node_modules/font-awesome/fonts/fontawesome-webfont.woff2', 'node_modules/font-awesome/fonts/fontawesome-webfont.eot', 'node_modules/font-awesome/fonts/fontawesome-webfont.svg'],
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
        return entry.slice(0, entry.indexOf(paths.scripts.dist) + paths.scripts.dist.length) + '/js';
      }));
  };
}

gulp.task('load-files', function () {
  return gulp.src(paths.scripts.src)
    .pipe(tap(function (file) {
      files.push(file.path);
    }));
});

gulp.task('browserify', function () {
  var tasks = files.map(function (entry) {
    var bundler = watchify(browser(entry));
    var watch = watchBundle(bundler, entry);
    bundler.on('update', watch);
    bundler.on('log', util.log);
    return watch();
  });
  return es.merge(tasks);
});

gulp.task('compileJs', function () {
  var tasks = files.map(function (entry) {
    var bundler = browser(entry);
    var bundle = watchBundle(bundler, entry);
    return bundle();
  });
  return es.merge(tasks);
});

gulp.task('lint', function () {
  return gulp.src([paths.scripts.resolveFile, './gulpfile.js'])
    .pipe(jshint('.jshintrc'))
    .pipe(jshint.reporter('jshint-stylish'))
    .pipe(jshintSummary.collect())
    .on('end', jshintSummary.summarize());
});

/**
 *=======================
 *      SASS / FONTS
 * ======================
 */

gulp.task('styles', function () {
  gulp.src([paths.styles.main])
    .pipe(sourcemaps.init())
    .pipe(sourcemaps.mapSources('./'))
    .pipe(sass({outputStyle: 'compact', sourceComments: 'map'}))
    .pipe(minifycss())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.styles.dist.css))
    .pipe(reload({stream: true}));
});

gulp.task('cssadmin', function () {
  gulp.src(paths.styles.admin, {sourcemap: true})
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(concat('admin.css'))
    .pipe(minifycss())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.styles.dist.admin));
});

gulp.task('cssvendors', function () {
  gulp.src(paths.styles.vendors)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(concat('vendors.css'))
    .pipe(minifycss())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.styles.dist.css));
});

gulp.task('fontsvendors', function () {
  gulp.src(paths.fonts.vendors)
    .pipe(gulp.dest(paths.fonts.dist));
});

/**
 *=======================
 *      BUILD TASKS
 * ======================
 */

gulp.task('js', function () {
  runSequence(
    'load-files',
    'compileJs'
  );
});

gulp.task('watchify', function () {
  runSequence(
    'load-files',
    'browserify'
  );
});

gulp.task('vendors', ['cssvendors', 'fontsvendors']);

gulp.task('watch-sass', ['styles', 'cssadmin'], function () {
  gulp.watch(paths.styles.src, ['styles', 'cssadmin']);
});

gulp.task('watch', ['watch-sass', 'watchify'], browserSync.reload);

gulp.task('browsersync', ['watch'], function () {
  browserSync({
    proxy: webServer + ':8000'
  });
});

gulp.task('default', ['watch']);
