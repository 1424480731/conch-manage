from pymongo import MongoClient

import urllib.parse as parse
import base64
import time
settings = {
    "ip":'127.0.0.1',
    "port":27017,
}

class MongoBase(object):

    def __init__(self):

        try:
            self.conn = MongoClient(settings["ip"], settings["port"])
        except Exception as e:
            raise e

    def get_table(self,dbname,setname):

        dbconn = None
        table_conn = None

        try:
            dbconn = self.conn[dbname]
            table_conn = dbconn[setname]
        except:
            print('connect exception!!!')
        return table_conn

    def insert(self,dbname,setname,dic):
        
        table_conn = self.get_table(dbname,setname)
        table_conn.insert(dic)

    def update(self, dbname,setname,dic, newdic):
        table_conn = self.get_table(dbname, setname)
        table_conn.update(dic, newdic)

    def delete(self, dbname,setname,dic):
        table_conn = self.get_table(dbname, setname)
        status = table_conn.remove(dic)
        return status
    def dbFind(self, dbname,setname,dic):
        table_conn = self.get_table(dbname, setname)
        data = table_conn.find(dic)
        data = list(data)
        return data

    def findAll(self,dbname,setname,):

        table_conn = self.get_table(dbname, setname)
        for i in table_conn.find():
            print(i)

class  MongoChengJiApi(MongoBase):

    def __init__(self):
        self.dbname = 'zf'
        self.setname = 'cjzf'
        super().__init__()

    def base_all(self):

        ret = []
        table_conn = self.get_table(self.dbname,self.setname)
        ret_list = list(table_conn.find({'id':'市名'},{'area':1,'district_box.district':1,'district_box.road_box.html_box':1}))

        for data in ret_list:
            area = data.get('area')
            district_box = data.get('district_box')
            district_num = len(district_box)
            road_num=0
            html_num=0
            for district in district_box:
                road_box = district.get('road_box')
                road_num += len(road_box)
                for road_e in road_box:
                    html_num += len(road_e.get('html_box'))
            ret.append({'area':area,'district_num':district_num,'road_num':road_num,'html_num':html_num})
        return ret

    def get_detail_msg_by_area(self,cond):

        ret = []
        table_conn = self.get_table(self.dbname,self.setname)
        ret_list = list(table_conn.find({'id':'市名','area':cond.get('area')},{'district_box.district':1,'district_box.road_box.road':1,'district_box.road_box.html_box':1}))

        for data in ret_list:
            district_box = data.get('district_box')
            for district in district_box:

                road_box = district.get('road_box')
                district_name = district.get('district')
                print(district_name)
                for road in road_box:
                    road_c = road.get('road')
                    html_box = road.get('html_box')
                    if html_box:
                        ret.append({'district_name':district_name,'road':road,'html_num':len(html_box)})
        return ret

    def get_area_district(self):
        table_conn = self.get_table(self.dbname,self.setname)
        ret_list = list(table_conn.find({'id':'市名'},{'area':1,'district_box.district':1,'_id':0}))
        return ret_list

    def get_fymsg_by_area_district(self,cond):

        area = cond.get('area')
        district = cond.get('district')
        ret_list = []
        pipeline = [
                {'$match':{'area':area,'district_box.district':district}},
                {'$unwind':'$district_box'},
                {'$match':{'district_box.district':district}},
                {'$project':{'area':1,'district_box.district':1,'district_box.road_box.road':1,'district_box.road_box.html_box':1,'_id':0}},

            ]
        table_conn = self.get_table(self.dbname, self.setname)
        ret_data = list(table_conn.aggregate(pipeline))[0]
        road_box = ret_data.get('district_box').get('road_box')
        if road_box:
            for road in road_box:
                if road.get('html_box'):
                   ret_list.append(road)
        print(ret_list)
        return ret_list


if __name__ == '__main__':

   ml = MongoBase()
   ml = MongoChengJiApi()
   dbname = 'zf'
   setname = 'cjzf'
   # print(ml.base_all())
   # print(ml.get_detail_msg_by_area({'area':'北京'}))
   # ml.get_area_district()
   ml.get_fymsg_by_area_district({'area':'阿里','district':'噶尔县'})
   # ml.get_fymsg_by_area_district({'area':'阿勒泰','district':'阿勒泰市'})
