var gulp = require('gulp');
var webserver = require('gulp-webserver');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
 gulp.task('serve', function() {
  gulp.src('./')
    .pipe(webserver({
      livereload: true,
      port: 8002	
    }));
gulp.task('browser-sync', function() {
	browserSync.init(null, {
		notify: false,
		server: {
			baseDir: './'
		},
		port: 8889
	});
});
 gulp.task('bs-reload', function () {
    browserSync.reload();
});
 gulp.task('default', ['browser-sync'], function () {
    gulp.watch("*.html", ['bs-reload']);
    gulp.watch("*.js", ['bs-reload']);
});