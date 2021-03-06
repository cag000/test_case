import logging
import json

from controller import Controller

class Main(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.db_host = self.config.get("DB_CLIPPER", "db_host")    
        self.db_pwd = self.config.get("DB_CLIPPER", "db_pwd")    
        self.db_user = self.config.get("DB_CLIPPER", "db_user")    
        self.day = self.get_days()
        
    def test_case(self):
        datas = self.read_txt("regex.txt")
        list_media_today = self.get_media_update_today()
        list_error_content = []
        for i in list_media_today:
            logging.info(i)
            try:
                media_content = self.get_content(i)
                for j in media_content:
                    for test in media_content[j]:
                        coba = self.match_regex(
                            media=i,
                            list_of_regex=datas,
                            content=test,
                            day=self.day[0]
                        )
                        if coba:
                            media_error = {
                                j: "Konten Kotor"
                            }
                            list_error_content.append(media_error)
                            break
                        else:
                            break
            except Exception as e:
                logging.error(e)
        with open("media_kontent_kotor_"+self.day[0]+".json", "w") as f:
            json.dump(list_error_content, f)
            f.close()
    
    def get_media_update_today(self):
        con = self.db_con(
            db_host=self.db_host,
            db_pwd=self.db_pwd,
            db_user=self.db_user
        )
        list_media = []
        try:
            cursor = con.cursor()
            query = '''
                SELECT news_media FROM data_news_index_new where news_pubday="{}" GROUP BY news_media
            '''.format(self.day[0])
            cursor.execute(query)
            datas = cursor.fetchall()
            for i in datas:
                list_media.append(i["news_media"])
        except Exception as e:
            logging.error(e)
        finally:
            con.close()
            return set(list_media)
    
    def get_content(self, news_media):
        con = self.db_con(
            db_host=self.db_host,
            db_pwd=self.db_pwd,
            db_user=self.db_user
        )
        data = {}
        try:
            list_content = []
            cursor = con.cursor()
            query = '''
                SELECT
                data_news_content.news_content as content 
                FROM 
                data_news_index_new  
                LEFT JOIN data_news_content ON data_news_index_new.news_id = data_news_content.news_id 
                where news_pubday = "{0}" AND news_media = "{1}" limit 10
            '''.format(self.day[0], news_media)
            cursor.execute(query)
            data = cursor.fetchall()
            for i in data:
                list_content.append(i["content"])
            data = {news_media: list_content}
        except Exception as e:
            logging.error(e)
        finally:
            con.close()
            return data
        
if __name__ == "__main__":
    logging.basicConfig(
            format='[%(asctime)s] - [%(levelname)s] -  MEDIA = %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
    )
    Main().test_case()