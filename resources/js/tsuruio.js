$(function() {
	function goTo($element) {
		console.log($element);
		var headerHeight = 112;
		$('html, body').animate({scrollTop: $element.offset().top - 112}, 1000);
	}

	$.each($(".navigation .scroll-btn"), function(index, element) {
		$(this).on('click', function(event) {
			event.preventDefault();
			goTo($($(this).attr("href")));
		});
	});

});
