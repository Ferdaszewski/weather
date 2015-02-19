function app() {
  $('.sparkline').each( function(index) {
    var forecast = $(this).data('forecast').split(',');
    var options = {
      type: 'line',
      width: '900px',
      height: '400px',
      fillColor: false,
      disableHiddenCheck: true,
      spotColor: false,
      spotRadius: '3',
      higlightLineColor: null,
      lineWidth: 3
    };
    $(this).sparkline(forecast, options);
  });
}

$(document).ready(function() {
  app();
});
