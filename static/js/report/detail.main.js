//datatable初始参数
var initAjaxsource= "/report/ajax?kw=奶糖API"+"&batchno="+Math.max.apply(null,res.no);//默认调用最新批次执行结果
var initParams={
        "sAjaxSource": initAjaxsource,
        //该配置确保datatable是可以刷新的，不能少
        retrieve: true,
        "columns": [
            { "data": "datebuffer" },
            { "data": "interfacename" },
            { "data": "testcasename" },
            { "data": "plateform" },
            { "data": "testresult" },
            { "data": "failreason" },
            { "data": "response" }
        ]
    };
var wageNowTable;
var no= res.no;//批次时间戳
var pass= res.pass;//成功率
var service= res.service;
var data=[];

for (var i=0 ;i <= no.length; i++){
    t= new Date(no[i]*1000);
    tmp={
        name: t.toString(),
        value:[
            [t.getFullYear(), t.getMonth(), t.getDate()].join('/')+' '+[t.getHours(), t.getMinutes(), t.getSeconds()].join(':'),
            pass[i],
            no[i]
        ]
    };
    data.push(tmp);
}
//配置报表
var myChart = echarts.init(document.getElementById('echarts_sheet'));
var option = {
    title: {
        right: '0%',
        bottom: '0%',
        text: '各批次成功率',
        subtext: '数据来源：QADEV'
    },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return '执行时刻：'+[date.getHours(), date.getMinutes()].join(':') +'\n成功率：'+params.value[1]+'\n批次：'+params.value[2];
        }
    },
    toolbox: {
        show : true,
        feature : {
            magicType : {show: true, type: ['line', 'bar']},
        saveAsImage : {show: true}
        }
    },
    grid: {
        top: '10%',
        left: '5%',
        right: '10%',
        bottom: '15%'
    },
    xAxis: [{
        nameRotate: 30,
        type: 'time'
    }],
    yAxis: [{
        name: '成功率',
        type: 'value'
    }],
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
    $('#datatable_sheet').DataTable(initParams);
});