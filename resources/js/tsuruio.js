$(function() {
  $(".try .button").on("click", function(e) {
    e.preventDefault();
    $(".dropdown-menu").toggleClass("open");
  });
});
