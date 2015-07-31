module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		sass: {
      options: {
        sourcemap: 'none'
      },
			dist: {
				files: [{
					expand: true,
					cwd: 'resources/styles',
				  src: '*.scss',
					dest: 'resources/styles',
					ext: '.css'
				}]
			}
		},
		sitemap: {
			dist: {
				pattern: ['*.html', 'easy/*.html', '!**/google*.html'], // this will exclude 'google*.html'
				siteRoot: './'
			}
		},
		robotstxt: {
            dist: {
                dest: './',
                policy: [
                    {
                        ua: 'googlebot',
                        disallow: '/resources/'
                    },
                    {
                        ua: 'googlebot-news',
                        allow: 'http://blog.tsuru.io/'
                    },
                    {
                        ua: 'googlebot-third',
                        allow: ['http://docs.tsuru.io/']
                    },
                    {
                        sitemap: ['http://tsuru.io/sitemap.xml', 'http://docs.tsuru.io/sitemap.xml']
                    },
                    {
                        crawldelay: 100
                    },
                    {
                        host: 'tsuru.io'
                    }
                ]
            }
        },
		watch: {
			css: {
				files: '**/*.scss',
				tasks: ['sass']
			},
			html: {
				files: ['*.html', 'easy/*.html', '!**/google*.html'],
				tasks: ['sitemap']
			}
		},
	});
	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-sitemap');
	grunt.loadNpmTasks('grunt-robots-txt');

	grunt.registerTask('map',['sitemap', 'robotstxt']);
	grunt.registerTask('default',['watch']);
};
