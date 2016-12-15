var gulp = require('gulp'),
  plumber = require('gulp-plumber'),
  rename = require('gulp-rename'),
  autoprefixer = require('gulp-autoprefixer'),
  minifycss = require('gulp-clean-css'),
  sass = require('gulp-sass'),
  browserSync = require('browser-sync'),
  concat = require('gulp-concat'),
  reload = browserSync.reload,
  paths = {
    src: 'scss/**/*.scss',
    jsvendors: ['node_modules/jquery/dist/jquery.js', 'node_modules/bootstrap-sass/assets/javascripts/bootstrap.js'],
    cssvendors: ['vendors/bootstrap.scss','node_modules/font-awesome/scss/font-awesome.scss'],
    fontsvendors: ['node_modules/font-awesome/fonts/fontawesome-webfont.ttf', 'node_modules/font-awesome/fonts/fontawesome-webfont.woff',
              'node_modules/font-awesome/fonts/fontawesome-webfont.woff2', 'node_modules/font-awesome/fonts/fontawesome-webfont.eot', 'node_modules/font-awesome/fonts/fontawesome-webfont.svg']
  },
  dest = {
    css: '../dest/css/',
    scripts: '../dest/js/',
    fonts: '../dest/fonts/'
  };

gulp.task('styles', function(){
  gulp.src([paths.src], { sourcemap: true })
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(sass())
    .pipe(autoprefixer('last 2 versions'))
    //.pipe(minifycss())
    .pipe(gulp.dest(dest.css))
    .pipe(reload({ stream:true }));
});

gulp.task('cssvendors', function(){
  gulp.src(paths.cssvendors, { sourcemap: true })
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(sass())
    .pipe(concat('vendors.css'))
    .pipe(rename('vendors.css'))
    .pipe(autoprefixer('last 2 versions'))
    .pipe(minifycss())
    .pipe(gulp.dest(dest.css));
});

gulp.task('jsvendors', function(){
  gulp.src(paths.jsvendors)
    .pipe(concat('vendors.js'))
    .pipe(rename('vendors.js'))
    .pipe(gulp.dest(dest.scripts));
});

gulp.task('fontsvendors', function(){
  gulp.src(paths.fontsvendors)
    .pipe(gulp.dest(dest.fonts));
});

gulp.task('browsersync', function(){
  gulp.styles;
  browserSync({
    proxy: "127.0.0.1:8000"
  });
  gulp.watch(paths.src, ['styles']);
});

gulp.task('vendors', ['cssvendors', 'jsvendors', 'fontsvendors']);

gulp.task('default', function(){
  gulp.styles;
  gulp.watch(paths.src, ['styles']);
});

