import pymysql

conn=pymysql.connect(host='localhost',user='root',passwd='uisf1002',charset='utf8',port=3306)
cur = conn.cursor()
cur.execute("show databases")
databases = []
for iter in cur:
    databases.append(iter)
print(databases)
conn.select_db("student")
cur.execute("show tables")
tables_list=cur.fetchall()
for i in tables_list:
    print(' '.join(i))
insert_value = (123456)
cur.execute('insert into new_student(no) values(%s)',insert_value)
conn.commit()