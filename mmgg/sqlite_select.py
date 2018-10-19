import sqlite3

def select(s="thumbnail"):
    conn = sqlite3.connect("mmg.db")
    c = conn.cursor()
    result = c.execute("select {} from maogou".format(s))
    data = result.fetchall()
    print(type(data))
    print(len(data))
    conn.close()

    return data
select()