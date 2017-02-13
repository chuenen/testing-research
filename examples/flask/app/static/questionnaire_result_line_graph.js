var series = []
var result = Object.keys(data.satisfaction);
var len = result.length
for(var i = 0; i < len; i++){
var r = result[i]
    series.push({name: r,
                 data: data.satisfaction[r]
    })
}

var container = $('#rating-visualization')
var chart = new Highcharts.Chart({
    colors: ['#0E9D58', '#BFD047', '#FFC105', '#EF7E14', '#D36259'],
    chart: {
        renderTo: $(container)[0],
        type: 'column',
        marginTop: 40,
        height: 320,
        zoomType: 'x',
        backgroundColor: '#FFF'
    },
    title: {
            text: 'Result of questionnaire'
    },
    xAxis: {
        categories: data.question 
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Count of Answer'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
        shared: true
    },
    plotOptions: {
        column: {
            stacking: 'normal',
            cursor: 'pointer',
            animation: {
                redraw: true,
                duration: 2000,
                easing: 'easeOutBounce'
            }
        }
    },
    series: series
});
