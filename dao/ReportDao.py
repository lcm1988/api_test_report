#coding:utf-8
from time import localtime,strftime
from dao.BaseDao import BaseDao
from tools.Conf import Conf

class ReportDao(BaseDao):
    def __init__(self):
        super(ReportDao,self).__init__()
        self.tbname='res'

    def GetNewNo(self,service=''):
        return self.getdata(data='distinct no',where='service=\'%s\''%service,orderby='no desc',limit='1')

    def GetAllService(self):
        return self.getdata(data='distinct service')

    def GetReportIndex(self):
        srvs=[i['service'] for i in self.GetAllService()]
        service,pas,fail,err=[],[],[],[]
        for i in srvs:
            service.append(i)
            no=self.GetNewNo(i)[0]['no']
            pass_num=self.getdata(data='count(*)',where='result=\'%s\' and no =%s and service=\'%s\''%('pass',no,i))[0]['count(*)']
            fail_num=self.getdata(data='count(*)',where='result=\'%s\' and no =%s and service=\'%s\''%('fail',no,i))[0]['count(*)']
            err_num=self.getdata(data='count(*)',where='result=\'%s\' and no =%s and service=\'%s\''%('err',no,i))[0]['count(*)']
            pas.append(pass_num)
            fail.append(fail_num)
            err.append(err_num)
        #print(pass_num,fail_num,err_num)
        report_res={
            'err':err,
            'pass':pas,
            'fail':fail,
            'service':service
        }
        return report_res

    def GetReportDetail(self,kw=''):
        #service_name= Conf().get_conf('config.service')[kw]
        #获取最近50个批次
        res=self.getdata(data='distinct no',where='service=\'%s\''%kw,orderby='no desc',limit=50)

        no=[i['no'] for i in res]
        acc,fail,err=[],[],[]
        #填充各批次数据
        for i in no:
            res=self.getdata(data='result',where='no=%s and service=\'%s\''%(str(i),kw))
            acc.append(int((len([1 for i in res if i['result']=='pass'])/len(res))*100))
            err.append(int((len([1 for i in res if i['result']=='err'])/len(res))*100))
            fail.append(int((len([1 for i in res if i['result']=='fail'])/len(res))*100))
        res={'service': kw, 'no': no, 'pass': acc, 'fail': fail, 'err': err}
        return res

    def GetReportAjax(self,kw='',no=''):
        #service_name= Conf().get_conf('config.service')[kw]
        #获取指定批次、指定服务case运行结果

        data='id,no,platform,service,uri,casename,casepath,result,consoleinfo,errinfo,cost'
        res=self.getdata(data=data,where='no=%s and service=\'%s\''%(no,kw))
        res={'data':res}
        return res



if __name__=="__main__":
    #print(ReportDao().GetReportIndex())
    print(ReportDao().GetReportDetail(kw='NT_API'))
    print(ReportDao().GetReportAjax(kw='NT_API',no='1510827337'))
    print(ReportDao().GetReportIndex())
