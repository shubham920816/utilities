import logging
import os
import datetime
import sys



class loggerfunc(object):
    """This class initialises a looger object."""

    def __init__(self,level="INFO",run_date="",logfilename="ingestion",absolutepath="/mnt/applog"):
        """Log level  and folder path for log file is initiazed and created."""
        self.level=level
        self.servicename=logfilename
        if len(run_date)==0:
            self.run_date=datetime.datetime.today().isoformat()
        self.run_date=run_date
        self.absolutepath=absolutepath
        self.loglevel=self.setlogginglevel()

    def setlogginglevel(self):
        """String Logging defination is converted to Logging Object defination.

        Returns:
        Obj:logginglevel
        """
        logginglevel = str.upper(self.level)
        LEVELS = {'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        return(LEVELS[logginglevel])

    def logger(self):
        """Create logging file format and defines log handler file name.

        Returns:
        LoggerObj:logger_test
        """
        self.setlogginglevel()
        logger_test = logging.getLogger(os.path.basename(sys.argv[0].split(".")[0]))
        logger_test.setLevel(self.loglevel)
        foldername="%s/logs/%s/"%(self.absolutepath,self.run_date)
        os.system("mkdir -p %s"%foldername)
        ch = logging.FileHandler("%s/%s.log"%(foldername,self.servicename), mode='a')
        ch.setLevel(self.loglevel)
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s -%(filename)s - %(funcName)s - %(message)s')
        ch.setFormatter(formatter)
        logger_test.addHandler(ch)
        return (logger_test)

if __name__ == "__main__":
    pass

