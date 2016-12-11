import MySQLdb
data = "["
db = db = MySQLdb.connect(host,username,password,database)
cursor = db.cursor()
cursor.execute("select * from raw_data order by time desc;")
for i in range(cursor.rowcount):
       row = cursor.fetchone()
       list = "{\"time\":"+str(row[0])+",\"mos1\":"+str(row[1])+","\
              "\"mos2\":"+str(row[2])+",\"tmp1\":"+str(row[3])+","\
              "\"tmp2\":"+str(row[4])+",\"light_in\":"+str(row[5])+","\
              "\"light_out\":"+str(row[6])+"}"
       if((i+1)==cursor.rowcount):
              list+="]"
       else:
              list+=","
              data+=list
db.close()
