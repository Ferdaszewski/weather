function drawSparklines() {
  
  var options_night = {
    type: 'line',
    width: '100%',
    height: '100%',
    lineColor: 'rgba(0,0,0,.1)',
    fillColor: 'rgba(0,0,0,.1)',

    numberFormatter: night_day,

    lineWidth: 2,
    spotColor: null,
    minSpotColor: null,
    maxSpotColor: null,
    highlightSpotColor: null,

    chartRangeMin: 0,
    chartRangeMax: 1,

    composite: true,
    disableTooltips: false,
    disableHighlight: false,
    highlightLineColor: null,
    disableHiddenCheck: true
  };

  var options_wind = {
    type: 'line',
    width: '100%',
    height: '100%',
    lineColor: '#80EB6A',
    fillColor: '#A4F493',

    tooltipSuffix: ' mph',

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

    tooltipSuffix: ' °F',

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

    numberFormatter: percent,
    tooltipSuffix: '%',

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

    numberFormatter: percent,
    tooltipSuffix: '%',

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

  var forecast_night = $('#wind-temp').data('night').split(',');

  var forecast_temp = $('#wind-temp').data('forecast-temp').split(',');
  var forecast_wind = $('#wind-temp').data('forecast-wind').split(',');

  var forecast_cloud = $('#cloud-precip').data('forecast-cloud').split(',');
  var forecast_precip = $('#cloud-precip').data('forecast-precip').split(',');

  console.log("Drawing Sparklines...")
  $('#wind-temp').sparkline(forecast_wind, options_wind);
  $('#wind-temp').sparkline(forecast_temp, options_temp);
  $('#wind-temp').sparkline(forecast_night, options_night);

  $('#cloud-precip').sparkline(forecast_cloud, options_cloud);
  $('#cloud-precip').sparkline(forecast_precip, options_precip);
  $('#cloud-precip').sparkline(forecast_night, options_night);

  function percent(num) {
    return num * 100;
  };

  function night_day(num) {
    if (num === 1)
      return "Night";
    else
      return "Day";
  };
}

$(document).ready(function() {
  drawSparklines();

  // Redraw sparklines on window resize
  var resizeTimer
  $(window).resize( function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(drawSparklines, 500);

  });
});
