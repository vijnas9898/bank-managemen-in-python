from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import StringProperty,ObjectProperty,NumericProperty
import mysql.connector

db=mysql.connector.connect(host="localhost",user="root",password="toor",database="bnkmgmt")
cur=db.cursor()
Builder.load_file('F:/bank management/screens.kv')

class LoginScreen(Screen):
        def verify(self):
                z=False
                cur.execute("select * from employee")
                f=cur.fetchall()
                for rows in f:
                        if self.ids["uname"].text==rows[0] and self.ids["passw"].text==rows[10] and self.ids["bid"].text==rows[8]:
                                z=True
                                self.manager.current='menu'
                                break
                        if self.ids["uname"].text=="admin" and self.ids["passw"].text=="admin":
                                z=True
                                self.manager.current="adscr"
                                break
                if z==False:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Username or Password",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
        pass

class MenuScreen(Screen):
        def trans(self):
                box = FloatLayout()
                box.add_widget(Label(text="Transactions",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                btn1 = Button(text="Deposit",size_hint=(1/4,1/5),pos_hint={'center_x':0.2,'center_y':0.2})
                box.add_widget(btn1)
                btn2=Button(text="Withdraw",size_hint=(1/4,1/5),pos_hint={'center_x':0.8,'center_y':0.2})
                box.add_widget(btn2)
                btn3=Button(text="Details",size_hint=(1/4,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                box.add_widget(btn3)
                popup =Popup(title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                btn1.bind(on_release=self.deps,on_press=popup.dismiss)
                btn2.bind(on_release=self.withs,on_press=popup.dismiss)
                btn3.bind(on_release=self.details,on_press=popup.dismiss)
                popup.open()
        def deps(self,instance):
                self.manager.current='dep'
        def withs(self,instance):
                self.manager.current='with'
        def details(self,instance):
                self.manager.current='det'
        def loans(self):
                box = FloatLayout()
                box.add_widget(Label(text="Loans",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                btn1 = Button(text="New Loan",size_hint=(1/4,1/5),pos_hint={'center_x':0.2,'center_y':0.2})
                box.add_widget(btn1)
                btn2=Button(text="Details",size_hint=(1/4,1/5),pos_hint={'center_x':0.8,'center_y':0.2})
                box.add_widget(btn2)
                popup =Popup(title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                btn1.bind(on_release=self.nl,on_press=popup.dismiss)
                btn2.bind(on_release=self.status,on_press=popup.dismiss)
                popup.open()
        def nl(self,instance):
                        self.manager.current='nl'
        def status(self,instance):
                        self.manager.current='lstat'
        pass

class NewAccount(Screen):
        def new(self):
                brid=self.ids["brid"].text
                sex='m'
                acno=self.ids["acno"].text
                nm=self.ids["nm"].text
                addr=self.ids["addr"].text
                age=self.ids["age"].text
                acctype=self.ids["acctype"].text
                pcn=self.ids["pcn"].text
                uid=self.ids["uid"].text
                dob=self.ids["dob"].text
                email=self.ids["email"].text
                ph=self.ids["ph"].text
                occ=self.ids["occ"].text
                cur.execute("insert into customer(accountno,custname,age,gender,panno,uidno,email,phone,occupation,dob,address,branchid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[acno,nm,age,sex,pcn,uid,email,ph,occ,dob,addr,brid])
                cur.execute("select branchid,ifsccode from branch")
                f=cur.fetchall()
                for i in f:
                        if brid==i[0]:
                                cur.execute("insert into accounts(accountid,acctype,ifsccode)values(%s,%s,%s)",[acno,acctype,i[1]])
                db.commit()             
        pass

class ModifyAccount(Screen):
        acno=StringProperty()
        addr=StringProperty()
        ph=StringProperty()
        email=StringProperty()
        occ=StringProperty()
        def mod(self):
                acno=self.ids["acno"].text
                cur.execute("select * from customer")
                f=cur.fetchall()
                for i in f:
                        if acno==i[0]:
                                self.ids["addr"].text=addr=i[11]
                                self.ids["ph"].text=ph=i[7]
                                self.ids["em"].text=email=i[6]
                                self.ids["occ"].text=occ=i[8]
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Account No",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()                            
        def update(self):               
                cur.execute("update customer set address=%s,phone=%s,email=%s,occupation=%s where accountno=%s",[self.ids["addr"].text,self.ids["ph"].text,self.ids["em"].text,self.ids["occ"].text,self.ids["acno"].text])
                db.commit()
        pass

class DeleteAccount(Screen):
        def dele(self):
                q=self.ids["del"].text
                cur.execute("delete from customer where accountno=%s",[q])
                cur.execute("delete from accounts where accountid=%s",[q])
                db.commit()
        pass

class NewLoan(Screen):
        def sub(self):
                no=self.ids["no"].text
                ac=self.ids["ac"].text
                nm=self.ids["nm"].text
                amt=self.ids["amt"].text
                docs=self.ids["docs"].text
                ltype=self.ids["ltype"].text
                nom=self.ids["nom"].text
                pan=self.ids["pan"].text
                uid=self.ids["uid"].text
                occ=self.ids["occ"].text
                rate=self.ids["rate"].text
                dur=self.ids["dur"].text
                brid=self.ids["brid"].text
                bal=int(amt)+(int(amt)*(float(rate)/100))
                emi=int(bal)/int(dur)
                cur.execute("select * from branch")
                f=cur.fetchall()
                for i in f:
                        if brid==i[0]:
                                cur.execute("insert into borrower(loanid,accountid,borrowname,occupation,loantype,panno,uidno,nominee,docs,loanamt,branchid)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[no,ac,nm,occ,ltype,pan,uid,nom,docs,amt,brid])
                                cur.execute("insert into loans(loanno,accountid,loantype,interestrates,duration,balance,installments)values(%s,%s,%s,%s,%s,%s,%s)",[no,ac,ltype,rate,dur,bal,emi])
                                db.commit()
                                break
                else: 
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Branch ID",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
        pass

class LoanStatus(Screen):
        lnno=StringProperty()
        acno=StringProperty()
        n=StringProperty()
        ltype=StringProperty()
        bal=StringProperty()
        emi=StringProperty()
        dur=StringProperty()
        def disp(self):
                lnno=self.ids["lnno"].text
                cur.execute("select * from borrower")
                f=cur.fetchall()
                for i in f:
                        if lnno==i[0]:
                                self.acno=i[1]
                                self.n=i[2]
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Loan ID",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
                        
                cur.execute("select * from loans")
                s=cur.fetchall()
                for j in s:
                        if lnno==j[0]:
                                self.ltype=j[2]
                                self.bal=str(j[4])
                                self.emi=str(j[6])
                                self.dur=str(j[5])
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Loan ID",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()

        pass

class Details(Screen):
        acno=StringProperty()
        nm=StringProperty()
        age=StringProperty()
        ph=StringProperty()
        baddr=StringProperty()
        bal=StringProperty()
        atype=StringProperty()
        def disp(self):
                acno=self.ids["acid"].text
                cur.execute("select * from customer")
                f=cur.fetchall()
                for i in f:
                        if acno==i[0]:
                                self.nm=i[1]
                                self.age=i[2]
                                self.ph=i[7]
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Account No",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
                        
                cur.execute("select * from accounts")
                s=cur.fetchall()
                for j in s:
                        if acno==j[0]:
                                self.bal=str(j[1])
                                self.atype=j[2]
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Account No",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
                        
        def trlg(self):
                layout = GridLayout(cols=4, spacing=10, size_hint_y=None)
                layout.bind(minimum_height=layout.setter('height'))
                layout.add_widget(Label(text='   ',size_hint_y=None,height=40))
                layout.add_widget(Label(text='   ',size_hint_y=None,height=40))
                layout.add_widget(Label(text='   ',size_hint_y=None,height=40))
                btn1 = Button(text="Close",size_hint_x=(0.7))
                layout.add_widget(btn1)
                layout.add_widget(Label(text='Date',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Operation',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Amount',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Account',size_hint_y=None,height=40))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                cur.callproc('banklogs')
                a=cur.stored_results()
                for r in a:
                        f=r.fetchall()
                        for i in f:
                                for l in i:
                                        layout.add_widget(Label(text=str(l),size_hint_y=None,height=40))
                root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                root.add_widget(layout)
                popup =Popup(title='Logs',content=root,size_hint=(1,1), size=(400,400),auto_dismiss=True,separator_height=0,title_align="justify")
                btn1.bind(on_press=popup.dismiss)
                popup.open()
        pass

class AdminScreen(Screen):
        def addemp(self,instance):
                self.manager.current='ae'
        def delemp(self,instance):
                self.manager.current='de'
        def empldet(self):
                layout = GridLayout(cols=6, spacing=10, size_hint_y=None)
                layout.bind(minimum_height=layout.setter('height'))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                btn1 = Button(text="<-- Back",size_hint_x=(0.7))
                layout.add_widget(btn1)
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                btn2 = Button(text="Add",size_hint_x=(0.7))
                layout.add_widget(btn2)
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                btn3 = Button(text="Delete",size_hint_x=(0.7))
                layout.add_widget(btn3)
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                layout.add_widget(Label(text='ID',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Name',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Age',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Gender',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Address',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Dependents',size_hint_y=None,height=40))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                cur.execute("select empid,empname,age,gender,address,dependentsno from employee")
                f=cur.fetchall()
                for i in f:
                        for j in i:
                                layout.add_widget(Label(text=str(j),size_hint_y=None,height=40))
                root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                root.add_widget(layout)
                popup =Popup(title='',content=root,size_hint=(1,1), size=(400,400),auto_dismiss=True,separator_height=0,title_align="justify")
                btn1.bind(on_press=popup.dismiss)
                btn2.bind(on_press=self.addemp,on_release=popup.dismiss)
                btn3.bind(on_press=self.delemp,on_release=popup.dismiss)
                popup.open()
        def delloan(self,instance):
                self.manager.current='dln'
        def loandet(self):
                layout = GridLayout(cols=7, spacing=10, size_hint_y=None)
                layout.bind(minimum_height=layout.setter('height'))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=20))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                btn1 = Button(text="<-- Back",size_hint_x=(0.7))
                layout.add_widget(btn1)
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                btn2 = Button(text="Delete",size_hint_x=(0.7))
                layout.add_widget(btn2)
                layout.add_widget(Label(text=' ',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Loan ID',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Account No',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Loan Type',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Interest',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Balance',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Duration',size_hint_y=None,height=40))
                layout.add_widget(Label(text='Installments',size_hint_y=None,height=40))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                layout.add_widget(Label(text='______________________________',size_hint_y=None,height=20))
                cur.execute("select * from loans")
                f=cur.fetchall()
                for i in f:
                        for j in i:
                                layout.add_widget(Label(text=str(j),size_hint_y=None,height=40))
                root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
                root.add_widget(layout)
                popup =Popup(title='',content=root,size_hint=(1,1), size=(400,400),auto_dismiss=True,separator_height=0,title_align="justify")
                btn1.bind(on_press=popup.dismiss)
                btn2.bind(on_press=self.delloan,on_release=popup.dismiss)
                popup.open()
        pass

class Deposit(Screen):
        def depo(self):
                cur.execute("select * from accounts")
                f=cur.fetchall()
                acno=self.ids["acno"].text
                for i in f:
                        if acno==i[0]:
                                bala=int(self.ids["bala"].text)
                                bal=i[1]+bala
                                cur.execute("update accounts set balance=%s,amt=%s where accountid=%s",[bal,bala,acno])
                                db.commit()
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Account No",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
        pass

class Withdraw(Screen):
        def withd(self):
                cur.execute("select * from accounts")
                f=cur.fetchall()
                acno=self.ids["acno"].text
                for i in f:
                        if acno==i[0]:
                                bala=int(self.ids["bala"].text)
                                bal=i[1]-bala
                                cur.execute("update accounts set balance=%s,amt=%s where accountid=%s",[bal,bala,acno])
                                db.commit()
                                break
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Invalid Account No",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
        pass

class AddEmployee(Screen):
        def newemp(self):
                empid=self.ids["empid"].text
                sex='m'
                empname=self.ids["empname"].text
                address=self.ids["address"].text
                age=self.ids["age"].text
                salary=self.ids["salary"].text
                depno=self.ids["depno"].text
                uid=self.ids["uid"].text
                dob=self.ids["dob"].text
                bid=self.ids["bid"].text
                passw=self.ids["password"].text
                cpass=self.ids["cpass"].text
                if passw==cpass:
                        cur.execute("insert into employee(empid,empname,age,gender,address,salary,uidno,dependentsno,branchid,dob,password)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[empid,empname,age,sex,address,salary,uid,depno,bid,dob,passw])
                        db.commit()
                else:
                        box = FloatLayout()
                        box.add_widget(Label(text="Password Doesn't Match",pos_hint={'center_x':0.5,'center_y':0.8},font_size=20))
                        btn1 = Button(text="Close",size_hint=(1/3,1/5),pos_hint={'center_x':0.5,'center_y':0.2})
                        box.add_widget(btn1)
                        popup =Popup(title='Error!', title_size=(30), content=box,size_hint=(1/2,1/2), size=(400, 400),auto_dismiss=False)
                        btn1.bind(on_press=popup.dismiss)
                        popup.open()
        pass

class DeleteEmployee(Screen):
        def delm(self):
                q=self.ids["eid"].text
                cur.execute("delete from employee where empid=%s",[q])
                db.commit()
        pass

class DeleteLoan(Screen):
        def deln(self):
                g=self.ids["lnn"].text
                cur.execute("delete from borrower where loanid=%s",[g])
                cur.execute("delete from loans where loanno=%s",[g])
                db.commit()
        pass

sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(NewAccount(name='newacc'))
sm.add_widget(ModifyAccount(name='modacc'))
sm.add_widget(DeleteAccount(name='delacc'))
sm.add_widget(NewLoan(name='nl'))
sm.add_widget(Details(name='det'))
sm.add_widget(LoanStatus(name='lstat'))
sm.add_widget(AdminScreen(name='adscr'))
sm.add_widget(Deposit(name='dep'))
sm.add_widget(Withdraw(name='with'))
sm.add_widget(AddEmployee(name='ae'))
sm.add_widget(DeleteEmployee(name='de'))
sm.add_widget(DeleteEmployee(name='dln'))

class Banker(App):
        def build(self):
                return sm

Banker().run()

