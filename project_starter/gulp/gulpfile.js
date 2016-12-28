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
    main: 'scss/main.scss',
    admin: 'scss/admin.scss',
    jsvendors: ['node_modules/jquery/dist/jquery.js', 'node_modules/bootstrap-sass/assets/javascripts/bootstrap.js'],
    cssvendors: ['vendors/bootstrap.scss','node_modules/font-awesome/scss/font-awesome.scss'],
    fontsvendors: ['node_modules/font-awesome/fonts/fontawesome-webfont.ttf', 'node_modules/font-awesome/fonts/fontawesome-webfont.woff',
              'node_modules/font-awesome/fonts/fontawesome-webfont.woff2', 'node_modules/font-awesome/fonts/fontawesome-webfont.eot', 'node_modules/font-awesome/fonts/fontawesome-webfont.svg']
  },
  dest = {
    css: '../apps/front/static/css/',
    admin: '../apps/custom_admin/static/custom_admin/css/',
    scripts: '../apps/front/static/js/',
    fonts: '../apps/front/static/fonts/'
  };

gulp.task('styles', function(){
  gulp.src([paths.main], { sourcemap: true })
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

gulp.task('cssadmin', function(){
  gulp.src(paths.admin, { sourcemap: true })
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(sass())
    .pipe(concat('admin.css'))
    .pipe(rename('admin.css'))
    .pipe(autoprefixer('last 2 versions'))
    .pipe(minifycss())
    .pipe(gulp.dest(dest.admin));
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

gulp.task('watch', ['default']);

gulp.task('default', function(){
  gulp.styles;
  gulp.cssadmin;
  gulp.watch(paths.src, ['styles', 'cssadmin']);
});

