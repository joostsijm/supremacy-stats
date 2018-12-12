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

// Copy third party libraries from /node_modules into /app/static/app/static/vendor
gulp.task('vendor', function() {

	// Bootstrap
	gulp.src([
		'node_modules/bootstrap/dist/**/*',
		'!node_modules/bootstrap/dist/css/bootstrap-grid*',
		'!node_modules/bootstrap/dist/css/bootstrap-reboot*'
	])
		.pipe(gulp.dest('app/static/vendor/bootstrap'));

	// DataTables
	gulp.src([
		'node_modules/datatables.net/js/*.js',
		'node_modules/datatables.net-bs4/js/*.js',
		'node_modules/datatables.net-bs4/css/*.css',
		'node_modules/datatables.net-responsive/js/*'
	])
		.pipe(gulp.dest('app/static/vendor/datatables/'));

	// Amchart
	gulp.src([
		'node_modules/amcharts3/amcharts/themes/*.js',
		'node_modules/amcharts3/amcharts/*.js',
	])
		.pipe(gulp.dest('app/static/vendor/amcharts3/'));

	// Amchart
	gulp.src([
		'node_modules/amcharts3/amcharts/images/*.svg',
	])
		.pipe(gulp.dest('app/static/vendor/amcharts3/images'));

	// Font Awesome
	gulp.src([
		'node_modules/font-awesome/**/*',
		'!node_modules/font-awesome/{less,less/*}',
		'!node_modules/font-awesome/{scss,scss/*}',
		'!node_modules/font-awesome/.*',
		'!node_modules/font-awesome/*.{txt,json,md}'
	])
		.pipe(gulp.dest('app/static/vendor/font-awesome'));

	// jQuery
	gulp.src([
		'node_modules/jquery/dist/*',
		'!node_modules/jquery/dist/core.js'
	])
		.pipe(gulp.dest('app/static/vendor/jquery'));

	// jQuery Easing
	gulp.src([
		'node_modules/jquery.easing/*.js'
	])
		.pipe(gulp.dest('app/static/vendor/jquery-easing'));

	// Minify vendor js
	gulp.src([
		'app/static/vendor/**/*.js',
		'!app/static/vendor/**/*.min.js'
	])
		.pipe(uglify())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(gulp.dest('app/static/vendor'))

	// Minify vendor css
	gulp.src([
		'app/static/vendor/**/*.css',
		'!app/static/vendor/**/*.min.css'
	])
		.pipe(cleanCSS())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(gulp.dest('app/static/vendor'))
});

// Compile SASS 
gulp.task('css:compile', function() {
	return gulp.src('app/static/sass/**/*.sass')
		.pipe(sass.sync({
			outputStyle: 'expanded'
		}).on('error', sass.logError))
		.pipe(rename({
			suffix: '.compiled'
		}))
		.pipe(gulp.dest('app/static/css'));
});

// Minify CSS
gulp.task('css:minify', function() {
	return gulp.src([
		'app/static/css/**/*.css',
		'!app/static/css/**/*.min.css'
	])
		.pipe(cleanCSS())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(gulp.dest('app/static/css'))
		.pipe(browserSync.stream({match: 'app/static/css/**/*.css'}));
});

// CSS
gulp.task('css', gulp.parallel('css:compile', 'css:minify'));

// Minify JavaScript
gulp.task('js', function() {
	return gulp.src([
		'app/static/js/**/*.js',
		'!app/static/js/**/*.min.js'
	])
		.pipe(uglify())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(gulp.dest('app/static/js'))
		.pipe(browserSync.stream());
});

// Default task
gulp.task('default', gulp.parallel('vendor', 'css', 'js'));

// Configure the browserSync task
gulp.task('browserSync', function() {
	browserSync.init({
		notify: false,
		proxy: '127.0.0.1:5000',
		open: false
	});
});

//Run Flask server
gulp.task('runserver', function() {
	exec('flask run');
});

// Dev task
gulp.task('dev', gulp.series(gulp.parallel('runserver', 'browserSync'), function() {
	gulp.watch([
		'app/templates/**/*.html',
		'app/**/*.py',
	], browserSync.reload);
	gulp.watch([
		'app/static/sass/**/*.sass',
	], ['css:compile', browserSync.reload]);
	gulp.watch([
		'app/static/css/**/*.css',
		'!app/static/css/**/*.min.css',
	], ['css:minify', browserSync.reload]);
	gulp.watch([
		'app/static/js/**/*.js',
		'!app/static/js/**/*.min.js'
	], ['js', browserSync.reload]);
}));
