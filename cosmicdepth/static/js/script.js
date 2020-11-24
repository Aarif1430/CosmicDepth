$(document).ready(function(){
  setTimeout(function(){$('.messages.success').fadeOut();}, 8000);
  $(window).click(function(){$('.messages.success').fadeOut();});
});