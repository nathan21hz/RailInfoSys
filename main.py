from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Ui_mainWindow import Ui_MainWindow
from Ui_loginWindow import Ui_Login
from Ui_registerWindow import Ui_Register
import sqlite3
import datetime

basicconn = sqlite3.connect('./DB/BasicData.db')
basiccursor = basicconn.cursor()
trainconn = sqlite3.connect('./DB/Train.db')
traincursor = trainconn.cursor()
userlevel = 0

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
        basiccursor.execute('select max(uid) from userinfo')
        maxid = basiccursor.fetchone()
        maxid = maxid[0] if maxid[0]!=None else 0
        basiccursor.execute('insert into userinfo values (?,?,?,NULL,?)', (maxid+1,self.lineedit_user_name.text(),self.lineedit_user_password.text(),self.spin_user_level.value()))
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
        if(checkUserlevel(0)):
            basiccursor.execute('update station set code=?,name=?,type=? where id=?', (self.lineedit_station_code.text(), self.lineedit_station_name.text(),self.spin_train_type.value() ,self.list_station_list.currentItem().text().split("|")[0]))
            basicconn.commit()
            self.refreshAll()
        
    #新增车站
    def stationAdd(self):
        if(checkUserlevel(0)):
            basiccursor.execute('select max(id) from station')
            maxid = basiccursor.fetchone()
            maxid = maxid[0] if maxid[0]!=None else 0
            basiccursor.execute('insert into station values (?,?,?,?)', (maxid+1,self.lineedit_station_code.text(),self.lineedit_station_name.text(),self.spin_train_type.value()))
            basicconn.commit()
            self.refreshAll()
        
    #删除车站
    def stationDel(self):
        if(checkUserlevel(0)):
            basiccursor.execute('delete from station where id=?', (self.list_station_list.currentItem().text().split("|")[0], ))
            basicconn.commit()
            self.refreshAll()
    
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
            id =  self.table_line.item(self.table_line.currentRow(), 0).text()
            basiccursor.execute('update raillink set time=?,cost=? where id=?', (self.spin_line_time.value(), self.spin_line_cost.value(), id))
            basicconn.commit()
            self.refreshAll()
        
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
    
    #列车线路列表选择动作
    def trainListre(self):
        pass
    
    #添加车辆
    def trainAdd(self):
        if(checkUserlevel(0)):
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
            pass
    
    #删除车辆
    def trainDel(self):
        if(checkUserlevel(0)):
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
        if(checkUserlevel(0)):
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
        if(checkUserlevel(0)):
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
        if(checkUserlevel(0)):
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
    
    #车票查询
    def ticketQuery(self):
        basiccursor.execute('select id from train')
        trains = basiccursor.fetchall()
        self.table_ticket.clearContents()
        trainlist = []
        for t in trains:
            trainid = t[0]
            if(cityIntrain(self.combo_ticket_depart.currentText().split("|")[1], trainid,1)):
                if(cityIntrain(self.combo_ticket_arrive.currentText().split("|")[1], trainid,2)):
                    trainlist.append(trainid)
        #print(trainlist)
        lines = len(trainlist)
        self.table_ticket.setRowCount(lines)
        forquerylist = ""
        for tl in trainlist:
            forquerylist = forquerylist + str(tl)+","
        forquerylist = forquerylist[0:-1]
        basiccursor.execute('select "code","departtime","totalcost","from","to" from train where id in ('+forquerylist+')')
        traintable = basiccursor.fetchall()
        for index, tt in enumerate(traintable):
            for i in range(3, 5):
                self.table_ticket.setItem(index,i, QtWidgets.QTableWidgetItem(stationCodeToName(tt[i])))
        for index, tt in enumerate(traintable):
            for i in range(0, 3):
                self.table_ticket.setItem(index,i, QtWidgets.QTableWidgetItem(str(tt[i])))
        for l in range(lines):
            temp = "否" if  ((self.table_ticket.item(l, 3).text() == self.combo_ticket_depart.currentText().split("|")[0]) and (self.table_ticket.item(l, 4).text() == self.combo_ticket_arrive.currentText().split("|")[0])) else "是"
            self.table_ticket.setItem(l,5, QtWidgets.QTableWidgetItem(temp))

#重写登陆窗口类            
class MyLoginDlg(Ui_Login):
    def Login(self):
        global userlevel
        leveltable = {0:"管理员", 1:"工作人员", 2:"旅客"}
        name = self.lineedit_name.text()
        password = self.lineedit_password.text()
        basiccursor.execute('select uid,level,username from userinfo where username=? and password=?', (name, password))
        userinfo = basiccursor.fetchone()
        if(userinfo):
            MainWindow.show()
            LoginDialog.close()
            userlevel = userinfo[1]
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
                return True
            pass
        return False
    elif(mode == 2):
        tablename = "train_"+str(trainid)
        traincursor.execute('select * from '+tablename)
        links = traincursor.fetchall()
        for l in links:
            basiccursor.execute('select * from raillink where id=?', (l[1], ))
            link = basiccursor.fetchone()
            if(link[2]==citycode):
                return True
            pass
        return False
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
    MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
    LoginDialog.setWindowIcon(QtGui.QIcon('icon.ico'))
    RegDialog.setWindowIcon(QtGui.QIcon('icon.ico'))

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

