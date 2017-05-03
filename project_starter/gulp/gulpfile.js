"use strict";

const gulp = require("gulp");
const util = require("gulp-util");
const babelify = require("babelify");
const es2015 = require("babel-preset-es2015");
const browserify = require("browserify");
const streamify = require("gulp-streamify");
const source = require("vinyl-source-stream");
const sourcemaps = require("gulp-sourcemaps");
const watchify = require("watchify");
const plumber = require("gulp-plumber");
const rename = require("gulp-rename");
const autoprefixer = require("gulp-autoprefixer");
const minifycss = require("gulp-clean-css");
const sass = require("gulp-sass");
const concat = require("gulp-concat");
const uglify = require("gulp-uglify");
const es = require("event-stream");
const tap = require("gulp-tap");
const runSequence = require('run-sequence');
const path = require("path");
const buffer = require('vinyl-buffer');
const browserSync = require('browser-sync');
const reload = browserSync.reload;

/**
 *======================
 *     Paths
 * ======================
 */

const paths = {
    styles: {
        src: "scss/**/*.scss",
        main: "scss/main.scss",
        admin: "scss/admin.scss",
        vendors: ["vendors/bootstrap.scss", "node_modules/font-awesome/scss/font-awesome.scss"],
        dist: {
            css: "../apps/front/static/css/",
            admin: "../apps/custom_admin/static/custom_admin/css/"
        }
    },
    scripts: {
        src: "../apps/**/src/app*.js",
        dist: "static"
    },
    fonts: {
        vendors: ["node_modules/font-awesome/fonts/fontawesome-webfont.ttf", "node_modules/font-awesome/fonts/fontawesome-webfont.woff",
            "node_modules/font-awesome/fonts/fontawesome-webfont.woff2", "node_modules/font-awesome/fonts/fontawesome-webfont.eot", "node_modules/font-awesome/fonts/fontawesome-webfont.svg"],
        dist: "../apps/front/static/fonts/"
    }
};

const webServer = "web";

/**
 *=======================
 *      JS
 * ======================
 */

var files = [];

gulp.task("load-files", function () {
    return gulp.src(paths.scripts.src)
        .pipe(tap(function (file) {
            files.push(file.path);
        }));
});

gulp.task("browserify", function () {
    var tasks = files.map(function (entry) {

        var bundler = watchify(
            browserify({
                entries: [entry],
                debug: true,
                cache: {}, packageCache: {}, fullPaths: true
            }).transform(babelify, {presets: [es2015]})
        );
        var watch = watchBundle(bundler, entry);
        bundler.on("update", watch);
        bundler.on("log", util.log);
        return watch();
    });
    return es.merge(tasks);
});

function watchBundle(bundler, entry) {
    return function () {
        return bundler.bundle()
            .on('error',function (err) {
                    console.log(err);
                    this.emit('end');
                })
            .pipe(source("app.js"))
            .pipe(buffer())
            .pipe(sourcemaps.init())
            .pipe(streamify(uglify()))
            .pipe(rename({extname: ".min.js"}))
            .pipe(sourcemaps.write("./"))
            .pipe(gulp.dest(function () {
                return entry.slice(0, entry.indexOf(paths.scripts.dist) + paths.scripts.dist.length) + "/js";
            }));
    };
}

/**
 *=======================
 *      SASS / FONTS
 * ======================
 */

gulp.task("styles", function () {
    gulp.src([paths.styles.main])
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: "compact", sourceComments: "map"}))
        .pipe(minifycss())
        .pipe(sourcemaps.write("./"))
        .pipe(gulp.dest(paths.styles.dist.css))
        .pipe(reload({stream: true}));
});

gulp.task("cssadmin", function () {
    gulp.src(paths.styles.admin, {sourcemap: true})
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(concat("admin.css"))
        .pipe(minifycss())
        .pipe(sourcemaps.write("./"))
        .pipe(gulp.dest(paths.styles.dist.admin));
});

gulp.task("cssvendors", function () {
    gulp.src(paths.styles.vendors)
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(concat("vendors.css"))
        .pipe(minifycss())
        .pipe(sourcemaps.write("./"))
        .pipe(gulp.dest(paths.styles.dist.css));
});

gulp.task("fontsvendors", function () {
    gulp.src(paths.fonts.vendors)
        .pipe(gulp.dest(paths.fonts.dist));
});

/**
 *=======================
 *      BUILD TASKS
 * ======================
 */

gulp.task('browsersync', ['styles'], function(){
  browserSync({
    proxy: webServer+":8000"
  });
  gulp.watch(paths.styles.src, ['styles']);
});

gulp.task("watchify", function () {
    runSequence(
        "load-files",
        "browserify"
    )
});

gulp.task('vendors', ['cssvendors', 'fontsvendors']);

gulp.task("watch-sass",  ["styles", "cssadmin"], function () {
    gulp.watch(paths.styles.src, ["styles", "cssadmin"]);
});

gulp.task("watch", ["watch-sass", "watchify"]);

gulp.task("default", ['watch']);
