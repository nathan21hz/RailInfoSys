from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Ui_mainWindow import Ui_MainWindow
from Ui_loginWindow import Ui_Login
from Ui_registerWindow import Ui_Register
import sqlite3
import datetime
import icon_rc

basicconn = sqlite3.connect('./DB/BasicData.db')
basiccursor = basicconn.cursor()
trainconn = sqlite3.connect('./DB/Train.db')
traincursor = trainconn.cursor()
userlevel = 0
userid = 0
transcitylist =[]

#重写主界面类
class MyWindow(Ui_MainWindow):
    #刷新列表
    def refreshAll(self):
        page = self.tabWidget.currentIndex()
        #self.tabWidget.setTabEnabled(1, False)
        if(page == 0):
            self.list_user.clear()
            basiccursor.execute("select * from userinfo")
            users = basiccursor.fetchall()
            for u in users :
                self.list_user.addItem(str(u[0])+"|"+u[1])
        elif(page == 1):
            self.list_station_list.clear()
            basiccursor.execute("select * from station")
            stations = basiccursor.fetchall()
            for s in stations :
                self.list_station_list.addItem(str(s[0])+"|"+s[2])
        elif(page == 2):
            self.table_line.clearContents()
            self.combo_line_depart.clear()
            self.combo_line_arrive.clear()
            basiccursor.execute('select count(*) from raillink')
            self.table_line.setRowCount(basiccursor.fetchone()[0])
            basiccursor.execute('select * from raillink')
            lines = basiccursor.fetchall()
            for index, l in enumerate(lines):
                for i in range(1, 3):
                    self.table_line.setItem(index,i, QtWidgets.QTableWidgetItem(stationCodeToName(l[i])))
            for index, l in enumerate(lines):
                    self.table_line.setItem(index,0, QtWidgets.QTableWidgetItem(str(l[0])))
            for index, l in enumerate(lines):
                for i in range(3, 5):
                    self.table_line.setItem(index,i, QtWidgets.QTableWidgetItem(str(l[i])))
            
            basiccursor.execute('select * from station')
            stations = basiccursor.fetchall()
            for s in stations:
                self.combo_line_depart.addItem(s[2]+'|'+s[1])
                self.combo_line_arrive.addItem(s[2]+'|'+s[1])
        elif(page == 3):
            self.table_train.clearContents()
            self.combo_tain_depart.clear()
            basiccursor.execute('select count(*) from train')
            self.table_train.setRowCount(basiccursor.fetchone()[0])
            basiccursor.execute('select * from train')
            lines = basiccursor.fetchall()
            for index, l in enumerate(lines):
                for i in range(4, 6):
                    self.table_train.setItem(index,i, QtWidgets.QTableWidgetItem(stationCodeToName(l[i])))
            for index, l in enumerate(lines):
                for i in range(0, 4):
                    self.table_train.setItem(index,i, QtWidgets.QTableWidgetItem(str(l[i])))
            for index, l in enumerate(lines):
                for i in range(6, 11):
                    self.table_train.setItem(index,i, QtWidgets.QTableWidgetItem(str(l[i])))
            
            basiccursor.execute('select * from station')
            stations = basiccursor.fetchall()
            for s in stations:
                self.combo_tain_depart.addItem(s[2]+'|'+s[1])
        elif(page == 4):
            self.combo_ticket_depart.clear()
            self.combo_ticket_arrive.clear()
            basiccursor.execute('select * from station')
            stations = basiccursor.fetchall()
            for s in stations:
                self.combo_ticket_depart.addItem(s[2]+'|'+s[1])
                self.combo_ticket_arrive.addItem(s[2]+'|'+s[1])
            pass
        elif(page == 5):
            status = ("已出票", "已使用","已退票" )
            seattable = ("一等座", "二等座", )
            self.table_order.clearContents()
            basiccursor.execute('select * from "order" where uid=?', (userid, ))
            orders = basiccursor.fetchall()
            self.table_order.setRowCount(len(orders))
            for index, o in enumerate(orders):
                self.table_order.setItem(index,0, QtWidgets.QTableWidgetItem(str(o[0])))
            for index, o in enumerate(orders):
                self.table_order.setItem(index,1, QtWidgets.QTableWidgetItem(uidToName(o[1])))
            for index, o in enumerate(orders):
                self.table_order.setItem(index,2, QtWidgets.QTableWidgetItem(o[2]))
            for index, o in enumerate(orders):
                for i in range(3, 5):
                    self.table_order.setItem(index,i, QtWidgets.QTableWidgetItem(stationCodeToName(o[i])))
            for index, o in enumerate(orders):
                self.table_order.setItem(index,6, QtWidgets.QTableWidgetItem(str(o[6])))
            for index, o in enumerate(orders):
                self.table_order.setItem(index,5, QtWidgets.QTableWidgetItem(seattable[o[5]]))
            for index, o in enumerate(orders):
                self.table_order.setItem(index,7, QtWidgets.QTableWidgetItem(status[o[7]]))
        pass
        
    #用户列表选择动作
    def userListre(self):
        basiccursor.execute("select * from userinfo where uid = "+self.list_user.currentItem().text().split("|")[0])
        user = basiccursor.fetchone()
        self.lineedit_user_uid.setText(str(user[0]))
        self.lineedit_user_name.setText(user[1])
        self.lineedit_user_password.setText(user[2])
        self.spin_user_level.setValue(user[4])
    
    #用户信息编辑
    def userEdit(self):
        if(self.lineedit_user_uid.text()):
            basiccursor.execute('update userinfo set username=?,password=?,level=? where uid=?', (self.lineedit_user_name.text(), self.lineedit_user_password.text(),self.spin_user_level.value() ,self.lineedit_user_uid.text()))
            basicconn.commit()
            self.refreshAll()
        else:
            QMessageBox.information(MainWindow,"提示", "请先选择要修改的用户",QMessageBox.Yes)
    
    #删除用户
    def userDel(self):
        if(self.lineedit_user_uid.text()):
            basiccursor.execute('select count(*) from "order" where uid=?', (self.lineedit_user_uid.text(), ))
            useruse = basiccursor.fetchone()[0]
            if(useruse>0):
                QMessageBox.information(MainWindow,"提示", "该用户存在过购买记录，无法删除",QMessageBox.Yes)
                return
            else:
                basiccursor.execute('delete from userinfo where uid=?', (self.lineedit_user_uid.text(), ))
                basicconn.commit()
                self.refreshAll()
        else:
            QMessageBox.information(MainWindow,"提示", "请先选择要删除的用户",QMessageBox.Yes)
    
    #添加用户
    def userAdd(self):
        if(self.lineedit_user_name.text() and self.lineedit_user_password.text()):
            basiccursor.execute('select max(uid) from userinfo')
            maxid = basiccursor.fetchone()
            maxid = maxid[0] if maxid[0]!=None else 0
            basiccursor.execute('insert into userinfo values (?,?,?,NULL,?)', (maxid+1,self.lineedit_user_name.text(),self.lineedit_user_password.text(),self.spin_user_level.value()))
            basicconn.commit()
            self.refreshAll()
        else:
            QMessageBox.information(MainWindow,"提示", "用户名或密码不能为空",QMessageBox.Yes)

    #车站选择列表动作
    def stationListre(self):
        basiccursor.execute("select * from station where id = "+self.list_station_list.currentItem().text().split("|")[0])
        station = basiccursor.fetchone()
        self.lineedit_station_code.setText(station[1])
        self.lineedit_station_name.setText(station[2])
        self.spin_train_type.setValue(station[3])
   
    #编辑车站
    def stationEdit(self):
        if(checkUserlevel(0)):
            if(self.list_station_list.currentItem()):
                basiccursor.execute('update station set code=?,name=?,type=? where id=?', (self.lineedit_station_code.text(), self.lineedit_station_name.text(),self.spin_train_type.value() ,self.list_station_list.currentItem().text().split("|")[0]))
                basicconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "请先选择要编辑的车站",QMessageBox.Yes)
        
    #新增车站
    def stationAdd(self):
        if(checkUserlevel(0)):
            if(self.lineedit_station_code.text() and self.lineedit_station_name.text()):
                basiccursor.execute('select max(id) from station')
                maxid = basiccursor.fetchone()
                maxid = maxid[0] if maxid[0]!=None else 0
                basiccursor.execute('insert into station values (?,?,?,?)', (maxid+1,self.lineedit_station_code.text(),self.lineedit_station_name.text(),self.spin_train_type.value()))
                basicconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "车站代码或车站名不能为空",QMessageBox.Yes)
        
    #删除车站
    def stationDel(self):
        if(checkUserlevel(0)):
            if(self.list_station_list.currentItem()):
                id = self.list_station_list.currentItem().text().split("|")[0]
                basiccursor.execute('select code from station where id=?', (id, ))
                citycode = basiccursor.fetchone()[0]
                basiccursor.execute('select count(*) from raillink where "from"=? or "to"=?', (citycode ,citycode , ))
                cityuse = basiccursor.fetchone()[0]
                if(cityuse>0):
                    QMessageBox.information(MainWindow,"提示", "该车站被使用过，无法删除",QMessageBox.Yes)
                    self.refreshAll()
                    return
                else:
                    basiccursor.execute('delete from station where id=?', (id, ))
                    basicconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "请先选择要删除的车站",QMessageBox.Yes)
    
    #线路列表选择动作
    def lineTablere(self):
        id =  self.table_line.item(self.table_line.currentRow(), 0).text()
        basiccursor.execute('select * from raillink where id=?', (id, ))
        oneline = basiccursor.fetchone()
        #print(oneline)
        self.combo_line_depart.setCurrentText(stationCodeToName(oneline[1])+'|'+oneline[1])
        self.combo_line_arrive.setCurrentText(stationCodeToName(oneline[2])+'|'+oneline[2])
        self.spin_line_time.setValue(oneline[3])
        self.spin_line_cost.setValue(oneline[4])
    
    #编辑线路
    def lineEdit(self):
        if(checkUserlevel(0)):
            if(self.table_line.currentRow()!=-1):
                id =  self.table_line.item(self.table_line.currentRow(), 0).text()
                basiccursor.execute('update raillink set time=?,cost=? where id=?', (self.spin_line_time.value(), self.spin_line_cost.value(), id))
                basicconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "请先选择要编辑的线路",QMessageBox.Yes)
        
    #添加线路
    def lineAdd(self):
        if(checkUserlevel(0)):
            basiccursor.execute('select max(id) from raillink')
            maxid = basiccursor.fetchone()
            maxid = maxid[0] if maxid[0]!=None else 0
            basiccursor.execute('insert into raillink values (?,?,?,?,?)', (maxid+1,self.combo_line_depart.currentText().split("|")[1],self.combo_line_arrive.currentText().split("|")[1],self.spin_line_time.value(),self.spin_line_cost.value()))
            basicconn.commit()
            self.refreshAll()
 
    #删除线路 
    def lineDel(self):
        if(checkUserlevel(0)):
            if(self.table_line.currentRow()!=-1):
                id =  self.table_line.item(self.table_line.currentRow(), 0).text()
                basiccursor.execute('select id from train')
                trains = basiccursor.fetchall()
                for t in trains:
                    traintable = "train_"+str(t[0])
                    traincursor.execute('select count(*) from '+traintable+' where linkid=?', (id, ))
                    trainuse = traincursor.fetchone()[0]
                    if(trainuse>0):
                        QMessageBox.information(MainWindow,"提示", "该线路被使用，无法删除",QMessageBox.Yes)
                        return
                basiccursor.execute('delete from raillink where id=?', (id, ))
                basicconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "请先选择要删除的线路",QMessageBox.Yes)
        
    #车辆列表选择动作
    def trainTablere(self):
        self.list_train_line.clear()
        self.combo_tain_line.clear()
        id =  self.table_train.item(self.table_train.currentRow(), 0).text()
        traincursor.execute('select * from train_'+str(id))
        lines = traincursor.fetchall()
        for l in lines:
            basiccursor.execute('select * from raillink where id=?', (l[1], ))
            line = basiccursor.fetchone()
            lineText = stationCodeToName(line[1])+'-'+stationCodeToName(line[2])
            #print (lineText)
            self.list_train_line.addItem(str(l[0])+'|'+lineText+'|'+str(l[1]))
        #print(id)
        traincursor.execute('select linkid from train_'+str(id)+' order by id desc limit 0,1')
        lastlineid = traincursor.fetchone()
        if(lastlineid):
            basiccursor.execute('select "to" from raillink where id=?', (lastlineid[0], ))
            laststation = basiccursor.fetchone()[0]
        else:
            basiccursor.execute('select "from" from train where id=?', (id, ))
            laststation = basiccursor.fetchone()[0]
        #print(laststation)
        basiccursor.execute('select * from raillink where "from"=?', (laststation, ))
        nextlines = basiccursor.fetchall()
        for n in nextlines:
            #print(n)
            self.combo_tain_line.addItem(str(n[0])+'|'+stationCodeToName(n[1])+'-'+stationCodeToName(n[2]))
        pass
    
    #列车线路列表选择动作
    def trainListre(self):
        pass
    
    #添加车辆
    def trainAdd(self):
        if(checkUserlevel(0)):
            if(self.lineedit_train_code.text()):
                basiccursor.execute('select max(id) from train')
                maxid = basiccursor.fetchone()
                maxid = maxid[0] if maxid[0]!=None else 0
                time = self.time_train_depart.time().toString("hh:mm:ss.000")
                basiccursor.execute('insert into train values (?,?,?,NULL,?,"NOTSET",0,0,?,?,?)',
                    (maxid+1,self.lineedit_train_code.text() , time, self.combo_tain_depart.currentText().split("|")[1], self.spin_train_carriage.value(), self.spin_train_first.value(), self.spin_train_second.value()))
                traincursor.execute('create table train_'+str(maxid+1)+' ( \'id\' INT PRIMARY KEY NOT NULL, \'linkid\' INT NOT NULL ) WITHOUT ROWID')
                basicconn.commit()
                trainconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "车次号不能为空",QMessageBox.Yes)
            pass
    
    #删除车辆
    def trainDel(self):
        if(checkUserlevel(0)):
            if(self.table_train.currentRow()!=-1):
                self.list_train_line.clear()
                self.combo_tain_line.clear()
                id =  self.table_train.item(self.table_train.currentRow(), 0).text()
                traincursor.execute('drop table train_'+str(id))
                basiccursor.execute('delete from train where id=?', (id, ))
                basicconn.commit()
                trainconn.commit()
                self.refreshAll()
            else:
                QMessageBox.information(MainWindow,"提示", "请先选择要删除的车辆",QMessageBox.Yes)
            pass
        
    #添加车辆线路
    def trainLineadd(self):
        if(checkUserlevel(0) and self.table_train.currentRow()!=-1):
            id =  self.table_train.item(self.table_train.currentRow(), 0).text()
            tablename = 'train_'+str(id)
            traincursor.execute('select count(*) from '+tablename)
            lines = traincursor.fetchone()[0]
            traincursor.execute(('insert into '+tablename+' values(?,?)'), (lines+1, self.combo_tain_line.currentText().split('|')[0]))
            trainconn.commit()
            self.trainTablere()
            #print (lines)
            pass
    
    #删除车辆线路
    def trainLinedel(self):
        if(checkUserlevel(0) and self.table_train.currentRow()!=-1):
            trainid =  self.table_train.item(self.table_train.currentRow(), 0).text()
            if(self.list_train_line.currentItem()):
                lineid = self.list_train_line.currentItem().text().split('|')[0]
                tablename = 'train_'+str(trainid)
                traincursor.execute('select count(*) from '+tablename)
                lines = traincursor.fetchone()[0]
                for i in range(int(lineid), lines+1):
                    traincursor.execute(('delete from '+tablename+' where id=?'), (i, ))
                trainconn.commit()
                self.trainTablere()
            else:
                QMessageBox.information(MainWindow,"提示", "请先选择要删除的线路",QMessageBox.Yes)
     
    #车辆数据同步
    def trainLinesave(self):
        if(checkUserlevel(0) and self.table_train.currentRow()!=-1):
            during = 0
            cost = 0
            trainid =  self.table_train.item(self.table_train.currentRow(), 0).text()
            tablename = 'train_'+str(trainid)
            traincursor.execute('select linkid from '+tablename+' order by id desc limit 0,1')
            lastlineid = traincursor.fetchone()
            if(lastlineid):
                basiccursor.execute('select "to" from raillink where id=?', (lastlineid[0], ))
                laststation = basiccursor.fetchone()[0]
            else:
                laststation = "NOTSET"
            #print(laststation)
            traincursor.execute('select * from '+tablename)
            lines = traincursor.fetchall()
            for l in lines:
                basiccursor.execute('select * from raillink where id=?', (l[1], ))
                oneline = basiccursor.fetchone()
                during = during + oneline[3]
                cost = cost +oneline[4]
            links = len(lines)
            #print(laststation, links, during, cost)
            basiccursor.execute('select "departtime" from train where id=?', (trainid, ))
            departtime = basiccursor.fetchone()[0]
            arrivetime = datetime.datetime.strptime(departtime, '%H:%M:%S.000')
            arrivetime = arrivetime+datetime.timedelta(minutes=during)
            arivetimetext = arrivetime.strftime('%H:%M:%S.000')
            #print(arivetimetext, laststation, links, cost)
            basiccursor.execute('update train set "arrivetime"=?,"to"=?,"links"=?,"totalcost"=? where id=?', (arivetimetext,laststation ,links ,cost, trainid))
            basicconn.commit()
            self.refreshAll()
            pass
    
    #车票查询
    def ticketQuery(self):
        global transcitylist
        transcitylist = []
        self.table_ticket.clearContents()
        self.table_ticket.setRowCount(0)
        if(self.checkBox.checkState()==0):
            trainlist = oneWayQuery(self.combo_ticket_depart.currentText().split("|")[1], self.combo_ticket_arrive.currentText().split("|")[1])
            #print(trainlist)
            lines = len(trainlist)
            self.table_ticket.setRowCount(lines)
            forquerylist = ""
            for tl in trainlist:
                forquerylist = forquerylist + str(tl)+","
            forquerylist = forquerylist[0:-1]
            basiccursor.execute('select "code","departtime","totalcost","from","to","id" from train where id in ('+forquerylist+')')
            traintable = basiccursor.fetchall()
            for index, tt in enumerate(traintable):
                for i in range(3, 5):
                    self.table_ticket.setItem(index,i, QtWidgets.QTableWidgetItem(stationCodeToName(tt[i])))
            for index, tt in enumerate(traintable):
                for i in range(0, 3):
                    self.table_ticket.setItem(index,i, QtWidgets.QTableWidgetItem(str(tt[i])))
            for l in range(lines):
                temp = "否" if  ((self.table_ticket.item(l, 3).text() == self.combo_ticket_depart.currentText().split("|")[0]) and (self.table_ticket.item(l, 4).text() == self.combo_ticket_arrive.currentText().split("|")[0])) else "是"
                self.table_ticket.setItem(l,7, QtWidgets.QTableWidgetItem(temp))
            for index, tt in enumerate(traintable):
                temp = partTimecost(tt[5],self.combo_ticket_depart.currentText().split("|")[1], self.combo_ticket_arrive.currentText().split("|")[1])
                self.table_ticket.setItem(index,5, QtWidgets.QTableWidgetItem(str(temp["cost"])))
                self.table_ticket.setItem(index,6, QtWidgets.QTableWidgetItem(str(temp["during"])))
        else:
            transfers = transferTicketQuery(self.combo_ticket_depart.currentText().split("|")[1],self.combo_ticket_arrive.currentText().split("|")[1])
            plancount = len(transfers)
            self.table_ticket.setRowCount(plancount*3)
            for index, t in enumerate(transfers):
                basiccursor.execute('select "code","departtime","totalcost","from","to" from train where id=?', (t["line1"], ))
                line1 = basiccursor.fetchone()
                temp1 = partTimecost(t["line1"], self.combo_ticket_depart.currentText().split("|")[1], t["transcity"])
                temp2 = partTimecost(t["line2"], t["transcity"], self.combo_ticket_arrive.currentText().split("|")[1])
                transcitylist.append(t["transcity"])
                
                for i in range(3, 5):
                    self.table_ticket.setItem(index*3+1,i, QtWidgets.QTableWidgetItem(stationCodeToName(line1[i])))
                for i in range(0, 3):
                    self.table_ticket.setItem(index*3+1,i, QtWidgets.QTableWidgetItem(str(line1[i])))
                self.table_ticket.setItem(index*3+1,5, QtWidgets.QTableWidgetItem(str(temp1["cost"])))
                self.table_ticket.setItem(index*3+1,6, QtWidgets.QTableWidgetItem(str(temp1["during"])))
                
                basiccursor.execute('select "code","departtime","totalcost","from","to" from train where id=?', (t["line2"], ))
                line2 = basiccursor.fetchone()
                for i in range(3, 5):
                    self.table_ticket.setItem(index*3+2,i, QtWidgets.QTableWidgetItem(stationCodeToName(line2[i])))
                for i in range(0, 3):
                    self.table_ticket.setItem(index*3+2,i, QtWidgets.QTableWidgetItem(str(line2[i])))
                self.table_ticket.setItem(index*3+2,5, QtWidgets.QTableWidgetItem(str(temp2["cost"])))
                self.table_ticket.setItem(index*3+2,6, QtWidgets.QTableWidgetItem(str(temp2["during"])))
                
                self.table_ticket.setSpan(index*3, 0, 1, 8)
                totalcost = temp1["cost"]+temp2["cost"]
                totalduring = temp1["during"]+temp2["during"]
                titleline = "方案"+str(index+1)+"    换乘站："+stationCodeToName(t["transcity"])+"    实际费用合计："+str(totalcost)+"元    总历时："+str(totalduring)+"分钟"
                self.table_ticket.setItem(index*3,0, QtWidgets.QTableWidgetItem(titleline))
    
    #订票
    def ticketOrder(self):
        global userid
        global transcitylist
        seattable={0:"一等座", 1:"二等座"}
        if(self.table_ticket.currentRow()!=-1):
            if(self.checkBox.checkState()==2 and self.table_ticket.currentRow()%3==0):
                return
            if(self.checkBox.checkState()==0):
                basiccursor.execute('select max(id) from "order"')
                maxid = basiccursor.fetchone()
                maxid = maxid[0] if maxid[0]!=None else 0
                traincode = self.table_ticket.item(self.table_ticket.currentRow(), 0).text()
                depart = self.combo_ticket_depart.currentText().split("|")[1]
                arrive = self.combo_ticket_arrive.currentText().split("|")[1]
                level = self.combo_ticket_level.currentIndex()
                cost = int(self.table_ticket.item(self.table_ticket.currentRow(), 5).text())*(2-level)
                
            elif(self.checkBox.checkState()==2 and self.table_ticket.currentRow()%3==1):
                basiccursor.execute('select max(id) from "order"')
                maxid = basiccursor.fetchone()
                maxid = maxid[0] if maxid[0]!=None else 0
                traincode = self.table_ticket.item(self.table_ticket.currentRow(), 0).text()
                depart = self.combo_ticket_depart.currentText().split("|")[1]
                arrive = transcitylist[int(self.table_ticket.currentRow()/3)]
                level = self.combo_ticket_level.currentIndex()
                cost = int(self.table_ticket.item(self.table_ticket.currentRow(), 5).text())*(2-level)
                
            elif(self.checkBox.checkState()==2 and self.table_ticket.currentRow()%3==2):
                basiccursor.execute('select max(id) from "order"')
                maxid = basiccursor.fetchone()
                maxid = maxid[0] if maxid[0]!=None else 0
                traincode = self.table_ticket.item(self.table_ticket.currentRow(), 0).text()
                depart = transcitylist[int(self.table_ticket.currentRow()/3)]
                arrive = self.combo_ticket_arrive.currentText().split("|")[1]
                level = self.combo_ticket_level.currentIndex()
                cost = int(self.table_ticket.item(self.table_ticket.currentRow(), 5).text())*(2-level)
            
            ans = QMessageBox.information(MainWindow,"提示", "请检查您的车票订单：\n订单号："+str(maxid+1)+"\n用户名："+uidToName(userid)+"\n车次号："+traincode+
                                                                         "\n从："+stationCodeToName(depart)+"\n到："+stationCodeToName(arrive)+"\n座位："+seattable[level]+"\n应付款："+str(cost)+" 元"
            ,QMessageBox.Yes|QMessageBox.No)
            if(ans == QMessageBox.Yes):
                basiccursor.execute('select firstclass,secondclass from train where code=?', (traincode, ))
                check = basiccursor.fetchone()
                if(level==0):
                    if(check[0]<=0):
                        QMessageBox.information(MainWindow,"提示", "余票不足",QMessageBox.Yes)
                        return
                elif(level==1):
                    if(check[1]<=0):
                        QMessageBox.information(MainWindow,"提示", "余票不足",QMessageBox.Yes)
                        return
                    
                basiccursor.execute('insert into "order" values(?,?,?,?,?,?,?,0)', (maxid+1, userid, traincode, depart, arrive, level, cost, ))
                if(level==0):
                    basiccursor.execute('update train set firstclass=firstclass-1 where code=?', (traincode, ))
                elif(level==1):
                    basiccursor.execute('update train set secondclass=secondclass-1 where code=?', (traincode, ))
                basicconn.commit()
                QMessageBox.information(MainWindow,"提示", "订票成功\n请前往“我的订单”页查看。",QMessageBox.Yes)
            else:
                QMessageBox.information(MainWindow,"提示", "订单取消",QMessageBox.Yes)
        pass
    
    #退票    
    def orderRefund(self):
        if(self.table_order.currentRow()!=-1):
            ans = QMessageBox.information(MainWindow,"提示", "您确认要退票吗？",QMessageBox.Yes|QMessageBox.No)
            if(ans == QMessageBox.Yes):
                orderid = self.table_order.item(self.table_order.currentRow(), 0).text()
                basiccursor.execute('select traincode,level,status from "order" where id=?', (orderid, ))
                delordertrain = basiccursor.fetchone()
                delcode = delordertrain[0]
                dellevel = delordertrain[1]
                if(delordertrain[2]==2):
                    QMessageBox.information(MainWindow,"提示", "当前状态无法退票",QMessageBox.Yes)
                    return
                
                if(dellevel==0):
                    basiccursor.execute('update train set firstclass=firstclass+1 where code=?', (delcode, ))
                elif(dellevel==1):
                    basiccursor.execute('update train set secondclass=secondclass+1 where code=?', (delcode, ))
                basiccursor.execute('update "order" set status=2 where id=?', (orderid, ))
                basicconn.commit()
                QMessageBox.information(MainWindow,"提示", "退票成功",QMessageBox.Yes)
                self.refreshAll()
                pass

#重写登陆窗口类            
class MyLoginDlg(Ui_Login):
    def Login(self):
        global userlevel
        global userid
        leveltable = {0:"管理员", 1:"工作人员", 2:"旅客"}
        name = self.lineedit_name.text()
        password = self.lineedit_password.text()
        basiccursor.execute('select uid,level,username from userinfo where username=? and password=?', (name, password))
        userinfo = basiccursor.fetchone()
        if(userinfo):
            MainWindow.show()
            LoginDialog.close()
            userlevel = userinfo[1]
            userid = userinfo[0]
            if(userlevel == 1):
                ui.tabWidget.setTabEnabled(0, False)
            elif(userlevel > 1):
                for i in range(0, 4):
                    ui.tabWidget.setTabEnabled(i, False)
            QMessageBox.information(MainWindow,"登陆成功", "欢迎，"+leveltable[userinfo[1]]+" "+userinfo[2],QMessageBox.Yes)
            ui.refreshAll()
        else:
            QMessageBox.information(MainWindow,"提示", "用户名或密码错误",QMessageBox.Yes)
        pass
    
    def Register(self):
        RegDialog.show()
        pass
        
    def Cancel(self):
        sys.exit(app.exec_())
        pass

#重写注册窗口类
class MyRegisterDlg(Ui_Register):
    def Submit(self):
        if((self.lineedit_name.text()!="") and (self.lineedit_password.text()!="")):
            name = self.lineedit_name.text()
            if(self.lineedit_password.text() == self.lineedit_pwconfirm.text()):
                password = self.lineedit_password.text()
            else:
                QMessageBox.information(MainWindow,"提示", "两次输入密码不一致",QMessageBox.Yes)
                return False
            basiccursor.execute('select * from userinfo where username=?', (name,))
            check = basiccursor.fetchone()
            if(not check):
                basiccursor.execute('select max(uid) from userinfo')
                maxid = basiccursor.fetchone()
                maxid = maxid[0] if maxid[0]!=None else 0
                basiccursor.execute('insert into userinfo values(?,?,?,null,?)', (maxid+1, name, password, 2))
                basicconn.commit()
                RegDialog.close()
                QMessageBox.information(MainWindow,"提示", "用户 "+name+" 注册成功",QMessageBox.Yes)
                return True
            else:
                QMessageBox.information(MainWindow,"提示", "用户名已被占用",QMessageBox.Yes)
                return False
        else:
            QMessageBox.information(MainWindow,"提示", "用户名或密码不能为空",QMessageBox.Yes)
            return False
        pass
        
    def Cancel(self):
        RegDialog.close()
        pass

#通过车站代码查询并返回车站名
def stationCodeToName(code):
    if(code == 'NOTSET'):
        return "暂未设置"
    else:
        basiccursor.execute('select name from station where code=?', (code, ))
        name = basiccursor.fetchone()
        return name[0]

#通过车站名查询并返回车站代码
def nameToStationCode(name):
    basiccursor.execute('select code from station where name=?', (name, ))
    code = basiccursor.fetchone()
    return code[0]
        
#通过uid返回用户名
def uidToName(uid):
    basiccursor.execute('select username from userinfo where uid=?', (uid, ))
    name = basiccursor.fetchone()
    return name[0]

#判断列车是否经过某城市 
#mode 1 :始发 mode 2:终到
def cityIntrain(citycode, trainid, mode):
    if(mode == 1):
        tablename = "train_"+str(trainid)
        traincursor.execute('select * from '+tablename)
        links = traincursor.fetchall()
        for l in links:
            basiccursor.execute('select * from raillink where id=?', (l[1], ))
            link = basiccursor.fetchone()
            if(link[1]==citycode):
                return {"status":True,"seq":l[0]}
            pass
        return {"status":False,"seq":None}
    elif(mode == 2):
        tablename = "train_"+str(trainid)
        traincursor.execute('select * from '+tablename)
        links = traincursor.fetchall()
        for l in links:
            basiccursor.execute('select * from raillink where id=?', (l[1], ))
            link = basiccursor.fetchone()
            if(link[2]==citycode):
                return {"status":True,"seq":l[0]}
            pass
        return {"status":False,"seq":None}
    pass
    
#返回经过某站的所有列车（返回字典 id : seq）
def trainThroughcity(citycode):
    traindict = dict()
    basiccursor.execute('select * from train')
    trains = basiccursor.fetchall()
    for t in trains:
        temp = cityIntrain(citycode, t[0],1 )
        if(temp["status"]):
            traindict[t[0]]=temp["seq"]
    #print(traindict)
    return traindict
    
#返回某列车后续所有站code（返回列表 code）
def cityFollow(trainid, seq):
    citylist = []
    tablename = "train_"+str(trainid)
    traincursor.execute('select * from '+tablename+' where id>=?', (seq, ))
    links = traincursor.fetchall()
    for l in links:
        basiccursor.execute('select "to" from raillink where id=?', (l[1], ))
        city = basiccursor.fetchone()[0]
        citylist.append(city)
    #print(citylist)
    return citylist
    pass

#单程搜索（返回列表）
def oneWayQuery(depart, arrive):
    basiccursor.execute('select id from train')
    trains = basiccursor.fetchall()
    trainlist = []
    for t in trains:
        trainid = t[0]
        temp1=cityIntrain(depart, trainid,1)
        if(temp1["status"]):
            temp2 = cityIntrain(arrive, trainid,2)
            if(temp2["status"]):
                if(temp1["seq"]<=temp2["seq"]):
                    trainlist.append(trainid)
    return trainlist
    
#联程搜索（返回列表 字典）
def transferTicketQuery(depart, arrive):
    transferlist = []
    firstlines = trainThroughcity(depart)
    for line1 in firstlines:
        for transcity in cityFollow(line1, firstlines[line1]):
            secondlines = trainThroughcity(transcity)
            for line2 in secondlines:
                dest = cityFollow(line2, secondlines[line2])
                if(arrive in dest):
                    transferlist.append({"line1":line1, "transcity":transcity, "line2":line2})
    return transferlist
    pass

#某列车两站间时间/费用（返回字典）
def partTimecost(trainid, depart, arrive):
    departtemp = cityIntrain(depart, trainid, 1)
    arrivetemp = cityIntrain(arrive, trainid, 2)
    during = 0
    cost = 0
    if(departtemp["status"] and arrivetemp["status"] and (departtemp["seq"]<=arrivetemp["seq"])):
        tablename = "train_"+str(trainid)
        traincursor.execute('select * from '+tablename+' where (id>=? and id<=?)', (departtemp["seq"], arrivetemp["seq"]))
        lines = traincursor.fetchall()
        for l in lines:
            basiccursor.execute('select * from raillink where id=?', (l[1], ))
            oneline = basiccursor.fetchone()
            during = during + oneline[3]
            cost = cost +oneline[4]
        pass
        #print({"status":True, "during":during, "cost":cost})
        return {"status":True, "during":during, "cost":cost}
    else:
        return {"status":False, "during":None, "cost":None}
    pass

#检查用户权限    
def checkUserlevel(requsetlevel):
    global userlevel
    if(userlevel<=requsetlevel):
        return True
    else:
        QMessageBox.information(MainWindow,"提示", "用户权限禁止",QMessageBox.Yes)
        return False

#初始化
def Initial():
    MainWindow.setWindowIcon(QtGui.QIcon(':icon.ico'))
    LoginDialog.setWindowIcon(QtGui.QIcon(':icon.ico'))
    RegDialog.setWindowIcon(QtGui.QIcon(':icon.ico'))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    LoginDialog = QtWidgets.QDialog()
    RegDialog = QtWidgets.QDialog()
    ui = MyWindow()
    logindialog = MyLoginDlg()
    regdialog = MyRegisterDlg()
    ui.setupUi(MainWindow)
    logindialog.setupUi(LoginDialog)
    regdialog.setupUi(RegDialog)
    Initial()
    LoginDialog.show()
    sys.exit(app.exec_())
