import sqlite3


def create_db():
    sql = sqlite3.connect('mmgg.db')
    print("connect success")
    c = sql.cursor()
    c.execute('''CREATE TABLE maogou (
        id INTEGER,
        topic VARCHAR(255),
        shorturl VARCHAR(100),
        thumbnail VARCHAR(255),
        PRIMARY KEY (id)
    )''')
    sql.commit()
    print("Table create successfully")
    sql.close()


class DataOutput:
    def __init__(self):
        self._sql = sqlite3.connect('mmgg.db')
        print("connect success")

    def __del__(self):
        self._sql.close()

    def store_data(self, data):
        if not data:
            return
        self.data = data

    def output_db(self):
        for item in self.data:
            c = self._sql.cursor()
            c.execute('''insert into maogou (id,topic,shorturl,thumbnail) values (?,?,?,?)''',
                      (item['id'], item['topic'], item['shorturl'], item['thumbnail']))
            self._sql.commit()
