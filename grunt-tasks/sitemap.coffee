module.exports = (grunt) ->
  grunt.config 'sitemap',
    dist:
      siteRoot: './'
      pattern: [
        '*.html'
        '!**/google*.html' # this will exclude 'google*.html'
      ]
