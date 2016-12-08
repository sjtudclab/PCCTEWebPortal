__author__ = 'Kaiyang Lv'


class DbM:
    def __init__(self, db):
        self.db = db

    def update(self, *, table, condition='', form_dict={}, **kwargs):
        sql = 'update ' + table + ' set '
        for key, val in form_dict.items():
            sql += key + '=' + repr(val[0]) + ', '
        for key, val in kwargs.items():
            sql += key + '=' + repr(val) + ', '
        sql = sql[:-2] + ' ' + condition
        print(sql)
        status = self.db.execute(sql)
        return status

    def insert(self, *, table ,  **kwargs):
        sql = 'insert into ' + table + ' ('
        for key in kwargs.keys():
            sql += key + ', '
        sql = sql[:-2] + ') values ('
        for val in kwargs.values():
            sql += repr(val) + ', '
        sql = sql[:-2] + ' )'
        print(sql)
        status = self.db.execute(sql)
        return status
