#!/usr/bin/python3.5
#coding:utf-8

class Conf():
    def __init__(self,env='qa'):
        self.fmd='conf.%s'%env.lower() if env.lower() in ('qa','prod') else 'conf.qa'

    def get_conf(self,keypath=''):
        [file,key]=keypath.split('.')
        md=__import__(self.fmd,fromlist=(file,))
        args=getattr(md,file)
        return getattr(args,key)

if __name__=="__main__":
    conf=Conf('qa').get_conf('config.db_qadev')
    print(conf)