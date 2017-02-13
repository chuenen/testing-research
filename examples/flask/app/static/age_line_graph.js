var w_age = Object.keys(data.w_age).map(function(key){
    return data.w_age[key];
});
var m_age = Object.keys(data.m_age).map(function(key){
    return data.m_age[key];
});

var container = $('#age-visualization')
var chart = new Highcharts.Chart({
    colors: ['#F50057', '#2979FF'],
    chart: {
        renderTo: $(container)[0],
        type: 'column',
        marginTop: 40,
        height: 320,
        zoomType: 'x',
        backgroundColor: '#FFF'
    },
    title: {
            text: 'Age of User'
    },
    xAxis: {
        categories: ['14 -', '15-24','25-34', '35-44', '45-54', '55-64', '65 +']
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Count of Age'
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
    series: [{
        name: 'Female',
        data: w_age
    }, {
        name: 'Male',
        data: m_age
    }]
});
