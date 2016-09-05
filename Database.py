import MySQLdb
import json
import SharedPreferences as sp
import Time as tm

host = "localhost"
username = "root"
password = "ecpsmartgarden"
database = "SmartGarden7"
dayStorage = "dayStorage"
dayAsTimeStamp = 86400 # 1 day = 86400 in timeStamp

initSharedPreferences()

def initSharedPreferences():
    sp.getSharedPreferences("Memoery")

def testConnectDB():
    print("Database: testConnectDB")
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
def insertLogData(time,action,typeA):
    print("Database: insertLogData --> action: "+str(action)+", type: "+str(typeA))
    initSharedPreferences()
    lessTime = (int(time)-(int(sp.get(dayStorage))*int(dayAsTimeStamp)))
    print("  - lessTime: "+str(tm.timeStamp2Date(lessTime)))
    try:
        db = db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        sql = "insert into log_data (action,type,time)"\
              "values (" +str(action) +", "+str(typeA) +", \""+str(time) +"\");"
        cursor.execute(sql)
        db.commit()
        sql = "delete from log_data where time < \"" +str(lessTime)+"\";"
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error:
        print("  - Database: Error")
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")
def insertRawData(time,moisture,temp,light):
    print("Database: insertRawData")
    initSharedPreferences()
    lessTime = (int(time)-(int(sp.get(dayStorage))*int(dayAsTimeStamp)))
    print("  - lessTime: "+str(tm.timeStamp2Date(lessTime)))
    try:
        db = db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        sql = "insert into raw_data (moisture,temp,light,time)"\
              "values (" +str(moisture) +", "+str(temp)+", "+str(light) +", \""+str(time) +"\");"
        cursor.execute(sql)
        db.commit()
        sql = "delete from raw_data where time < \"" +str(lessTime)+"\";"
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error:
        print("  - Database: Error")
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")
def selectRawDataList():
    print("Database: selectRawDataList")
    result = "["
    try:
        db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        cursor.execute("select * from raw_data order by time desc;")
        length = cursor.rowcount
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
            js = json.dumps({"id":row[0],"time":row[1],"moisture":row[2],"temp":row[3],"light":row[4]})
            if((i+1)==length):
                js+="]"
            else:
                js+=","
            result+=js
        #print(str(detailsList[0]))
    except MySQLdb.Error:
        print("  - Database: Error" )
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")

    return result
def selectLogDataList():
    print("Database: selectLogData2")
    result = "["
    try:
        db = MySQLdb.connect(host,username,password,database)#localhost,username,password,Database name
        cursor = db.cursor()
        sql= "select * from log_data order by time desc;"
        cursor.execute(sql)
        
        length = cursor.rowcount
        for i in range(cursor.rowcount):
            row = cursor.fetchone()
            js = json.dumps({"id":row[0],"time":row[1],"action":row[2],"type":row[3]})
            if((i+1)==length):
                js+="]"
            else:
                js+=","
            result+=js
        #print(str(detailsList[0]))
    except MySQLdb.Error:
        print("  - Database: Error" )
    finally:
        if db:
            db.close()
            print("  - Database: close connection..." +"\n")
    return result

