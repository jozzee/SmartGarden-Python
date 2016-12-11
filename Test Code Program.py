import MySQLdb
db = db = MySQLdb.connect(host,username,password,database)
cursor = db.cursor()
sql = "insert into log_data "\
      "(time,working,working_type,val_before,val_after)"\
      "values (1479101649,1,1,19.65,36.27);"
cursor.execute(sql)
db.commit()
db.close()
