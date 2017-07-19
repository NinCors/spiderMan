import sqlite3

url = "try_sql.db"
table_name = "info"


def create_table():
    sql3_db = sqlite3.connect(url)
    db = "create table {} (url varchar(1024), title varchar(256), teacher varchar(128), study_num int, tag varchar(256), types varchar(256), info varchar(1024), tests_name varchar(1024))".format(table_name)

    try:
        sql3_db.execute(db)
    except:
        print("No db file here!")
        return False
    print("Good")
    sql3_db.close()


