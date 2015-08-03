module.exports = (grunt) ->
  require('load-grunt-tasks') grunt

  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'

  grunt.loadTasks 'grunt-tasks'


# 	grunt.initConfig({
# 		pkg: grunt.file.readJSON('package.json'),

#         postcss: {
#             options: {
#                 processors: [
#                     require('autoprefixer-core')({browsers: 'last 2 versions'}), add vendor prefixes
#                 ]
#             },
#             dist: {
#                 src: 'resources/styles/**/*.css'
#             }
#         },

# 		sitemap: {
# 			dist: {
# 				pattern: ['*.html', 'easy/*.html', '!**/google*.html'], this will exclude 'google*.html'
# 				siteRoot: './'
# 			}
# 		},
# 		robotstxt: {
#             dist: {
#                 dest: './',
#                 policy: [
#                     {
#                         ua: 'googlebot',
#                         disallow: '/resources/'
#                     },
#                     {
#                         ua: 'googlebot-news',
#                         allow: 'http://blog.tsuru.io/'
#                     },
#                     {
#                         ua: 'googlebot-third',
#                         allow: ['http://docs.tsuru.io/']
#                     },
#                     {
#                         sitemap: ['http://tsuru.io/sitemap.xml', 'http://docs.tsuru.io/sitemap.xml']
#                     },
#                     {
#                         crawldelay: 100
#                     },
#                     {
#                         host: 'tsuru.io'
#                     }
#                 ]
#             }
#         },
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
