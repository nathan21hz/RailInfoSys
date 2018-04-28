from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_mainWindow import Ui_MainWindow
import sqlite3
import datetime

basicconn = sqlite3.connect('./DB/BasicData.db')
basiccursor = basicconn.cursor()
trainconn = sqlite3.connect('./DB/Train.db')
traincursor = trainconn.cursor()
class mywindow(Ui_MainWindow):
    #刷新列表
    def refreshAll(self):
        page = self.tabWidget.currentIndex()
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
            pass
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
        basiccursor.execute('update userinfo set username=?,password=?,level=? where uid=?', (self.lineedit_user_name.text(), self.lineedit_user_password.text(),self.spin_user_level.value() ,self.lineedit_user_uid.text()))
        basicconn.commit()
        self.refreshAll()
    
    #删除用户
    def userDel(self):
        basiccursor.execute('delete from userinfo where uid=?', (self.lineedit_user_uid.text()))
        basicconn.commit()
        self.refreshAll()
    
    #添加用户
    def userAdd(self):
        basiccursor.execute('select uid from userinfo order by uid desc limit 0,1')
        lines = basiccursor.fetchone()[0]
        basiccursor.execute('insert into userinfo values (?,?,?,NULL,?)', (lines+1,self.lineedit_user_name.text(),self.lineedit_user_password.text(),self.spin_user_level.value()))
        basicconn.commit()
        self.refreshAll()

    #车站选择列表动作
    def stationListre(self):
        basiccursor.execute("select * from station where id = "+self.list_station_list.currentItem().text().split("|")[0])
        station = basiccursor.fetchone()
        self.lineedit_station_code.setText(station[1])
        self.lineedit_station_name.setText(station[2])
        self.spin_train_type.setValue(station[3])
   
    #编辑车站
    def stationEdit(self):
        basiccursor.execute('update station set code=?,name=?,type=? where id=?', (self.lineedit_station_code.text(), self.lineedit_station_name.text(),self.spin_train_type.value() ,self.list_station_list.currentItem().text().split("|")[0]))
        basicconn.commit()
        self.refreshAll()
    
    #新增车站
    def stationAdd(self):
        basiccursor.execute('select id from station order by id desc limit 0,1')
        lines = basiccursor.fetchone()[0]
        basiccursor.execute('insert into station values (?,?,?,?)', (lines+1,self.lineedit_station_code.text(),self.lineedit_station_name.text(),self.spin_train_type.value()))
        basicconn.commit()
        self.refreshAll()
        
    #删除车站
    def stationDel(self):
        basiccursor.execute('delete from station where id=?', (self.list_station_list.currentItem().text().split("|")[0], ))
        basicconn.commit()
        self.refreshAll()
    
    def lineTablere(self):
        id =  self.table_line.item(self.table_line.currentRow(), 0).text()
        basiccursor.execute('select * from raillink where id=?', (id, ))
        oneline = basiccursor.fetchone()
        #print(oneline)
        self.combo_line_depart.setCurrentText(stationCodeToName(oneline[1])+'|'+oneline[1])
        self.combo_line_arrive.setCurrentText(stationCodeToName(oneline[2])+'|'+oneline[2])
        self.spin_line_time.setValue(oneline[3])
        self.spin_line_cost.setValue(oneline[4])
    
    def lineEdit(self):
        id =  self.table_line.item(self.table_line.currentRow(), 0).text()
        basiccursor.execute('update raillink set time=?,cost=? where id=?', (self.spin_line_time.value(), self.spin_line_cost.value(), id))
        basicconn.commit()
        self.refreshAll()
        
    #添加线路
    def lineAdd(self):
        basiccursor.execute('select id from raillink order by id desc limit 0,1')
        lines = basiccursor.fetchone()[0]
        basiccursor.execute('insert into raillink values (?,?,?,?,?)', (lines+1,self.combo_line_depart.currentText().split("|")[1],self.combo_line_arrive.currentText().split("|")[1],self.spin_line_time.value(),self.spin_line_cost.value()))
        basicconn.commit()
        self.refreshAll()
 
    #删除线路 
    def lineDel(self):
        id =  self.table_line.item(self.table_line.currentRow(), 0).text()
        basiccursor.execute('delete from raillink where id=?', (id, ))
        basicconn.commit()
        self.refreshAll()
    
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
    
    #线路列表选择动作
    def trainListre(self):
        pass
    
    #添加车辆
    def trainAdd(self):
        basiccursor.execute('select id from train order by id desc limit 0,1')
        lines = basiccursor.fetchone()[0]
        time = self.time_train_depart.time().toString("hh:mm:ss.000")
        basiccursor.execute('insert into train values (?,?,?,NULL,?,"NOTSET",0,0,?,?,?)',
            (lines+1,self.lineedit_train_code.text() , time, self.combo_tain_depart.currentText().split("|")[1], self.spin_train_carriage.value(), self.spin_train_first.value(), self.spin_train_second.value()))
        traincursor.execute('create table train_'+str(lines+1)+' ( \'id\' INT PRIMARY KEY NOT NULL, \'linkid\' INT NOT NULL ) WITHOUT ROWID')
        #basicconn.commit()
        #trainconn.commit()
        self.refreshAll()
        pass
    
    #删除车辆
    def trainDel(self):
        self.list_train_line.clear()
        self.combo_tain_line.clear()
        id =  self.table_train.item(self.table_train.currentRow(), 0).text()
        traincursor.execute('drop table train_'+str(id))
        basiccursor.execute('delete from train where id=?', (id, ))
        basicconn.commit()
        trainconn.commit()
        self.refreshAll()
        pass
    
    #添加车辆线路
    def trainLineadd(self):
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
        trainid =  self.table_train.item(self.table_train.currentRow(), 0).text()
        lineid = self.list_train_line.currentItem().text().split('|')[0]
        tablename = 'train_'+str(trainid)
        traincursor.execute('select count(*) from '+tablename)
        lines = traincursor.fetchone()[0]
        for i in range(int(lineid), lines+1):
            traincursor.execute(('delete from '+tablename+' where id=?'), (i, ))
        trainconn.commit()
        self.trainTablere()
     
    #车辆数据同步
    def trainLinesave(self):
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
        print(laststation)
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

def stationCodeToName(code):
    if(code == 'NOTSET'):
        return "暂未设置"
    else:
        basiccursor.execute('select name from station where code=?', (code, ))
        name = basiccursor.fetchone()
        return name[0]

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mywindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.refreshAll()
    sys.exit(app.exec_())

