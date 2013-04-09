// Copyright 2013 Globo.com authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

(function(global, document) {
	if(global._ === undefined) {
		global._ = {};
	}

	global._.setActive = function() {
		var i, path = global.location.href.replace(/\/$/, '').replace(/^http:\/\/.*\//, '');
		var re = new RegExp(path + '$');
		var itens = document.querySelectorAll('.nav > li > a');
		for(i = 0; i < itens.length; i++) {
			if(re.test(itens[i].href)) {
				itens[i].classList.add('active');
				break;
			}
		}
	};

	document.getElementsByTagName("body")[0].onload = global._.setActive();
})(window, window.document);
