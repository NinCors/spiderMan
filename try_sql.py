import sqlite3

base_url = "try_sql.db"
table_name = "info"


def create_table():
    sql3_db = sqlite3.connect(base_url)
    db = "create table {} (url varchar(1024), title varchar(256), teacher varchar(128), study_num int, tag varchar(256), types varchar(256), info varchar(1024), tests_name varchar(1024))".format(table_name)

    try:
        sql3_db.execute(db)
    except:
        return False
    sql3_db.close()

# Check if one item is exit or not
def query(title):
    sql3_db = sqlite3.connect(base_url)
    query_sql = "select * from {} where title = '{}'".format(table_name,title)
    cu = sql3_db.cursor() # create the cursor for execute sql query
    cu.execute(query_sql)
    record_list = cu.fetchall()
    if len(record_list) > 0:
        return True
    else:
        return False
    return False


def insertData(url, title, teacher, study_num, tag, types, info, tests_name):
    #create the table
    create_table()
    if query(title): # if the title exits, then just update it
        sql3_db = sqlite3.connect(base_url)
        update_sql = "update {} set study_num={}, info='{}', tests_name='{}', url='{}' where title='{}'".format(table_name, study_num, info, tests_name, url, title)

        try:
            sql3_db.execute(update_sql)
            sql3_db.commit()
        except sqlite3.Error as er:
            print ('er:', er.message)
            return False
        sql3_db.close()
        return True
    else:
        sql3_db = sqlite3.connect(base_url) 
        # if the item is not exit, then insert a new one
        insert_sql = "insert into {} (url, title, teacher, study_num, tag, types, info, tests_name) values('{}', '{}', '{}', {}, '{}', '{}', '{}', '{}')".format(table_name,url, title, teacher, study_num, tag, types, info,tests_name)
        try:
            sql3_db.execute(insert_sql)
            sql3_db.commit()
        except sqlite3.Error as er:
            print ('er:', er.message)
            return False
        sql3_db.close()
        return True
    return False



