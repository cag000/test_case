import pymysql
import re
import json
import sys
import logging

from io import StringIO
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
            logging.error(e)
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
        st = []
        for i in kwargs["list_of_regex"]:
            try:
                regex = "{}".format(i)
                r = re.compile(regex)
            except Exception as e:
                with open("python_regex_error_"+kwargs["day"]+".json", "a+") as ef:
                    err_me = {
                        "regex": "{}".format(i), #escape string unsolved
                        "error": "{}".format(e)
                    }
                    b = json.dumps(err_me)
                    ef.write(b+",\n")
                    ef.close()
                # print "Regex : {0} error {1}".format(i, e)
                regex = "{}".format(re.escape(i))
            pattern= r.finditer(kwargs["content"], re.MULTILINE)
            for matchNum, match in enumerate(pattern, start=1):
                if match.end() | match.start():
                    match_me = {
                        "Media": kwargs["media"],
                        "content": kwargs["content"],
                        "regex": i.decode('unicode_escape'),
                        "match_found": match.group(),
                    }
                    data = json.dumps(match_me)
                    with open("log_ambigu_"+kwargs["day"]+".json", "a+") as f:
                        f.write(data+",\n")
                        f.close()
                    return True
                else:
                    continue        
        return False