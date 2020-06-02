import logging
import datetime
import os
import sys


class loggerfunc(object):
    """
    This class intiates logger and return logger object
    """

    def __init__(self,level="INFO",run_date="",servicename="",absolutepath="/mnt/consumerhub"):
        """
        Initiates logger class
        :param level: Logging Level
        :param run_date: Date folder for logging
        :param servicename: Log file name
        :param absolutepath: Absolute path for dumping the Logs
        """

        self.level = level
        if run_date:
          self.run_date=run_date
        else:
            self.run_date=datetime.date.today().isoformat()
        self.absolutepath=absolutepath
        self.servicename=servicename
        self.loglevel=self.setlogginglevel()




    def setlogginglevel(self):
        """
        Sets Logging Level
        :return:
        """

        logginglevel = str.upper(self.level)
        LEVELS = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        return(LEVELS[logginglevel])



    def logger(self):
        """
        Returns logger object
        :return:
        """
        self.setlogginglevel()

        logger_obj = logging.getLogger(os.path.basename(sys.argv[0].split(".")[0]))
        logger_obj.setLevel(self.loglevel)

        foldername="%s/logs/%s/%s/"%(self.absolutepath,self.servicename,self.run_date)
        os.system("mkdir -p %s"%foldername)
        ch.setLevel(self.loglevel)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
        ch = logging.Filendler("%s/%s.log"%(foldername,self.servicename), mode='a')
        ch.setFormatter(formatter)
        logger_obj.addHandler(ch)
        return (logger_obj)

if __name__ == "__main__":
    t1 = loggerfunc()
    t2 = t1.logger()
    print(t2)

