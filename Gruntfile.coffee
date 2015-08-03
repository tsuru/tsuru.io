module.exports = (grunt) ->
  require('load-grunt-tasks') grunt

  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

  grunt.loadTasks 'grunt-tasks'


# 	grunt.initConfig({
# 		pkg: grunt.file.readJSON('package.json'),

# 		watch: {
# 			css: {
# 				files: '**/*.scss',
# 				tasks: ['sass', 'postcss']
# 			},
# 			html: {
# 				files: ['*.html', 'easy/*.html', '!**/google*.html'],
# 				tasks: ['sitemap']
# 			}
# 		},
# 	});

# 	grunt.registerTask('map',['sitemap', 'robotstxt']);
# 	grunt.registerTask('default',['watch']);
# };
