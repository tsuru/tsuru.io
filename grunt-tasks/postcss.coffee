module.exports = (grunt) ->
  grunt.config 'postcss',
    options:
      processors: [
        require('autoprefixer-core') browsers: 'ie >= 10, last 2 versions'
      ]
    dist:
      src: 'resources/styles/**/*.css'
