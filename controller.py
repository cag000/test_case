import pymysql
import re

from datetime import datetime
from datetime import timedelta
from ConfigParser import ConfigParser

class Controller:
    def __init__(self, config_file="config.ini"):
        self.config = ConfigParser()    
        self.config.read(config_file)
        
    def db_con(self, **kwargs):
        con = None
        try:
            con = pymysql.connect(
                host=kwargs["db_host"],
                user=kwargs["db_user"],
                password=kwargs["db_pwd"],
                db="new_clipper",
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            print e
        finally:
            return con
    
    def read_txt(self, namefile):
        testsite_array = None
        with open(namefile) as my_file:
            testsite_array = my_file.read().splitlines()
        return testsite_array
        
    def get_days(self):
        now = datetime.now().strftime("%Y-%m-%d")
        now_h = [
                (datetime.strptime(now, "%Y-%m-%d") - timedelta(days=0)).strftime("%Y-%m-%d")
        ]
        return now_h
    
    def match_regex(self, **kwargs):
        for i in kwargs["list_of_regex"]:
            print i
            print re.escape(i)
            break
            try:
                pattern = re.match("{}".format(i), kwargs["content"])
                if pattern:
                        return True
                else:
                    continue
            except Exception as e:
                raise e
        return False