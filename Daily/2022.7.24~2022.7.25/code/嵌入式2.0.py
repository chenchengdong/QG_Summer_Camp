import pandas as pd
import sqlalchemy
import numpy as np
from  sklearn.cluster import KMeans
from flask import Flask


class ClusterPred():

    def __init__(self):
        '''初始化'''
        self.engine = None
        self.training_set = None
        self.cluster = None
        self.centroid = None
        self.sql_one = None
        self.row_two = None
        self.row_one = None

    def read_db(self):
        global mysql_his_list
        self.engine = sqlalchemy.create_engine('mysql+pymysql://root:3751ueoxjwgixjw3913@39.98.41.126:3306/exclusive_plug')
        for i in range(len(mysql_his_list)):
            sql = 'select * from' + mysql_his_list[i] + 'where current !=0 and id between 2525620 and 2526119'
            df = pd.read_sql(sql, self.engine)
            if i == 0:
                self.training_set = np.array([df['current'], df['voltage'], df['power'], df['power_faction'],
                                         df['cumulative_power']]).T
            else:
                tem_training_set = np.array([df['current'], df['voltage'], df['power'], df['power_faction'],
                                             df['cumulative_power']]).T
                self.training_set = np.vstack((self.training_set, tem_training_set))

    def clu_history(self):
        global n_clusters
        self.cluster = KMeans(n_clusters=n_clusters, random_state=0).fit(self.training_set)

    def get_centroid(self):
        self.centroid = self.cluster.cluster_centers_
        return self.centroid

    def get_recent_info(self):
        global mysql_rece_list
#        这里要想办法只读一条最新信息
        self.sql_one = 'select * from' + mysql_rece_list[0] + 'where current !=0 and id between 2525620 and 2526119'
        self.row_one = pd.read_sql(self.sql_one, self.engine)
        row_one_tem = np.array([self.row_one['current'], self.row_one['voltage'], self.row_one['power'], self.row_one['power_factor'],
                            self.row_one['cumulative_power']]).T
        self.row_two = np.vstack((row_one_tem, np.zeros((1, 5))))

    def device_pred(self):
        pred = self.cluster.fit_predict(self.row_two)
#       根据字典得出是什么用电器，并修改name特征量
        return pred

    def written_db(self):
#       将数据重新写回数据库
        self.row_one.to_sql('xxx', self.engine, )














if __name__ == '__main__':
    mysql_his_list = ['device20200709', 'device20200710', 'device20200711', 'device20200712', 'device20200713',
                      'device20200714', 'device20200715', 'device20200716']
    mysql_rece_list = []
    n_clusters = 3
    #用电器字典
    elec_items = {}
    a = ClusterPred()


