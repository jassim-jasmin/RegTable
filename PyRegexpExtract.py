import mysql.connector
import re

class DB:
  def __init__(self):
    print("Just created object")

  def __init__(self, hostName,userName, dbPassword, dbSchema):
    try:
      self.mydb = mysql.connector.connect(host=hostName, user=userName, password=dbPassword, database=dbSchema)
      print(self.mydb)
    except:
      print("Database connectrion error1")

  def setDB(self):
    try:
      print("DB initialized")
      print("Schema: " + self.dbSchema + " host " + self.sql_host + " user name " + self.sql_userName + " password " + self.sql_password)
      self.mydb = mysql.connector.connect(host=self.sql_host, user=self.sql_userName, password=self.sql_password, database=self.dbSchema)
      print(self.mydb)
    except Exception as e:
      print("Database connectrion error2")
      print(e)

  def __init__(self,host,dbSchema):
    try:
      self.dbSchema = dbSchema
      if host == 'zillow':
        print("zillow")
        self.defultZillow()
        self.setDB()
      elif host == 'local':
        print("Local")
        self.defaultLocal()
        self.sql_schemaName = 'mj_db'
      else:
        print("Eroor in host selection")

    except Exception as e:
      print("Database connectrion error3")
      print(e)

  def defultZillow(self):
      self.sql_host = "192.168.15.10"
      self.sql_userName = "root"
      self.sql_password = "softinc"

  def defaultLocal(self):
    self.sql_host = "192.168.15.63"
    self.sql_userName = "root"
    self.sql_password = "softinc"

  def connect(self, hostName,userName, dbPassword, dbSchema):
    try:
      self.mydb = mysql.connector.connect(host=hostName, user=userName, password=dbPassword, database=dbSchema)
      print(self.mydb)
    except:
      print("Database connectrion error4")

  def connect(self):
    try:
      self.mydb = mysql.connector.connect(host=self.sql_host, user=self.sql_userName, password=self.sql_password, database=self.sql_schemaName)
      print(self.mydb)
    except:
      print("Database connectrion error5")

  def createColumn(self,tableName,columnName):
    try:
     mycursor = self.mydb.cursor()
     sql = "ALTER TABLE " + tableName + " ADD COLUMN " + columnName + " LONGTEXT;"
     print(sql)
     mycursor.execute(sql)
    except:
      print("Column not created")

  def reSearchInsertRow(self, tableName, idColumnName, searchColumnName, insertColumnName, whereCondition, patternRE,gNo,sOrR,replaceString):
    self.createColumn(tableName, insertColumnName)
    mycursor = self.mydb.cursor()
    sql = "select " + idColumnName + "," + searchColumnName + " from " + tableName

    if whereCondition:
      sql = sql + " where " + whereCondition
    sql = sql + ";"
    print(sql)
    mycursor.execute(sql)
    sqlInsert =[]
    for id, searchData in mycursor:
      rePattern = eval("re.compile(r'" + patternRE + "')")
      if searchData:
       if rePattern.search(searchData):
          print("Pattern Match")
          if sOrR == "s":
            sql2 ="update " + tableName + " set " + insertColumnName + " = '" + rePattern.search(searchData).group(int(gNo)) + "' where " + idColumnName + " = '" + str(id) + "'"
            sql2 = sql2 + ";"
            sqlInsert.append(sql2)
          if sOrR == "r":
            sqlInsert.append("update " + tableName + " set " + insertColumnName + " = '" + re.sub(patternRE, replaceString, searchData,) + "' where " +  idColumnName + " = '" + str(id) + "';")

    for query in sqlInsert:
      mycursor.execute(query)
      self.mydb.commit()
      print(query)
    print("Query updated successfull",mycursor.rowcount)


  def printRowWithId(self,tableName,idColumnName, columnNameSearch,columnNameInsert):
    sql = "select " + idColumnName + "," + columnNameSearch + "," + columnNameInsert + " from " + tableName + " limit 10;"
    mycursor = self.mydb.cursor()
    mycursor.execute(sql)
    dataDic= dict()
    for id,data,data2 in mycursor.fetchall():
      if data2:
        dataDic[id] = data + "__________:- " + data2
      else:
        dataDic[id] = data
    return dataDic

  def disconnect(self):
    try:
      self.mydb.close
    except:
      print("Exception in closing the db")

  def __del__(self):
    try:
      print("Disconnected")
      self.mydb.close
    except:
      print("Exception in closing the db")


#obj = DB("local")
#obj.connect()


#sql_schema = "nc_perquimans_rawdata"
#sql_table_name = "zillow_mail_address_fromtool"
#sql_idColumnName = "mail_address_record_id"
#sql_columnName = "mail_full_street_address"
#sql_eColumnName = "mail_zip"
#sql_condition = " mail_city is null and mail_full_street_address is not null and mail_international_address_flag is null  mail_full_street_address regexp '^[0-9] .* [A-Z][A-Z] [0-9][0-9][0-9][0-9][0-9]$'  "
#regexp = ' (\z\z) '
#group = '1'
#op = 's' # s for extract r for replace
#rstring = '' #if any

#test = DB(sql_host,sql_userName, sql_password, sql_schema)
#data = test.printRow("name_source_file","id", "Taxpayer_Address_2")


#test.reSearchInsertRow(sql_table_name, sql_idColumnName, sql_columnName, sql_eColumnName,sql_condition , regexp, group, op, rstring)






#print(data)
#test = DB("192.168.15.63","root","softinc", "mj_db")

#test.reSearchInsertRow("t_1", "f1", "f2", "f3", None, "(\w{0,3})", "1", "s", "")
#test.reSearchInsertRow("t_1", "f1", "f2", "f4", None, "(assi)", "1", "r", "")
#test.reSearchInsertRow("t_1", "f1", "f3", "f5", None, "\w(\w)\w", "1", "s", "")