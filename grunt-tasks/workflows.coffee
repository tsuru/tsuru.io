module.exports = (grunt) ->
  grunt.registerTask 'map', ['sitemap', 'robotstxt']
  grunt.registerTask 'css', ['sass', 'postcss']
  grunt.registerTask 'run', 'concurrent'
  grunt.registerTask 'default', 'run'
