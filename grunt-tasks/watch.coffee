module.exports = (grunt) ->
  grunt.config 'watch',
    css:
      files: 'resources/styles/**/*.scss'
      tasks: [
        'sass'
        'postcss'
      ]
    html:
      files: '**/*.html'
      tasks: 'sitemap'
