module.exports = (grunt) ->
  grunt.config 'robotstxt',
    dist:
      dest: './'
      policy: [{
        ua: 'googlebot'
        disallow: '/resources/'
      }, {
        ua: 'googlebot-news'
        allow: 'https://blog.tsuru.io/'
      }, {
        ua: 'googlebot-third'
        allow: ['https://docs.tsuru.io/']
      }, {
        sitemap: [
          'https://tsuru.io/sitemap.xml'
          'https://docs.tsuru.io/sitemap.xml'
        ]
      }, {
        crawldelay: 100
      }, {
        host: 'tsuru.io'
      }]
