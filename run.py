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
        'http://ntqa02v.qa.corp.qihoo.net:8080/': 'GIT',
        'http://ntqa02v.qa.corp.qihoo.net:8000/': 'Jenkins',
        '/static/T%E9%A1%B9%E7%9B%AE%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%96%87%E6%A1%A3.zip': 'T项目服务端测试文档'
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

#manager=Manager(app)

if __name__=="__main__":
    #manager.run()
    app.run(debug=True)