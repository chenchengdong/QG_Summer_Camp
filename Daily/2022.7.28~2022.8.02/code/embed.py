import json
import pandas as pd
import sqlalchemy
import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, request, jsonify


app = Flask(__name__)
#   将自动编码集关闭
app.config['JSON_AS_ASCII'] = False


@app.route('/getdata/<data>', methods=['GET', 'POST'])
def getdata(data):
    global a
    print(type(data))
    print(data)
    data = dict(json.loads(data))
    if data['current'] == 0:
        return jsonify('没有用电器')
    pre = predict(data)
    return jsonify(pre)


class ClusterPred():

    def __init__(self):
        self.engine = sqlalchemy.create_engine('mysql+pymysql://root:3751ueoxjwgixjw3913@39.98.41.126:3306/qg_mid')
        self.training_set = None
        self.his_db = None
        self.cluster = None
        self.centroid = None
        self.labels = None
        self.index_list = []

    def read_db(self):
        global mysql_his_list, value_order
        for index in range(len(mysql_his_list)):
            sql = 'select * from ' + mysql_his_list[index] + ' where current !=0 and voltage >=231 and ' \
                                                             'power_factor >0 and power>0 '
            df = pd.read_sql(sql, self.engine)
            # df = df.drop(df[(df['name'] == 'phone') | (df['name'] == 'Hot_melt_gun')].index)
            self.index_list.append(len(df['id']))
            if index == 0:
                self.training_set = np.array(df)
            else:
                tem_training_set = np.array(df)
                self.training_set = np.vstack((self.training_set, tem_training_set))
        self.his_db = self.training_set
        print('****')
        # print(f'未提取特征量的数据集大小为: {self.his_db.shape}')
        #   将历史数据提取特征量
        self.training_set = np.array(self.training_set[:, value_order], dtype=float)
        print('切割后的特征量数据集')
        print(self.training_set[0, :])
        self.training_set[:, 0] *= 3000.0
        self.training_set[:, 1] -= 0
        self.training_set[:, 2] *= 100
        print(self.training_set[0, :])
        print('****')
        # print(f'提取特征量后数据集大小为: {self.training_set.shape}')

    def clu_history(self):
        global n_clusters, dic, columns_list, mysql_t_list
        self.cluster = KMeans(n_clusters=n_clusters, random_state=0).fit(self.training_set)
        self.labels = self.cluster.labels_
        self.labels = list(self.labels)
        print('*分类对应序号*')
        print(self.labels)
        print("统计每个类的个数")
        # for i in range(12):
        #     print(f'第{i+1}类出现个数：{self.labels.count(i)}')
        #   将历史数据打上标签后
        self.his_db[:, 1] = self.labels
        print('*打上标签之后的历史数据')
        print(self.his_db)
        #  将历史数据再次恢复表头后
        self.his_db = pd.DataFrame(self.his_db, columns=columns_list)
        print('*恢复表头后的历史数据')
        print(self.his_db)
        #   将历史数据写入数据库新表
        tem1 = 0
        for i in range(len(mysql_t_list)):
            tem_df = self.his_db.iloc[tem1:tem1+self.index_list[i], :]
            tem1 = self.index_list[i]
            print('*切割后的数据表')
            print(type(tem_df))
            print(tem_df)
            tem_df.to_sql(mysql_t_list[i], self.engine, if_exists='replace', index=False)

    def get_centorid(self):
        self.centroid = self.cluster.cluster_centers_
        print(self.centroid)


def predict(dic_data):
    global values, n_clusters, dic, centers
    l = ['current', 'voltage', 'power', 'power_factor']
    feature = [dic_data[l1] for l1 in l]
    print(feature)
    #   对特征量进行放缩
    feature[0] *= 3000.0
    feature[1] -= 0
    feature[2] *= 100
    min_index = 0
    #   判断属于哪一个聚类中心
    for i in range(centers.shape[1]):
        if i == 0:
            distance1 = np.sum(np.square(centers[:, i] - feature))
        else:
            distance2 = np.sum(np.square(centers[:, i] - feature))
            if distance2 < distance1:
                min_index = i
    print(dic[min_index])
    return dic[min_index]


if __name__ == '__main__':
    mysql_his_list = ['qgDevice20220730']
    mysql_t_list = ['Data20220730']
    value_order = ['current', 'voltage', 'power', 'power_factor']
    columns_list = ['id', 'name', 'current', 'voltage', 'power', 'date', 'index_num', 'power_factor', 'frequency',
                    'cumulative_power']
    dic = {0: 'phone', 1: ' computer', 2: 'oscilloscope', 3: 'oscilloscope', 4: 'router', 5: 'Hot_melt_gun', 6: 'phone',
           7: 'computer', 8: 'Hot_melt_gun', 9: 'singlechip', 10: 'computer', 11: 'Hot_melt_gun'}
    #   5个特征值
    values = 4
    #   假设有5个用电器、簇心
    n_clusters = 12
    #   簇心
    centers = np.array([[1.52142857e+02, 2.36070771e+02, 3.27617143e+02, 2.74531429e-01],
                         [7.06956522e+02, 2.34704435e+02, 4.17653478e+03, 7.55100000e-01],
                         [2.94757895e+02, 2.35131158e+02, 1.19731158e+03, 5.18526316e-01],
                         [2.58520661e+02, 2.34924240e+02, 9.81286777e+02, 4.86166116e-01],
                         [4.21363636e+01, 2.34960705e+02, 1.56527273e+02, 4.79812500e-01],
                         [1.99687500e+02, 2.35353875e+02, 1.52695625e+03, 9.74425000e-01],
                         [1.62610169e+02, 2.35328288e+02, 6.40467797e+02, 5.02606780e-01],
                         [7.95600000e+02, 2.34767000e+02, 4.87000000e+03, 7.81780000e-01],
                         [1.35933333e+02, 2.34822533e+02, 1.03704889e+03, 9.72448889e-01],
                         [1.80000000e+01, 2.35627290e+02, 6.09403226e+01, 4.06451613e-01],
                         [6.66000000e+02, 2.34603375e+02, 3.87943750e+03, 7.45475000e-01],
                         [1.65444444e+02, 2.34992111e+02, 1.25838519e+03, 9.72625926e-01]]).T
    #   创建类对象
    if False:
        # 创建类对象
        a = ClusterPred()
        #   对历史数据进行标签
        a.read_db()
        a.clu_history()
        a.get_centorid()
    if False:
        engine_read = sqlalchemy.create_engine('mysql+pymysql://root:3751ueoxjwgixjw3913@39.98.41.126:3306/qg_mid')
        for i in range(len(mysql_t_list)):
            sql_t = 'select * from ' + mysql_t_list[i]
            read_df = pd.read_sql(sql_t, engine_read)
            print(read_df)
            for k, j in zip(read_df['name'], range(len(read_df['name']))):
                read_df.iloc[j, 1] = dic[k]
            read_df.to_sql(mysql_t_list[i], engine_read, if_exists='replace', index=False)

    #   拿到簇心之后要给他打标签
    #   访问路由时返回标签
    app.run(host='0.0.0.0', port=8082)



