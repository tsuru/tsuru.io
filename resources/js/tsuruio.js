(function(){
  var cancelEvent = function(event){
    event.preventDefault ? event.preventDefault() : event.returnValue = false;
  };

  var navigation = document.getElementById('navigation');
  var navButton = document.getElementById('navigation-button');

  navButton.addEventListener('click', function(e){
    cancelEvent(e);
    navButton.classList.toggle('navigation--is-open');
    navigation.classList.toggle('navigation--is-open');
  });

  var tryButton = document.getElementById('try-button');
  var dropdown = document.getElementById('dropdown-menu');
  if (tryButton && dropdown) {
    tryButton.addEventListener('click', function(e){
      cancelEvent(e);
      dropdown.classList.toggle('open');
    });
  }
})();
