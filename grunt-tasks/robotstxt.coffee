module.exports = (grunt) ->
  grunt.config 'robotstxt',
    dist:
      dest: './'
      policy: [{
        ua: 'googlebot'
        disallow: '/resources/'
      }, {
        ua: 'googlebot-news'
        allow: 'http://blog.tsuru.io/'
      }, {
        ua: 'googlebot-third'
        allow: ['http://docs.tsuru.io/']
      }, {
        sitemap: [
          'http://tsuru.io/sitemap.xml'
          'http://docs.tsuru.io/sitemap.xml'
        ]
      }, {
        crawldelay: 100
      }, {
        host: 'tsuru.io'
      }]
