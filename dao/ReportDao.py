#coding:utf-8
from time import localtime,strftime
from dao.BaseDao import BaseDao
from tools.Conf import Conf

class ReportDao(BaseDao):
    def __init__(self):
        super(ReportDao,self).__init__()
        self.tbname='testresult'

    def GetNewNo(self):
        return self.getdata(data='distinct datebuffer',orderby='datebuffer desc',limit='1')

    def GetReportIndex(self,no=''):
        no=self.GetNewNo()[0]['datebuffer']
        pass_res=self.getdata(data='count(*)',where='testresult="%s" and datebuffer =%s'%('pass',no))
        fail_res=self.getdata(data='count(*)',where='testresult="%s" and datebuffer =%s'%('fail',no))
        err_res=self.getdata(data='count(*)',where='testresult="%s" and datebuffer =%s'%('err',no))
        pass_num=pass_res[0]['count(*)']
        fail_num=fail_res[0]['count(*)']
        err_num=err_res[0]['count(*)']
        #print(pass_num,fail_num,err_num)
        report_res={
            'no':no,
            'err':[err_num],
            'pass':[pass_num],
            'fail':[fail_num],
            'service':['奶糖API']
        }
        return report_res

    def GetReportDetail(self,kw=''):
        service_name= Conf().get_conf('config.service')[kw]
        #获取最近50个批次
        res=self.getdata(data='distinct datebuffer',orderby='datebuffer desc',limit=50)

        no=[i['datebuffer'] for i in res]
        acc,fail,err=[],[],[]
        #填充各批次数据
        for i in no:
            res=self.getdata(data='testresult',where='datebuffer=%s'%str(i))
            acc.append(int((len([1 for i in res if i['testresult']=='pass'])/len(res))*100))
            err.append(int((len([1 for i in res if i['testresult']=='err'])/len(res))*100))
            fail.append(int((len([1 for i in res if i['testresult']=='fail'])/len(res))*100))
        res={'service': '奶糖API', 'no': no, 'pass': acc, 'fail': fail, 'err': err}
        return res

    def GetReportAjax(self,kw='',no=''):
        service_name= Conf().get_conf('config.service')[kw]
        #获取指定批次、指定服务case运行结果
        data='id,datebuffer,plateform,interfacename,testcasename,testresult,failreason,response'
        res=self.getdata(data=data,where='datebuffer=%s'%no)
        res={'data':res}
        return res



if __name__=="__main__":
    #print(ReportDao().GetReportIndex())
    print(ReportDao().GetReportAjax(kw='奶糖API',no='1591119191'))
