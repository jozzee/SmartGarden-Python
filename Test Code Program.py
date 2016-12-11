import MySQLdb
data = "["
db = db = MySQLdb.connect(host,username,password,database)
cursor = db.cursor()
cursor.execute("select * from log_data order by time desc;")
for i in range(cursor.rowcount):
      row = cursor.fetchone()
      js = "{\"time\":"+str(row[0])+",\"working\":"+str(row[1])\
      +",\"type\":"+str(row[2])+",\"val_berfore\":"+str(row[3])\
      +",\"val_after\":"+str(row[4])+"}"
      if((i+1)==cursor.rowcount):
            js+="]"
      else:
            js+=","
      data+=js
db.close()
