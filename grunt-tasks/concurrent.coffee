module.exports = (grunt) ->
  grunt.config 'concurrent',
    options:
      logConcurrentOutput: true
    dev: ['watch', 'connect']
