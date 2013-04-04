function login() {
    FB.login(function(response) {
        if (response.authResponse) {
            // connected
            // redirect
        } else {
            // cancelled
            // failure page
        }
    });
}

function testAPI() {
    console.log('Welcome! Fetching your information.... ');
    FB.api('/me', function(response) {
        console.log('Good to see you, ' + response.name + '.');
    });
}

window.fbAsyncInit = function() {
    FB.init({
        appId      : '441115332643061', // App ID
        channelUrl : 'http://localhost:5000/channel.html', // Channel File
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        xfbml      : true  // parse XFBML
    });
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            // connected
            // no login buttons
            testAPI();
        } else if (response.status === 'not_authorized') {
            // not_authorized
            // show login buttons
            // login()
        } else {
            // not_logged_in
            // show login buttons
            // login()
        }
    });
};

// Load the SDK Asynchronously
(function(d){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement('script'); js.id = id; js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));
