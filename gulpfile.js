const cssnano = require('gulp-cssnano');
const del = require('del');
const gulp = require('gulp');
const htmlmin = require('gulp-htmlmin');
const imagemin = require('gulp-imagemin');
const uglify = require('gulp-uglify-es').default;
const webpack = require('webpack-stream');

///////////////////////
// Development Tasks //
///////////////////////

// Bundle CSS and JS(X) for development
gulp.task('dev-webpack', function () {
  return gulp.src('src/js/**/*.+(js|jsx)')
    .pipe(webpack(require('./webpack/webpack.dev.js')))
    .pipe(gulp.dest('src/static/'));
});

// Clean dist
gulp.task('dev-clean', function () {
  return del('src/static');
});

// Copy media
gulp.task('dev-copy-media', function () {
  return gulp.src('src/media/**/*', {base: './src/'})
    .pipe(gulp.dest('src/static'));
});

// Watch static and template file changes
gulp.task('watch', function () {
  gulp.watch(['src/js/**/*', 'src/sass/**/*'], gulp.series(['dev-webpack']));
})

// Build dev
gulp.task('dev-build', gulp.series(
  'dev-clean',
  'dev-webpack',
  'dev-copy-media'
));

//////////////////////
// Production Tasks //
//////////////////////

// Bundle CSS and JS(X) for production
gulp.task('prod-webpack', function () {
  return gulp.src('src/js/**/*.+(js|jsx)')
    .pipe(webpack(require('./webpack/webpack.prod.js')))
    .pipe(gulp.dest('dist/'));
});

// Optimize JavaScript
gulp.task('optimize-js', function () {
  return gulp.src('dist/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('dist'));
});

// Optimize JavaScript
gulp.task('optimize-css', function () {
  return gulp.src('dist/*.css')
    .pipe(cssnano())
    .pipe(gulp.dest('dist'));
});

// Optimize HTML
gulp.task('optimize-html', () => {
  return gulp.src('src/templates/*.html')
    .pipe(htmlmin({ collapseWhitespace: true }))
    .pipe(gulp.dest('dist'));
});

// Copy media
gulp.task('prod-copy-media', function () {
  return gulp.src('src/media/**/*', {base: './src/'})
    .pipe(gulp.dest('dist'));
});

// Optimize Images
gulp.task('optimize-images', function () {
  return gulp.src('dist/imgs/**/*.+(png|jpg|jpeg|gif|svg)')
    .pipe(imagemin({
      interlaced: true,
    }))
    .pipe(gulp.dest('dist/imgs'));
});

// Clean dist
gulp.task('prod-clean', function () {
  return del('dist');
});

// Build and optimize prod
gulp.task('prod-build', gulp.series(
  'prod-clean',
  'prod-webpack',
  gulp.parallel('optimize-js', 'optimize-css', 'optimize-html',
    'prod-copy-media'),
  'optimize-images'
));
