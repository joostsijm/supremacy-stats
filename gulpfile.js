var gulp = require('gulp');
var sass = require('gulp-sass');
var header = require('gulp-header');
var cleanCSS = require('gulp-clean-css');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var beautify = require('gulp-html-beautify');
var pkg = require('./package.json');
var browserSync = require('browser-sync').create();
var exec = require('child_process').exec;

// Set the banner content
var banner = ['/*!\n',
    ' * Start Bootstrap - <%= pkg.title %> v<%= pkg.version %> (<%= pkg.homepage %>)\n',
    ' * Copyright 2013-' + (new Date()).getFullYear(), ' <%= pkg.author %>\n',
    ' * Licensed under <%= pkg.license %> (https://github.com/BlackrockDigital/<%= pkg.name %>/blob/master/LICENSE)\n',
    ' */\n',
    ''
].join('');

// Copy third party libraries from /node_modules into /app/static/app/static/vendor
gulp.task('vendor', function() {

    // Bootstrap
    gulp.src([
        './node_modules/bootstrap/dist/**/*',
        '!./node_modules/bootstrap/dist/css/bootstrap-grid*',
        '!./node_modules/bootstrap/dist/css/bootstrap-reboot*'
    ])
        .pipe(gulp.dest('./app/static/vendor/bootstrap'));

    // ChartJS
    gulp.src([
        './node_modules/chart.js/dist/*.js'
    ])
        .pipe(gulp.dest('./app/static/vendor/chart.js'));

    // DataTables
    gulp.src([
        './node_modules/datatables.net/js/*.js',
        './node_modules/datatables.net-bs4/js/*.js',
        './node_modules/datatables.net-bs4/css/*.css'
    ])
        .pipe(gulp.dest('./app/static/vendor/datatables/'));

    // Font Awesome
    gulp.src([
        './node_modules/font-awesome/**/*',
        '!./node_modules/font-awesome/{less,less/*}',
        '!./node_modules/font-awesome/{scss,scss/*}',
        '!./node_modules/font-awesome/.*',
        '!./node_modules/font-awesome/*.{txt,json,md}'
    ])
        .pipe(gulp.dest('./app/static/vendor/font-awesome'));

    // jQuery
    gulp.src([
        './node_modules/jquery/dist/*',
        '!./node_modules/jquery/dist/core.js'
    ])
        .pipe(gulp.dest('./app/static/vendor/jquery'));

    // jQuery Easing
    gulp.src([
        './node_modules/jquery.easing/*.js'
    ])
        .pipe(gulp.dest('./app/static/vendor/jquery-easing'));
});

// Compile SCSS
gulp.task('css:compile', function() {
    return gulp.src('./app/static/scss/**/*.scss')
        .pipe(sass.sync({
            outputStyle: 'expanded'
        }).on('error', sass.logError))
        .pipe(gulp.dest('./app/static/css'));
});

// Minify CSS
gulp.task('css:minify', ['css:compile'], function() {
    return gulp.src([
        './app/static/css/*.css',
        '!./app/static/css/*.min.css'
    ])
        .pipe(cleanCSS())
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(gulp.dest('./app/static/css'))
        .pipe(browserSync.stream());
});

// CSS
gulp.task('css', ['css:compile', 'css:minify']);

// Minify JavaScript
gulp.task('js', function() {
    return gulp.src([
        './app/static/js/*.js',
        '!./app/static/js/*.min.js'
    ])
        .pipe(uglify())
        .pipe(rename({
            suffix: '.min'
        }))
        .pipe(gulp.dest('./app/static/js'))
        .pipe(browserSync.stream());
});

// Default task
gulp.task('default', ['css', 'js', 'vendor']);

// Configure the browserSync task
gulp.task('browserSync', function() {
    browserSync.init({
        notify: false,
        proxy: '127.0.0.1:5000',
    });
});

//Run Flask server
gulp.task('runserver', function() {
    exec('pipenv run ./start.sh');
});

// Dev task
gulp.task('dev', ['runserver', 'css', 'js', 'vendor', 'browserSync'], function() {
    gulp.watch([
        './app/templates/*/*.html',
        './app/*.py',
    ], browserSync.reload);
    gulp.watch('./app/static/scss/**/*.scss', ['css']);
    gulp.watch('./app/static/js/*.js', ['js']);
});
