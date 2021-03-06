module.exports = (grunt) ->
  grunt.config 'sass',
    options:
      sourcemap: 'none'
      style: 'compressed'
    dist:
      files: [
        expand: true
        cwd: 'resources/styles'
        src: '*.scss'
        dest: 'resources/styles'
        ext: '.css'
      ]
