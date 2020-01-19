#!/usr/bin/python3
 
import pymysql

def init():
    global db,cursor
    # 打开数据库连接
    db = pymysql.connect("localhost","root","h4p3aYing","bookManage" )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

def select(table,content, judge):
    sql="select "+content+" from "+table+" where "+judge+" ;"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print("Error: unable to fetch data")

def insert(table,content):
    sql="insert into "+table+" values"+content+" ;"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("Error: unable to insert")
        
def delete(table,judge):
    sql="delete from "+table+" where"+judge+" ;"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("Error: unable to delete")
    
def update(table,content,judge):
    sql="update "+table+" set "+content+" where "+judge+" ;"
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("Error: unable to update")


def endit(): 
    # 关闭数据库连接
    db.close()
    

if __name__=="__main__":
    init()
    
