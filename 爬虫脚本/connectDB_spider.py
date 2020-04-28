import pymysql

def  connDB():                              #连接数据库  
    conn=pymysql.connect(host="160.19.212.99",user="kaifa",passwd="224n5p67CfIDy2E^");  
    cur=conn.cursor();  
    return (conn,cur); 

def exeUpdate(conn,cur,sql):                #更新或插入操作  
    sta=cur.execute(sql);  
    conn.commit();  
    return (sta);  
  
def exeDelete(conn,cur,IDs):                #删除操作  
    sta=0;  
    for eachID in IDs.split(' '):  
        sta+=cur.execute("");  
    conn.commit();  
    return (sta);  
          
def exeQuery(cur,sql):                      #查找操作  
    cur.execute(sql);  
    return (cur);  
      
def connClose(conn,cur):                    #关闭连接，释放资源  
    cur.close();  
    conn.close();  