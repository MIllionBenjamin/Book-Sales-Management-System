#!/usr/bin/python3
 
from SQLTest import *
from openpyxl import Workbook
import easygui as g
import numpy as np
import sys

def purchase():
    results=select("book","*","1=1")
    #print(results)
    temp=[]
    for row in results:
        message=row[1]+':'+str(row[2])+' left.'
        temp.append(message)
    inventory=tuple(temp)#将数据表条目的部分信息转换为元组，便于choicebox使用
    option=g.choicebox(msg='Which one do you want to purchase?',title='',choices=inventory)
    num=temp.index(option)#获得选择的条目在数据表上的索引
    purchaseNum=100-results[num][2]#进货数量
    if(purchaseNum>0):#只有数量小于100时才进货
        quotes=select("Quote","*","Book_id='"+results[num][0]+"'")
        temp=('','',0x3f3f3f3f3f3f)
        for row in quotes:#找到最便宜的进货价
            if(row[2]<temp[2]):
                temp=row
        update("book","Quantity=100","Book_id='"+results[num][0]+"'")
        #print(temp)
        insert("Bookshop_Purchase_Log(Supplier_id,Book_id,Price,Amount)","("+temp[0]+","+temp[1]+","+str(temp[2])+","+str(purchaseNum)+")")
        g.msgbox(msg="Successful!!!",title="")
    else:
        g.msgbox(msg="It's full",title="Warning")
    
def returns():
    results=select("book","*","1=1")
    #print(results)
    temp=[]
    for row in results:
        message=row[1]
        temp.append(message)
    inventory=tuple(temp)#将数据表条目的部分信息转换为元组，便于choicebox使用
    option=g.buttonbox(msg='Which one do you want to return?',title='',choices=inventory)
    num=temp.index(option)#获得选择的条目在数据表上的索引
    addNum=g.enterbox(msg="How many do you want to return?",title="RETURN")
    update("book","Quantity="+"Quantity+"+str(addNum),"Book_id='"+results[num][0]+"'")
    insert("Customer_Return_Log(Book_name,Price,Amount)","('"+results[num][1]+"',"+str(results[num][3])+","+str(addNum)+")")

def statistics():
    results1=select("Bookshop_Sell_Log","*","1=1")#获得销售结果
    message={}
    for row in results1:
        if message.get(row[2])!=None:
            message[row[2]][0]+=row[4]
            message[row[2]][1]+=row[3]*row[4]
        else:
            message[row[2]]=[]
            message[row[2]].append(row[4])
            message[row[2]].append(row[3]*row[4])
            
    results2=select("Customer_Return_Log","*","1=1")#获得客户退货结果
    for row in results2:
        if message.get(row[2])!=None:
            message[row[2]][0]-=row[4]
            message[row[2]][1]-=row[3]*row[4]
        else:
            message[row[2]]=[]
            message[row[2]].append((-1)*row[4])
            message[row[2]].append((-1)*row[3]*row[4])
        
    temp1=[]#统计出书本的买卖情况
    temp2=list(message.keys())
    for eachOne in temp2:
        temp3=message[eachOne]
        temp3.insert(0,eachOne)
        temp1.append(temp3)
    #print(temp1)
    
    label=['BookName','Amount','Saleroom']#写入表格
    wb = Workbook()
    ws = wb.active#第一个表
    ws.append(label)
    for i in temp1:
        ws.append(i)
    wb.save("销售记录.xlsx")

def sales():
    results=select("book","*","1=1")
    #print(results)
    temp=[]
    for row in results:
        message=row[1]+':'+str(row[2])+' left.'
        temp.append(message)
    inventory=tuple(temp)#将数据表条目的部分信息转换为元组，便于choicebox使用
    option=g.choicebox(msg='These are the books left.',title='',choices=inventory)
    num=temp.index(option)#获得选择的条目在数据表上的索引
    saleNum=g.enterbox(msg="How many do you want to buy?",title="RETURN")
    #print(saleNum)
    if(int(saleNum)<=results[num][2]):
        update("book","Quantity="+"Quantity-"+saleNum,"Book_id='"+results[num][0]+"'")
        insert("Bookshop_Sell_Log(Book_name,Price,Amount)","('"+results[num][1]+"',"+str(results[num][3])+","+saleNum+")")
    else:
        g.msgbox(msg="Isn't enough.",title="Warning")

def functionsOption():
    while(1):
        option = g.buttonbox(msg='What do you want to do?', title='OPTION', choices=('Purchase', 'Returns', 'Statistics', 'Sales'), image=None)
        if option==None:
            sys.exit(0)
        else:
            if(option=='Purchase'):
                purchase()
            elif(option=='Returns'):
                returns()
            elif(option=='Statistics'):
                statistics()
            elif(option=='Sales'):
                sales()
    endit()

def main():
    init()
    if g.ccbox(msg='Book sales management system.', title='BOOK MANAGEMENT', choices=('START', 'CANCEL'), image=None):
        functionsOption()
    else:
        sys.exit(0)

if __name__=='__main__':
    main()



