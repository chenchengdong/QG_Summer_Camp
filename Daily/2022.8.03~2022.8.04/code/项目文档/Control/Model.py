import pandas as pd
import numpy as np
import hashlib
import sqlalchemy
import pymysql
import datetime
import random
import jieba

class Model:

    def __init__(self):
        self.sql_acc = 'mysql+pymysql://root:3751ueoxjwgixjw3913@39.98.41.126:3306/book_management'
        self.user_mysql_name = ''
        self.book_mysql_name = 'library'
        self.engine = sqlalchemy.create_engine(self.sql_acc)
        self.conn = pymysql.connect(host="39.98.41.126",
                                    port=3306,
                                    user="root",
                                    password="3751ueoxjwgixjw3913",
                                    db="book_management",
                                    charset="utf8")
        self.cursor = self.conn.cursor()
        self.k1 = '%5cu#-jeq15abg$z9_i#_w=$o88m!*al?edl>bat8cr74sid'
        self.values = ['bookIndex', 'title', 'cover', 'author', 'translator', 'publishTime', 'tag', 'point',
                       'readingCount', 'goodCount', 'starCount', 'bookInfo', 'authorInfo', 'review', 'publishHouse',
                       'pointCount']

    def book_to_index(self, book):
        """
        change the name of the book into the id of the book
        :param book: the name of the book --> str
        :return: the id of the book --> int
        """
        sql = 'select * from ' + self.book_mysql_name + ' where title = ' + book
        book_df = pd.read_sql(sql, self.engine)
        return str(int(book_df["bookIndex"]))

    def index_to_book(self, book_index):
        """
        change the id of the book into the name of the book
        :param book_index: the id of the book --> str
        :return: the name of the book --> str
        """
        sql = 'select * from ' + self.book_mysql_name + ' where bookIndex = %d ' % int(book_index)
        book_df = pd.read_sql(sql, self.engine)
        return str(np.array(book_df["title"])[0])

    def user_to_id(self, user):
        """
        change the username into the id of user
        :param user: the name of the user --> str
        :return: the id of the user --> int
        """
        sql = 'select * from ' + self.user_mysql_name + ' where user_name = ' + user
        user_df = pd.DataFrame(sql, self.engine)
        return int(user_df["id"])

    def praise(self, user_name, book_praised):
        """
        which is used to praise one book
        :param user_name: who want to praise the book --> str
        :param book_praised: the name of the book which will be praised --> str
        """
        sql = 'select * from ' + self.user_mysql_name + ' where user_name = ' + user_name
        user_df = pd.read_sql(sql, self.engine)
        sql = 'select * from ' + self.book_mysql_name + ' where title =' + book_praised
        book_df = pd.read_sql(sql, self.engine)

        if Model.book_to_index(self, book_praised) in np.array(user_df["praise"])[0]:
            self.conn.ping(reconnect=True)
            sql = 'update ' + self.user_mysql_name + ' set praise = %s where id = %s'
            self.cursor = self.conn.cursor()
            rows = self.cursor.execute(sql, (str(np.array(user_df['praise'])[0].remove(book_praised)),
                                             str(int(user_df["id"]))))
            self.conn.commit()
            self.cursor.close()

            self.cursor = self.conn.cursor()
            sql = 'update ' + self.book_mysql_name + ' set goodCount = %s where title = %s'
            rows = self.cursor.execute(sql, (str(int(book_df['goodCount']) - 1), book_praised))
            self.conn.commit()
            self.cursor.close()
        else:
            self.conn.ping(reconnect=True)
            sql = 'update ' + self.user_mysql_name + ' set praise = %s where id = %s'
            self.cursor = self.conn.cursor()
            rows = self.cursor.execute(sql, (str(np.array(user_df['praise'])[0] + [book_praised]),
                                             str(int(user_df["id"]))))
            self.conn.commit()
            self.cursor.close()

            self.cursor = self.conn.cursor()
            sql = 'update ' + self.book_mysql_name + ' set goodCount = %s where title = %s'
            rows = self.cursor.execute(sql, (str(int(book_df['goodCount']) + 1), book_praised))
            self.conn.commit()
            self.cursor.close()


    def collect(self, user_name, book_collected):
        """
        which is used to collect one book by a user
        :param user_name: who want to collect the book --> str
        :param book_collected: the name of the book which will be collected --> str
        """
        self.conn.ping(reconnect=True)
        sql = 'select * from ' + self.user_mysql_name + ' where user_name =' + user_name
        user_df = pd.read_sql(sql, self.engine)
        sql = 'select * from ' + self.book_mysql_name + ' where title =' + book_collected
        book_df = pd.read_sql(sql, self.engine)

        if Model.book_to_index(self, book_collected) in np.array(user_df["praise"])[0]:
            sql = 'update ' + self.user_mysql_name + ' set praise = %s where id = %s'
            self.cursor = self.conn.cursor()
            rows = self.cursor.execute(sql, (str(np.array(user_df['praise'])[0].remove(book_collected)),
                                             str(int(user_df["id"]))))
            self.conn.commit()
            self.cursor.close()
        else:
            sql = 'update ' + self.user_mysql_name + ' set praise = %s where id = %s'
            self.cursor = self.conn.cursor()
            rows = self.cursor.execute(sql, (str(np.array(user_df['praise'])[0] + [book_collected]),
                                             str(int(user_df["id"]))))
            self.conn.commit()
            self.cursor.close()

            self.cursor = self.conn.cursor()
            sql = 'update ' + self.book_mysql_name + ' set goodCount = %s where title = %s'
            rows = self.cursor.execute(sql, (str(int(book_df['starCount']) + 1), book_collected))
            self.conn.commit()
            self.cursor.close()

    def review(self, user, book, url, review):
        """
        which is used when user want to give a review to the book, where url is the access of the user's picture
        :param user: the name of the user --> str
        :param book: the name of the book --> str
        :param url: the access of the user's picture --> str
        :param review: what user will give to the book --> str
        :return: the final status of this function --> str
        """
        self.conn.ping(reconnect=True)
        sql = 'select * from ' + self.book_mysql_name + ' where title =' + book
        book_df = pd.read_sql(sql, self.engine)

        sql = 'update' + self.book_mysql_name + 'set review = %s where title = %s'
        rows = self.cursor.execute(sql, (str(list(np.array(book_df["review"])[0]) + [user + '-' + url + '-' + review]),
                                         book))
        self.conn.commit()
        self.cursor.close()

        sql = 'update' + self.book_mysql_name + ''

    def find(self, wanted_word, book_info_flag=False):
        """
        find something, which is based on something known un_clearly
        :param wanted_word: something known un_clearly --> str
        :param book_info_flag: check if we use the book_info to find, which is set because it's really slow
                               if we use the book_info, but we think that it is necessary --> True or False
        :return: some book which may be what user want to find --> [str]
        """
        sql = 'select title, author, bookInfo from ' + self.book_mysql_name
        book_df = pd.read_sql(sql, self.engine)
        wanted_word_list = [x for x in jieba.cut(wanted_word, cut_all=True)]
        poit_number_list = []

        book_mat = np.array(book_df)
        for i in range(np.shape(book_mat)[0]):
            temp_point = 0
            if wanted_word == book_mat[i, 1]:
                poit_number_list.append(float("inf"))
                continue
            elif wanted_word in book_mat[i, 1]:
                temp_point += 7 * len(wanted_word)
            temp_point += len([x for x in jieba.cut(book_mat[i, 0], cut_all=True) if x in wanted_word_list]) * 5
            if book_info_flag:
                temp_point += len([x for x in jieba.cut(book_mat[i, 2])])
            poit_number_list.append(temp_point)
        sorted_id = sorted(range(len(poit_number_list)), key=lambda k: poit_number_list[k], reverse=True)
        print(sorted_id)
        return [Model.simple_show(self, x) for x in sorted_id[:100]]

    def register(self, register_data):
        """
        user who doesn't register in this system will register a unique account number for him
        :param register_data: which content user's nickname,password and Confirm password  all --->str
        :return:the final status of this function --->str
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        values = ['user_name', 'password', 'repassword', 'phone_number', 'email']
        user = []
        for k in values:
            user.append(register_data[k])

        if user[2] != user[1]:
            return {"WARNING: THE PASSWORD YOU INPUT TWICE ARE NOT THE SAME"}
        else:
            rows = self.cursor.execute(' select * from ' + ' users where user_name= %s', user[0])
            if rows != 0:
                return {"WARNING: THE USER NAME HAS BEEN OCCURRED"}
            else:
                if len(user[3]) != 11 or str(user[3])[0] != '1' or str(user[3]).isdigit() is not True:
                    return {"WARNING: THE PHONE NUMBER GIVED IS WRONG"}
                elif '@' not in str(user[4]) or '.com' not in str(user[4]):
                    return {"WARNING: THE EMAIL GIVED IS WRONG"}
                else:
                    #  DELETE THE REINPUT PASSWORD
                    user.pop(2)
                    #   PASSWORD ENCRYPTION
                    h1 = hashlib.md5()
                    h1.update(user[1].encode(encoding='utf-8'))
                    user[1] = h1.hexdigest()
                    user.append('[]')
                    user.append('[]')
                    user.append('hello')
                    user.append('url')
                    user = tuple(user)
                    sql = ' insert into ' + \
                          ' users(user_name, password, phone_number,' \
                          ' email, praise, collect, signature, user_url) ' + ' value (%s, %s, %s, %s, ' \
                                                                             '%s, %s, %s, %s) '
                    rows = self.cursor.execute(sql, user)
                    self.conn.commit()

                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    bg = tuple((user[0], time_now, 'login'))
                    self.written_bg(bg)
                    self.cursor.close()
                    return 'SUCCESS'

    def login(self, login_data):
        """
        user who had been registered in the system login this system
        :param login_data: which contains user_name and user's password --->{str:str}
        :return:if user successfully login we return user's nickname which is encrypted --->{str:str}
                else we return the warning of the login status --->{str}
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        values = ['user_name', 'password']
        user = []
        for k in values:
            user.append(login_data[k])
        rows = self.cursor.execute('select * from ' + ' users where user_name =%s ', user[0])
        if rows == 0:
            return {"WARNING: THE USER IS NOT EXIST"}
        else:
            msg = self.cursor.fetchone()
            h1 = hashlib.md5()
            h1.update(user[1].encode(encoding='utf-8'))
            if h1.hexdigest() != msg[2]:
                return {"WARNING: THE PASSWORD IS WRONG"}
            else:
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                bg = tuple((user[0], time_now, 'login'))
                # RETURN THE ENCRYPTED USER_NAME --->DICT
                self.written_bg(bg)
                return {"user_name": self.en_ctry(user[0])}


    def logout(self, logout_data):
        """
        user who are in the system logout the system
        :param logout_data: which is a tuple contains user_name,time_now and operation --->tuple
        :return: NONE
        """
        self.written_bg(logout_data)

    def update_user_url(self, url):
        """
        user who had been registered in the system update his head portrait
        :param url: which is a tuple contains user_url and user_name --->tuple
        :return: NONE
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        sql = 'update users ' + 'set user_url =%s where user_name =%s'
        rows = self.cursor.execute(sql, url)
        self.conn.commit()
        self.cursor.close()

    def id_to_user(self, user_id):
        """
        change the user_id into user_name
        :param user_id: user_id in database --->str
        :return: user_name --->str
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        rows = self.cursor.execute('select user_name from ' + 'users where id=%s', user_id)
        user_name = self.cursor.fetchone()
        self.cursor.close()
        return user_name

    def change_password(self, way):
        """
        user who had been registered in the system change the password
        :param way: which is a dict contains user_name, phone_number, email, old_password and new_password --->{str:str}
        :return:the status of changing password's operation --->{str}
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        values1 = ['phone_number', 'email', 'old_password']
        values2 = ['user_name', 'phone_number', 'email', 'old_password', 'new_password']
        verification = [way[i] for i in values1]
        user = [way[i] for i in values2]
        user[0] = self.de_ctry(user[0])
        h1 = hashlib.md5()
        h1.update(verification[-1].encode(encoding='utf-8'))
        verification[-1] = h1.hexdigest()
        rows = self.cursor.execute('select phone_number, email, password ' + ' from users where user_name=%s', user[0])
        true_data = self.cursor.fetchone()
        if verification[0] == true_data[0] or verification[1] == true_data[1] or verification[2] == true_data[2]:
            h1.update(user[-1].encode(encoding='utf-8'))
            new_password = h1.hexdigest()
            sql = 'update users ' + 'set password = %s where user_name =%s'
            tuple_password = tuple((new_password, user[0]))
            self.cursor.execute(sql, tuple_password)
            #   WRITEBACK TO BACKGROUND SYSTEM
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bg = tuple((user[0], time_now, 'editpassword'))
            self.written_bg(bg)
            self.cursor.close()
            return {"SUCCESS"}
        else:
            self.cursor.close()
            return {"WARNING: ALL YOU GIVED ARE WRONG"}

    def signature_edit(self, signature, user):
        """
        user who had been registered in the system edit his signature
        :param signature: the signature which the user want to edit --->{str:str}
        :param user: user's nickname which is encrypted --->str
        :return: NONE
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        user = self.de_ctry(user)
        signature_tuple = tuple((signature, user))
        sql = 'update users ' + 'set signature = %s where user_name=%s'
        rows = self.cursor.execute(sql, signature_tuple)
        self.conn.commit()
        self.cursor.close()

    def written_bg(self, bg):
        """
        write the operation of the user to the database
        :param bg: the operation and time of the user --->tuple
        :return: NONE
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        sql = 'insert into ' + 'bg(user_name, time, operation) value(%s, %s, %s)'
        rows = self.cursor.execute(sql, bg)
        self.cursor.close()

    def detail_show(self, user_name, bookIndex):
        """
        show the detail information of a concrete book
        :param user_name: user's nickname which is encrypted --->str
        :param bookIndex:the concrete book's index in the database
        :return:the detail information of a book --->{str:{}}
        """
        key_words = ['user_name', 'user_url', 'context']
        self.cursor = self.conn.cursor()
        rows = self.cursor.execute('select * from ' + ' library where bookIndex = %s', bookIndex)
        book_tuple = self.cursor.fetchone()
        detail = {k: i for k, i in zip(self.values, book_tuple)}
        review = list(detail['review'])
        while '[' and ']' and ',' not in review:
            review.remove()
        detail['review'] = {k: {k2: re for k2, re in zip(key_words, i.split('-'))}
                            for k, i in zip(range(len(review)), review)}
        detail = {'book': detail}
        user_name = self.de_ctry(user_name)
        rows = self.cursor.execute('select praise, collect from ' + ' users where user_name =%s ', user_name)
        user_with_book = self.cursor.fetchone()
        praise = [i for i in list(user_with_book[0]) if i != ',' and i != '[' and i != ']']
        collect = [i for i in list(user_with_book[1]) if i != ',' and i != '[' and i != ']']
        detail['message'] = {'praise': str(any([x == bookIndex for x in praise])),
                             'collect': str(any([x == bookIndex for x in collect]))}
        self.cursor.close()
        return detail

    def simple_show(self, book_index):
        """
        show a book simply by a few information of it
        :param book_index: the concrete book's index in the database --->str
        :return: the simple information of a book --->tuple
        """
        values_tem = ['title', 'cover', 'author', 'tag', 'point', 'pointCount',
                      'readingCount', 'goodCount', 'starCount', 'bookInfo']
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        rows = self.cursor.execute('select title,cover,author,tag,point,pointCount,readingCount,goodCount,'
                                   + ' starCount,bookInfo from library where bookIndex =%s ', book_index)
        book_simple = self.cursor.fetchone()
        print(book_simple)
        print(type(book_simple))
        print(book_index)
        book_simple_dict = {k: i for k, i in zip(values_tem, list(book_simple))}
        self.cursor.close()
        return book_simple_dict

    def ranking(self, signal):
        """
        show the ranking of the books by different factor
        :param signal: the ranking factor --->str
        :return:a list of ranking books of a factor --->list
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        #   THE RETURN LIST
        return_list = []
        #   RANKING BY SCORE
        if signal == 'point':
            rows = self.cursor.execute('select bookIndex,' + ' point from library')
        #   RANKING BY READERS
        elif signal == 'readingCount':
            rows = self.cursor.execute('select bookIndex,' + ' readingCount from library')
        #   RANKING BY COLLECTS
        elif signal == 'starCount':
            rows = self.cursor.execute('select bookIndex, ' + ' starCount from library')
        elif signal == 'goodCount':
            rows = self.cursor.execute('select bookIndex, ' + ' goodCount from library')
        tem_tuple = self.cursor.fetchall()
        tem_list = list(tem_tuple)
        tem_list.sort(key=lambda x: x[1], reverse=True)
        book_id_list = list([idx[0] for idx in tem_list])
        top_point = book_id_list[:100]
        for i in top_point:
            book_simple = self.simple_show(i)
            book_simple['bookIndex'] = i
            return_list.append(book_simple)
        self.cursor.close()
        return return_list

    def hit_recommend(self):
        """
        the hit recommend books of our database
        :return: a list of hit recommend book --->list
        """
        self.conn.ping(reconnect=True)
        self.cursor = self.conn.cursor()
        #   THE RETURN LIST
        return_list = []
        rows = self.cursor.execute('select bookIndex, ' + 'point from library')
        tem_list = list(self.cursor.fetchall())
        tem_list.sort(key=lambda x: x[1], reverse=True)
        need = tem_list[:200]
        L1 = random.sample(range(1, 200), 5)
        for i in L1:
            book_simple = self.simple_show(need[i][0])
            return_list.append(book_simple)
        self.cursor.close()
        return return_list


    def en_ctry(self, s):
        """
        the user's nickname which need to be encrypted
        :param s:user's nickname --->str
        :return: an encrypted nickname
        """
        encry_str = ""
        for i, j in zip(s, self.k1):
            temp = str(ord(i) + ord(j)) + '_'
            encry_str = encry_str + temp
        return encry_str

    def de_ctry(self, p):
        """
        use to decrypt an encrypted nickname
        :param p: an encrypted nickname
        :return: a decrypted nickname
        """
        dec_str = ""
        p = str(p)
        for i, j in zip(p.split("_")[:-1], self.k1):
            temp = chr(int(i) - ord(j))
            dec_str = dec_str + temp
        return dec_str

    def kind(self, kind_num):
        """
        return some book whose kind is what we need
        :param kind_num: the number of the kind we need --> int
        :return: the book simple message list --> [simple_book]
        """
        sql = 'select bookIndex where kind_num = %d' % int(kind_num)
        df = pd.read_sql(sql, self.engine)
        _list = list(np.array(df))
        return [self.simple_show(x) for x in list(random.sample(_list, 100) if len(_list) >= 100 else _list) if x != None]


    def like_book(self, user):
        """
        return some book which we think that the user will like
        :param user: the name of the user --> str
        :return: the book simple message list --> [simple_book]
        """
        test_flag = True
        if test_flag:
            sql = 'select id where user_name = ' + str(user)
            df = pd.read_sql(sql, self.engine)
            _id = int(df['id'])
            return self.kind(_id)[:10]
        sql = 'select pre_book where user_name = ' + str(user)
        df = pd.read_sql(sql, self.engine)
        _list = list(np.array(df)[0])
        return [self.simple_show(x) for x in _list]

    def hot_book(self):
        """
        randomly return the book whose point is great
        :return: the book simple message list --> [simple_book]
        """
        sql = 'select bookIndex where point > 95'
        df = pd.read_sql(sql, self.engine)
        _list = [x[0] for x in np.array(df)]
        return [self.simple_show(x) for x in _list]
