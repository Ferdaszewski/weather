function drawSparklines() {
  
  var options_wind = {
    type: 'line',
    width: '100%',
    height: '100%',
    lineColor: '#80EB6A',
    fillColor: '#A4F493',

    lineWidth: 5,
    spotRadius: '5',
    spotColor: null,
    minSpotColor: '#48D12B',
    maxSpotColor: '#48D12B',
    highlightSpotColor: '#CEFBC4',

    chartRangeMin: 0,
    chartRangeMax: 20,

    highlightLineColor: null,
    disableHiddenCheck: true
  };

  var options_temp = {
    type: 'line',
    width: '100%',
    height: '100%',
    lineColor: '#FB727F',
    fillColor: false,

    lineWidth: 5,
    spotRadius: '5',
    spotColor: null,
    minSpotColor: '#F23244',
    maxSpotColor: '#F23244',
    highlightSpotColor: '#FEC6CB',

    chartRangeMin: 32,
    chartRangeMax: 70,

    composite: true,
    highlightLineColor: null,
    disableHiddenCheck: true
  };

  var options_cloud = {
    type: 'line',
    width: '100%',
    height: '100%',
    lineColor: '#FFB074',
    fillColor: '#FFC599',

    lineWidth: 5,
    spotRadius: '5',
    spotColor: null,
    minSpotColor: '#FA8A34',
    maxSpotColor: '#FA8A34',
    highlightSpotColor: '#FFDFC7',

    chartRangeMin: 0,
    chartRangeMax: 1,

    highlightLineColor: null,
    disableHiddenCheck: true
  };

  var options_precip = {
    type: 'line',
    width: '100%',
    height: '100%',
    lineColor: '#5ED0C8',
    fillColor: false,

    lineWidth: 5,
    spotRadius: '5',
    spotColor: null,
    minSpotColor: '#209A91',
    maxSpotColor: '#209A91',
    highlightSpotColor: '#C0F6F2',

    composite: true,
    chartRangeMin: 0,
    chartRangeMax: 1,

    highlightLineColor: null,
    disableHiddenCheck: true
  };


  var forecast_temp = $('#wind-temp').data('forecast-temp').split(',');
  var forecast_wind = $('#wind-temp').data('forecast-wind').split(',');
  var forecast_cloud = $('#cloud-precip').data('forecast-cloud').split(',');
  var forecast_precip = $('#cloud-precip').data('forecast-precip').split(',');

  $('#wind-temp').sparkline(forecast_wind, options_wind);
  $('#wind-temp').sparkline(forecast_temp, options_temp);

  $('#cloud-precip').sparkline(forecast_cloud, options_cloud);
  $('#cloud-precip').sparkline(forecast_precip, options_precip);
}

$(document).ready(function() {
  drawSparklines();

  // Redraw sparklines on window resize
  var resizeTimer
  $(window).resize( function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(drawSparklines(), 1000);
    console.log("resizing window")
  });
});
