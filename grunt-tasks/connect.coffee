module.exports = (grunt) ->
  grunt.config 'connect',
    server:
      options:
        port: 7777
        keepalive: true
