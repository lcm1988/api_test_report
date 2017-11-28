// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

// 指定图表的配置项和数据
var option = {
    //标题属性
    title: {
        right: 10,
        bottom: 5,
        text: '各服务最新批次展示',
        subtext: '数据来源：NTQA'
    },
    //维度属性
    legend: {
        type: 'plain',
        orient: 'vertical',
        right: 20,
        top: '40%',
        backgroundColor: '#ccc' ,
        data:['error', 'pass', 'fail']
    },
    //数据表属性
    grid:{
        bottom: '15%',
        top: '10%',
        left: '5%',
        right: '10%'
    },
    tooltip : {
        top: 60,
        trigger: 'axis',
        axisPointer :{            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    xAxis: {
            name: '服务名称',
            type : 'category',
            data:  res.service
        },
    yAxis: {
        name: '用例数/个',
        type: 'value'
    },
    series: [{
            name: 'error',
            type: 'bar',
            itemStyle : { normal: {label : {show: true, position: 'top'}}},
            data: res.err
        },{
            name: 'pass',
            type: 'bar',
            itemStyle : { normal: {label : {show: true, position: 'top'}}},
            data: res.pass
        },{
            name: 'fail',
            type: 'bar',
            itemStyle : { normal: {label : {show: true, position: 'top'}}},
            data: res.fail
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
myChart.on('click', function (params) {
    window.open('/report/detail?kw=' + encodeURIComponent(params.name));
});