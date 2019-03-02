const { series, parallel, task, src, dest } = require('gulp');
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

function vendor_export_bootstrap(cb) {
	src([
		'node_modules/bootstrap/dist/**/*',
		'!node_modules/bootstrap/dist/css/bootstrap-grid*',
		'!node_modules/bootstrap/dist/css/bootstrap-reboot*'
	])
		.pipe(dest('app/static/vendor/bootstrap'))
		.on('end', cb);
}

function vendor_export_datatables(cb) {
	src([
		'node_modules/datatables.net/js/*.js',
		'node_modules/datatables.net-bs4/js/*.js',
		'node_modules/datatables.net-bs4/css/*.css',
		'node_modules/datatables.net-responsive/js/*'
	])
		.pipe(dest('app/static/vendor/datatables/'))
		.on('end', cb);
}

function vendor_export_amchart(cb) {
	src([
		'node_modules/amcharts3/amcharts/themes/*.js',
		'node_modules/amcharts3/amcharts/*.js',
	])
		.pipe(dest('app/static/vendor/amcharts3/'))
		.on('end', cb);
}

function vendor_export_amchart_images(cb) {
	src([
		'node_modules/amcharts3/amcharts/images/*.svg',
	])
		.pipe(dest('app/static/vendor/amcharts3/images'))
		.on('end', cb);
}

function vendor_export_d3(cb) {
	src([
		'node_modules/d3/*.js',
	])
		.pipe(dest('app/static/vendor/d3/'))
		.on('end', cb);
}

function vendor_export_font_awesome(cb) {
	src([
		'node_modules/font-awesome/**/*',
		'!node_modules/font-awesome/{less,less/*}',
		'!node_modules/font-awesome/{scss,scss/*}',
		'!node_modules/font-awesome/.*',
		'!node_modules/font-awesome/*.{txt,json,md}'
	])
		.pipe(dest('app/static/vendor/font-awesome'))
		.on('end', cb);
}

function vendor_export_jquery(cb) {
	src([
		'node_modules/jquery/dist/*',
		'!node_modules/jquery/dist/core.js'
	])
		.pipe(dest('app/static/vendor/jquery'))
		.on('end', cb);
}

function vendor_export_jqurey_easing(cb) {
	src([
		'node_modules/jquery.easing/*.js'
	])
		.pipe(dest('app/static/vendor/jquery-easing'))
		.on('end', cb);
}

function vendor_minify_js(cb) {
	src([
		'app/static/vendor/**/*.js',
		'!app/static/vendor/**/*.min.js'
	])
		.pipe(uglify())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(dest('app/static/vendor'))
		.on('end', cb);
}

function vendor_minify_css(cb) {
	src([
		'app/static/vendor/**/*.css',
		'!app/static/vendor/**/*.min.css'
	])
		.pipe(cleanCSS())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(dest('app/static/vendor'))
		.on('end', cb);
}

// Compile SASS
function css_compile(cb) {
	src('app/static/sass/**/*.sass')
		.pipe(sass.sync({
			outputStyle: 'expanded'
		}).on('error', sass.logError))
		.pipe(rename({
			suffix: '.compiled'
		}))
		.pipe(dest('app/static/css'))
		.on('end', cb);
}

// Minify CSS
function css_minify(cb) {
	src([
		'app/static/css/**/*.css',
		'!app/static/css/**/*.min.css'
	])
		.pipe(cleanCSS())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(dest('app/static/css'))
		.on('end', cb)
		.pipe(browserSync.stream({match: 'app/static/css/**/*.css'}));
}

// Minify JavaScript
function js(cb) {
	src([
		'app/static/js/**/*.js',
		'!app/static/js/**/*.min.js'
	])
		.pipe(uglify())
		.pipe(rename({
			suffix: '.min'
		}))
		.pipe(dest('app/static/js'))
		.on('end', cb)
		.pipe(browserSync.stream());
}

// Configure the browserSync task
function browser_sync() {
	browserSync.init({
		notify: false,
		proxy: '127.0.0.1:5000',
		open: false
	});
}

//Run Flask server
function run_server() {
	return exec('flask run');
}

// Dev task
function dev() {
	watch([
		'app/templates/**/*.html',
		'app/**/*.py',
	], browserSync.reload);
	watch([
		'app/static/sass/**/*.sass',
	], ['css:compile', browserSync.reload]);
	watch([
		'app/static/css/**/*.css',
		'!app/static/css/**/*.min.css',
	], ['css:minify', browserSync.reload]);
	watch([
		'app/static/js/**/*.js',
		'!app/static/js/**/*.min.js'
	], ['js', browserSync.reload]);
}

// Tasks
task('vendor_export', parallel(
	vendor_export_bootstrap,
	vendor_export_datatables,
	vendor_export_datatables,
	vendor_export_amchart,
	vendor_export_amchart_images,
	vendor_export_d3,
	vendor_export_font_awesome,
	vendor_export_jquery,
	vendor_export_jqurey_easing
))
task('vendor', series('vendor_export', parallel(vendor_minify_js, vendor_minify_css)))
task("css", series(css_compile, css_minify))
task('js', js)
task('dev', series(parallel(run_server, browser_sync), dev))
task('default', series('vendor', parallel('css', 'js')))
