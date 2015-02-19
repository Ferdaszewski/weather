function app() {
  $('.sparkline').each( function() {
    $(this).sparkline($(this).data('forecast').split(','));
  });
}





$(document).ready(function() {
  app();
});