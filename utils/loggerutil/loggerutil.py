import logging
import datetime
import os
import time
import sys
from commonutils.storage.azure.files import FileLayer
import multiprocessing

class loggerfunc(object):

    def __init__(self,level="INFO",req_id="",run_id="",run_date="",servicename="",servicelog=False,absolutepath="/mnt/consumerhub"):

        self.level = level
        self.run_id=run_id
        self.req_id=req_id
        self.run_date=run_date
        self.absolutepath=absolutepath
        self.servicelog=servicelog
        self.servicename=servicename
        self.loglevel=self.setlogginglevel()




    def setlogginglevel(self):
        logginglevel = str.upper(self.level)
        LEVELS = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        return(LEVELS[logginglevel])



    def logger(self):
        self.setlogginglevel()

        logger_test = logging.getLogger(os.path.basename(sys.argv[0].split(".")[0]))
        logger_test.setLevel(self.loglevel)

        foldername="%s/logs/%s/%s/%s/%s/"%(self.absolutepath,self.servicename,self.req_id,self.run_id,self.run_date)
        os.system("mkdir -p %s"%foldername)

        if self.servicelog:
          ch=logging.TimedRotatingFileHandler(path=foldername,
                                 when="D",
                                 interval=4,
                                 backupCount=5)

        else:
          ch = logging.FileHandler("%s/%s.log"%(foldername,self.servicename), mode='a')

        ch.setLevel(self.loglevel)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
        # formatter = logging.Formatter(
        #     '%(asctime)s  - %(levelname)s -%(filename)s:%(lineno)d - %(funcName)s - %(message)s')
        ch.setFormatter(formatter)
        logger_test.addHandler(ch)
        return (logger_test)

    def logextract(self,t1,rootdir):

        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                filename=os.path.join(subdir, file)
                if (("log" in file) and ("success"  not  in file) and (len(file.split("log")[1]) > 0)):
                    try:
                     t1.upload_to_blob(filename,container="consumerhubdev")
                     os.rename(filename,filename+".success")
                    except Exception as e:
                        pass

    def log_poll(self):
        pushflag=servicelog
        t1 = FileLayer()
        rootdir = self.absolutepath + "/logs/"
        while pushflag:
            self.logextract(t1,rootdir)


    def logpush(self):
        print("inside log push module")
        process= multiprocessing.Process(target=self.log_poll,
                                             args=(self.servicelog,))
        process.start()
        #while True:
        #   time.sleep(1)
        #   if not multiprocessing.active_children():
        #       break
        #for i in range(20):
        #    print("value",i)



if __name__ == "__main__":
    t1 = loggerfunc()
    t2 = t1.logger()
    print(t2)

