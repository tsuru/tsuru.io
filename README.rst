Tsuru beta registration
=======================

.. image:: https://secure.travis-ci.org/globocom/tsuru-beta-registration.png
   :target: http://travis-ci.org/globocom/tsuru-beta-registration

Coming soon...

Environment variables
---------------------

The following environment variables define how this app behaves:

* SIGN_KEY: the key that will be used to sign user requests, to prevent some
  sort of request manipulation.
* SECRET_KEY: the secret key used for sessions. This project uses sessions only
  to store CSRF tokens.
* FACEBOOK_APP_ID: the id of the `app in Facebook
  <https://developers.facebook.com/apps>`_. Used for Facebook login.
* GITHUB_CLIENT_ID: the client id of the `GitHub app
  <https://github.com/settings/applications>`_. Used for GitHub login.
* GITHUB_CLIENT_SECRET: the client secret of the `GitHub app
  <https://github.com/settings/applications>`_. Used for GitHub login.
* GOOGLE_API_KEY: the API key used to access Google APIs.
* GOOGLE_USER_IP: one of the authorized user IPs in your project at Google.
