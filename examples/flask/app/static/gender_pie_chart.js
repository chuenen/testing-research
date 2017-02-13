var container = $('#data-visualization')
var chart = new Highcharts.Chart({
    colors: ['#D50000', '#3D5AFE'],
    chart: {
        renderTo: $(container)[0],
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Gender Ratio'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    series: [{
        name: 'Gender',
        colorByPoint: true,
        data: [{
            name: 'Female',
            y: data['female']
        }, {
            name: 'Male',
            y: data['male']
        }]
    }]
});
