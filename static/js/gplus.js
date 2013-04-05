(function() {
	var po = document.createElement('script');
	po.type = 'text/javascript';
	po.async = true;
	po.src = 'https://apis.google.com/js/client:plusone.js?onload=renderGplus';
	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(po, s);
})();


function renderGplus() {
	gapi.signin.render('signinButton', {
		'callback': 'gplusCallback',
		'clientid': '489556242997.apps.googleusercontent.com',
		'cookiepolicy': 'single_host_origin',
		'requestvisibleactions': 'http://schemas.google.com/AddActivity',
		'scope': 'https://www.googleapis.com/auth/plus.login'
	});
}

function gplusCallback(r) {
}
