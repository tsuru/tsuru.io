module.exports = (grunt) ->
  require('load-grunt-tasks') grunt

  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

  grunt.loadTasks 'grunt-tasks'
