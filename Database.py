import MySQLdb
import json
import preference.SharedPreferences as sp
import Time as t

host = "localhost"
username = "<User Name of MySQL Database>"
password = "<Password>"
database = "<Database Name>"

fqIData = "fqIData"         #frequency to insert data to database
ageData = "ageData"         #day off store data in database
hourStamp = 3600
dayStamp = 86400 # 1 day = 86400 in timeStamp

sp.getSharedPreferences()

def testConnectDB():
    print("Database, testConnectDB")
    try:
        db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print ("  - Database Version: %s" %version)
    except MySQLdb.Error:
        print("  - Database: Error" )
        sys.exit(1)
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")

def insertRawData(timeStamp,moisture,temp,light):
    print("Database: insertDataList")
    result = False
    nextTime = 0
    lessTime = (int(timeStamp)-(int(sp.get(ageData))*int(dayStamp)))

    sql = "insert into raw_data (time,mos1,mos2,tmp1,tmp2,light_in,light_out)"\
          "values (" +str(timeStamp) +", "+str(moisture["point1"])+", "+str(moisture["point2"]) \
          +","+str(temp["point1"])+","+str(temp["point2"])+","+str(light["light_in"])+","+str(light["light_out"]) +");"

    sql2 = "delete from raw_data where time < " +str(lessTime)+";"

    #print(str(sql))
    #print(str(sql2))

    try:
        db = db = MySQLdb.connect(host,username,password,database)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.execute(sql2)
        db.commit()
        result = True
    except MySQLdb.Error:
        print("  - Database: Error")
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")

    if(result):
        nextTime = int(timeStamp) +(int(sp.get(fqIData))*int(hourStamp))
    return result,nextTime
    
def selectRawDataList():
    print("Database: selectDataList")
    result = False
    data = "["
    try:
        db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        cursor.execute("select * from raw_data order by time desc;")
        length = cursor.rowcount
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
                        js = "{\"time\":"+str(row[0])+",\"mos1\":"+str(row[1])+",\"mos2\":"+str(row[2])+",\"tmp1\":"+str(row[3])+",\"tmp2\":"+str(row[4])+",\"light_in\":"+str(row[5])+",\"light_out\":"+str(row[6])+"}"
            if((i+1)==length):
                js+="]"
            else:
                js+=","
            data+=js
        #print(str(data))
        result = True
    except MySQLdb.Error:
        print("  - Database: Error" )
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")

    return result,data

def insertLogData(timeStamp,working,typeA,valBefore,valAfter):
    print(" Database: log data ( working: "+str(working) +", type: "+str(typeA) +" )")
    result = False
    lessTime = (int(timeStamp)-(int(sp.get(ageData))*int(dayStamp)))
    
    try:
        db = db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        sql = "insert into log_data (time,working,working_type,val_before,val_after)"\
              "values (" +str(timeStamp) +", "+str(working) +", "+str(typeA)+", "+str(valBefore) +", "+str(valAfter) +");"
        cursor.execute(sql)
        db.commit()
        sql = "delete from log_data where time < " +str(lessTime)+";"
        cursor.execute(sql)
        db.commit()
        result = True
        
    except MySQLdb.Error:
        print("  Database: Error")
    finally:
        if db:
            db.close()
            print("  success")
            print("  Database: close connection..." +"\n")
    return result

def selectLogDataList():
    print("Database: selectHistoryList")
    result = False
    data = "["
    try:
        db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        sql= "select * from log_data order by time desc;"
        cursor.execute(sql)
        
        length = cursor.rowcount
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
            js = "{\"time\":"+str(row[0])+",\"working\":"+str(row[1])+",\"type\":"+str(row[2])+",\"val_berfore\":"+str(row[3])+",\"val_after\":"+str(row[4])+"}"
            if((i+1)==length):
                js+="]"
            else:
                js+=","
            data+=js
        result = True
    except MySQLdb.Error:
        print("  - Database: Error" )
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")
    return result, data
