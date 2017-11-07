#coding:utf-8
import pymysql
from tools.Conf import Conf
'''

'''
class BaseDao():
    def __init__(self):
        self.conf=Conf().get_conf('config.db')
        self.tbname='test'
        '''
        self.db= pymysql.connect(
            host=conf['host'],
            user=conf['user'],
            password=conf['pwd'],
            database=conf['db'])
        '''

    def getdata(self,data='',where='',orderby='',limit=''):
        dt= data if data else '*'

        whr= 'where %s'%where if  where else 'where 1=1'

        order='order by %s'%orderby if orderby else ''

        lmt='limit %s'%str(limit) if limit else ''

        sql="select %s from %s %s %s %s"%(dt,self.tbname,whr,order,lmt)
        data=self.excute(sql)
        return data

    def excute(self,sql='',type='select'):
        if type=='select' and sql.strip()[:6].lower()!='select':
            raise()
        db= pymysql.connect(
            host=self.conf['host'],
            user=self.conf['user'],
            password=self.conf['pwd'],
            database=self.conf['db'])
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        #print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        return data

if __name__=="__main__":
    data_fields={'data':'name,age','limit':'1'}
    data=BaseDao().getdata(data='name,age',where='age=2 and name=2',orderby='age desc,name asc',limit=1)
    print(data)