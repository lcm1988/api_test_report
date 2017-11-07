#coding:utf-8
from json import dumps
from flask import Flask
from flask import request
from flask import render_template
from flask_script import Manager
from dao.ReportDao import ReportDao
from tools.GetLink import GetLink

app=Flask(__name__)

@app.route('/')
def index():
    '''首页导航'''
    res={
        '/report/index': '自动化测试总览',
        '/report/detail?kw=奶糖API': '奶糖API测试明细',
        'http://ntqa02v.qa.corp.qihoo.net:8080/': 'GIT'
    }
    return GetLink(res)

@app.route('/report/index')
def report_index():
    '''报告首页，展示各服务最新批次结果'''
    res=ReportDao().GetReportIndex()
    return render_template('report/index.html',res=res)

@app.route('/report/detail')
def report_detail():
    '''服务明细，表格展示最新批次结果'''
    kw=request.args.get('kw','')
    res=ReportDao().GetReportDetail(kw)
    return render_template('report/detail.html', res=res)

@app.route('/report/ajax')
def report_ajax():
    '''请求指定服务、指定批次结果用以ajax请求返回'''
    kw=request.args.get('kw','')
    batchno=request.args.get('batchno','')
    if not kw or not batchno:
        return '查询缺少必要的参数'
    res=ReportDao().GetReportAjax(kw,batchno)
    return dumps(res,ensure_ascii=False)

manager=Manager(app)

if __name__=="__main__":
    manager.run()
    #app.run(debug=True)