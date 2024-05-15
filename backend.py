import sqlite3 as sq

db = 'table.db'

def connect():

    conn = sq.connect(db)

    c = conn.cursor()

    c.execute("""
				CREATE TABLE IF NOT EXISTS data (
					fio text,
					nick text,
					mail text,
					password text primary key,
					phone text,
					adress text,
					date text
)			 
	""")


    conn.commit()
    conn.close()


def enter(fio, nick, mail, password, phone, adress, date):
    conn = sq.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES(?,?,?,?,?,?,?)", (fio, nick, mail, password, phone, adress, date))
    conn.commit()
    conn.close()


def show():
    conn = sq.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM data")


    i = c.fetchall()
    conn.commit()
    conn.close()
    return i




def check():

    if len(show()) == 0:
        return False
    else:
        return True



connect()
