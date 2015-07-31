(function($){
  $('#navigation-button').click(function(e){
    e.preventDefault();
    $(this).toggleClass('navigation--is-open');
    $('#navigation').toggleClass('navigation--is-open');
  });

  $('.try .button').on('click', function(e){
    e.preventDefault();
    $('.dropdown-menu').toggleClass('open');
  });
})(jQuery);
