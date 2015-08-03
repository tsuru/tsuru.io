module.exports = (grunt) ->
  grunt.config 'watch',
    css:
      files: 'resources/styles/**/*.scss'
      tasks: 'css'
    html:
      files: '**/*.html'
      tasks: 'map'
