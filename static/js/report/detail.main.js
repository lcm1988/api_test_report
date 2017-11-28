//datatable初始参数

var wageNowTable;
var no= res.no;//批次时间戳
var pass= res.pass;//成功率
var service= res.service;
var data=[];

var initAjaxsource= "/report/ajax?kw="+service+"&batchno="+Math.max.apply(null,no);//默认调用最新批次执行结果
var initParams={
        "sAjaxSource": initAjaxsource,
        //该配置确保datatable是可以刷新的，不能少
        retrieve: true,
        "columns": [
            { "data": "no"},
            { "data": "platform" },
            { "data": "service" },
            { "data": "uri" },
            { "data": "casename" },
            { "data": "casepath" },
            { "data": "result" },
            { "data": "cost" },
            { "data": "consoleinfo", "visible": false },
            { "data": "errinfo", "visible": false },
            { "data": null , "defaultContent": "<button>查看</button>"}
        ],
        "order":[[6,"asc"]]
    };

for (var i=0 ;i < no.length; i++){
    runtime= new Date(no[i]*1000);
    tmp={
        name: runtime.toString(),
        value:[
            [runtime.getFullYear(), runtime.getMonth()+1, runtime.getDate()].join('/')+' '+[runtime.getHours(), runtime.getMinutes()].join(':'),
            pass[i],
            no[i]
        ]
    };
    data.push(tmp);
}
//配置报表
var myChart = echarts.init(document.getElementById('echarts_sheet'));
var option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            param = params[0];
            console.log(JSON.stringify(param));
            return '执行时间：'+param.data.value[0]+'<br>成功率：'+param.data.value[1]+'<br>批次：'+param.data.value[2];
        }
    },
    toolbox: {
        show : true,
        feature : {
            magicType : {show: true, type: ['line', 'bar']},
            saveAsImage : {show: true}
        },
        right:'2%'
    },
    grid: {
        top: '10%',
        left: '5%',
        right: '10%',
        bottom: '15%'
    },
    xAxis: [{
        name: '执行时间',
        type: 'time',
        minInterval: 0,
        nameRotate: 0,
        max: function(){
            return Date.parse(new Date())+3600*1000
        }
    }],
    yAxis: [{
        name: '成功率',
        type: 'value',
        max:100
    }],
    dataZoom: [
        {
        	id: 'dataZoomX1',
        	type: 'inside',
        	xAxisIndex: [0],
        	filterMode: 'filter'
        },
        {
        	id: 'dataZoomX2',
        	type: 'slider',
        	xAxisIndex: [0],
        	filterMode: 'filter'
        }
    ],
    series: [{
        name: '模拟数据',
        type: 'line',
        symbolSize:10,
        data: data
    }]
};

myChart.setOption(option);
myChart.on('click', function (params) {
    //window.open('https://www.baidu.com/s?wd=' + encodeURIComponent(params.name));//点击不同shadow跳转不同页面
    wageNowTable = $('#datatable_sheet').dataTable(initParams);
    wageNowTable.fnDestroy();//这行必须有，不然没办法刷新列表
    url = "/report/ajax?kw="+service+'&'+'batchno='+params.value[2];//根据点击位置生成ajax请求url
    //alert(url);
    initParams.sAjaxSource=url;
    wageNowTable = $('#datatable_sheet').dataTable(initParams);//刷新数据列表

});

//配置数据列表
$(document).ready(function() {
    var table = $('#datatable_sheet').DataTable(initParams);
    $('#datatable_sheet tbody').on( 'click', 'button', function () {
        var data = table.row( $(this).parents('tr') ).data();
        alert( data["consoleinfo"] +"\n\n"+ data["errinfo"] );
    } );
});