import mysql.connector
import pickle
import os


def display_all_doctors():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        print('Doctors:')
        mycur.execute('select * from doctor')
        rs=mycur.fetchall()
        for r in rs:
            print(r)
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()

def search_based_on_department():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        dep=input("Enter required department to be displayed")
        print('*'*60)
        print('%6s'%'Number','%10s'%'Name','%10s'%'Age','%6s'%'Nationality','%5s'%'DOJ','%15s'%'Gender''%15s'%'Department')
        print('*'*60)
        a=mycur.execute("select * from doctor where ddep='{}'".format(dep))
        rs=mycur.fetchall()
        for r in rs:
            print('%6s'%r[0],'%15s'%r[1],'%6s'%r[2],'%10s'%r[3],'%15s'%r[4],'%3s'%r[5],'%15s'%r[6])
    except Exception as e:
        print(e)
    mycur.close()
    mycon.close()


def search_by_name():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        name=input("Enter doctor name to be shown")
        print('*'*100)
        print('%6s'%'Number','%10s'%'Name','%10s'%'Age','%6s'%'Nationality','%5s'%'DOJ','%15s'%'Gender''%15s'%'Department')
        print('*'*100)
        a=mycur.execute("select * from doctor where dname='{}'".format(name))
        rs=mycur.fetchall()
        for r in rs:
            print('%6s'%r[0],'%15s'%r[1],'%6s'%r[2],'%10s'%r[3],'%15s'%r[4],'%3s'%r[5],'%15s'%r[6])
    except Exception as e:
        print(e)
    mycur.close()
    mycon.close()

def insert_record():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        dno=int(input('Enter doctor ID to be inserted:'))
        dname=input('Enter name of doctor:')
        dage=int(input('Enter age of doctor:'))
        dnat=input('Enter nationality of doctor:')
        doj=input('Enter date of joining:')
        dgender=input('Enter gender')
        ddep=input('Enter dept name')
        mycur.execute("insert into doctor values({},'{}',{},'{}','{}','{}','{}')".format(dno,dname,dage,dnat,doj,dgender,ddep))
        mycon.commit()
    except Exception as e:
        print(e)
        
    mycur.close()
    mycon.close()
    f=open('doctor.dat','wb+')
    while True:
        
        t=[]
        x=[]
        for k in range(5):
            if k==0:
                print('Timings for Sunday')
            elif k==1:
                print('Timings for Monday')
            elif k==2:
                print('Timings for Tuesday')
            elif k==3:
                print('Timings for Wednesday')
            elif k==4:
                print('Timings for Thursday')
            y=[]
            a=[]
            for j in range(3):
                s=float(input('enter timings'))
                y.append(s)
                a.append(0)
            x.append(a)                
            t.append(y)
        rec=[dno,t,x]
        pickle.dump(rec,f)
        cont=input('do you want to continue adding?....Y/N')
        if cont.upper()=="N":
            break
    f.close()

def update_record():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        no=int(input('Enter ID to be updated:'))
        q='select * from doctor where dno={}'.format(no)
        mycur.execute(q)
        rs=mycur.fetchone()
        if rs==None:
            print("Doctor doesn't exist")
        else:
            print(rs)
            name=input('Enter name of doctor:')
            age=int(input('Enter age of doctor:'))
            nationality=input('Enter nationality of doctor:')
            doj=input('Enter date of joining:')
            gen=input('Enter gender')
            dept=input('Enter dept name')
            a="update doctor set dname='{}',dage={},dnat='{}',doj='{}',dgender='{}',ddep='{}' where dno={}".format(name,age,nationality,doj,gen,dept,no)
            mycur.execute(a)
            print(mycur.rowcount,'Records updated')
            mycon.commit()
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()      

def delete_record():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        no=int(input('Enter ID to be deleted:'))
        q='delete from doctor where dno={}'.format(no)
        mycur.execute(q)
        mycon.commit()
        print(mycur.rowcount,'Record deleted successfully')
        f=open('doctor.dat','rb')
        f1=open('doctor1.dat','ab')
        flag=0
        while True:
            try:
                rec=pickle.load(f)
                if rec[0]!=no:
                    pickle.dump(rec,f1)
                flag=1
            except EOFError:
                f.close()
                f1.close()
                if flag==0:
                    print('end')
                break
        os.remove('doctor.dat')
        os.rename('doctor1.dat','doctor.dat')
    except Exception as e:
        print(e)
        mycon.rollback()
        
    mycur.close()
    mycon.close()
    
def display_bin():
    f=open('doctor.dat','rb')
    s='*'
    print(s*150)
    print('%9s'%'Doctor ID','%60s'%'Timings','%60s'%'Appointments')
    print(s*150)
    while True:
        try:
            e_rec=pickle.load(f)
            print('%9s'%e_rec[0],'%60s'%e_rec[1],'%60s'%e_rec[2])
            
        except EOFError:
            print(s*60)
            print('The End')
            f.close()
            break
        
def book_appointment():
    found=0
    f=open('doctor.dat','rb')
    f1=open('doctor1.dat','ab')
    docid=int(input('enter id to be booked'))
    patid=int(input('enter patient id'))
    while True:
        
        try:
            rec=pickle.load(f)
            if docid==rec[0]:
                day=input('enter which day you want to book appointment')
                if day=='Sunday':
                    for i in range(3):
                        if rec[2][0][i]==0:
                            print(rec[1][0][i])
                    time=float(input('enter timing for appointment'))
                    q=rec[1][0].index(time)
                    rec[2][0][q]=patid
                elif day=='Monday':
                    for i in range(3):
                        if rec[2][1][i]==0:
                            print(rec[1][1][i])
                    time=float(input('enter timing for appointment'))
                    q=rec[1][1].index(time)
                    rec[2][1][q]=patid
                elif day=='Tuesday':
                    for i in range(3):
                        if rec[2][2][i]==0:
                            print(rec[1][2][i])
                    time=float(input('enter timing for appointment'))
                    q=rec[1][2].index(time)
                    rec[2][2][q]=patid
                elif day=='Wednesday':
                    for i in range(3):
                        if rec[2][3][i]==0:
                            print(rec[1][3][i])
                    time=float(input('enter timing for appointment'))
                    q=rec[1][3].index(time)
                    rec[2][3][q]=patid
                elif day=='Thursday':
                    for j in range(3):
                        if rec[2][4][j]==0:
                            print(rec[1][4][j])
                    time=float(input('enter timing for appointment'))
                    q=rec[1][4].index(time)
                    rec[2][4][q]=patid
            pickle.dump(rec,f1)
            found=1
            
        except EOFError:
            f.close()
            f1.close()
            if found==0:
                print('end')
            break
    
    os.remove('doctor.dat')
    os.rename('doctor1.dat','doctor.dat')
    
def del_appointment():
    found=0
    f=open('doctor.dat','rb')
    f1=open('doctor1.dat','ab')
    docid=int(input('enter doctor id whose appointment to be deleted'))
    patid=int(input('enter patient id'))
    while True:
        try:
            rec=pickle.load(f)
            if docid==rec[0]:
                day=input('enter which day you want to delete appointment')
                if day=='Sunday':
                    for i in range(3):
                        if rec[2][0][i]==patid:
                            print(rec[1][0][i])
                            ch=float(input('choose appointment timing to delete'))
                            q=rec[1][0].index(ch)
                            rec[2][0][q]=0
                elif day=='Monday':
                    for i in range(3):
                        if rec[2][1][i]==patid:
                            print(rec[1][1][i])
                            ch=float(input('choose appointment timing to delete'))
                            q=rec[1][1].index(ch)
                            rec[2][1][q]=0
                elif day=='Tuesday':
                    for i in range(3):
                        if rec[2][2][i]==patid:
                            print('Timings of appointment booked:',rec[1][2][i])
                            ch=float(input('choose appointment timing to delete'))
                            q=rec[1][2].index(ch)
                            rec[2][2][q]=0
                elif day=='Wednesday':
                    for i in range(3):
                        if rec[2][3][i]==patid:
                            print(rec[1][3][i])
                            ch=float(input('choose appointment timing to delete'))
                            q=rec[1][3].index(ch)
                            rec[2][3][q]=0
                elif day=='Thursday':
                    for j in range(3):
                        if rec[2][4][j]==patid:
                            print(rec[1][4][i])
                            ch=float(input('choose appointment timing to delete'))
                            q=rec[1][4].index(ch)
                            rec[2][4][q]=0
            pickle.dump(rec,f1)
            found=1
        except EOFError:
            f.close()
            f1.close()
            if found==0:
                print('end')
            break 
    os.remove('doctor.dat')
    os.rename('doctor1.dat','doctor.dat')
    
def refresh_week():
    flag=0
    f=open('doctor.dat','rb')
    f1=open('doctor1.dat','ab')
    while True:
        
        try:
            rec=pickle.load(f)
            for i in range(5):
                
                for j in range(3):
                    if rec[2][i][j]!=0:
                        
                        rec[2][i][j]=0
            pickle.dump(rec,f1)
            flag=1
        except EOFError:
            f.close()
            f1.close()
            if flag==0:
                print('done')
            break
    os.remove('doctor.dat')
    os.rename('doctor1.dat','doctor.dat')

#*******************************************************************************#

def sign_up_patient():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        pid=int(input('enter patient id'))
        mycur.execute("select * from patients where pid={}".format(pid))
        rs=mycur.fetchone()
        if rs==None:
            name=input('Enter name:')
            age=int(input('Enter age:'))
            dob=input('Enter date of birth:')
            a="insert into patients values({},'{}','{}',{})".format(pid,name,dob,age)
            mycur.execute(a)
            mycon.commit()
            print(mycur.rowcount,'Record inserted')
            
        else:
            print('already exists')
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()
           
def display_all_patients():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        mycur.execute('select * from patients')
        rs=mycur.fetchall()
        print('No of records=',mycur.rowcount)
        print("%3s"%"pid","%15s"%"pname","%15s"%"date of birth","%4s"%"age")
        for r in rs:
            print("%3s"%r[0],"%15s"%r[1],"%15s"%r[2],"%4s"%r[3]) 
    except Exception as e:
        print(e)
   
    mycur.close()
    mycon.close()
   
def update_patient_details():
    
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        no=int(input('Enter number to be updated:'))
        mycur.execute(("select * from patients where pid={}").format(no))
        rs=mycur.fetchone()
        if rs==None:
            print('patient dosent exist')
        else:
            print(rs)
            name=input('Enter name:')
            age=int(input('Enter age'))
            dob=input('Enter date of birth:')
            pno=int(input('Enter patient id:'))
            a="update patients set pname='{}',page={},pdob='{}'where pid={}".format(name,age,dob,pno)
            mycur.execute(a)
            print(mycur.rowcount,'Records updated')
            mycon.commit()
    except Exception as e:
        print(e)
    mycur.close
    mycon.commit()
   
        
    
def search_patient_by_ID():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        id=int(input("Enter patient ID to be shown"))
        print('*'*100)
        print("%3s"%"pid","%15s"%"pname","%15s"%"date of birth","%4s"%"age")
        print('*'*100)
        a=mycur.execute("select * from patients where pid='{}'".format(id))
        rs=mycur.fetchall()
        for r in rs:
            print("%3s"%r[0],"%15s"%r[1],"%15s"%r[2],"%4s"%r[3])
    except Exception as e:
        print(e)
    
    mycur.close()
    mycon.close()
    
def search_patient_by_name():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        name=input("Enter patient name to be shown")
        print('*'*100)
        print("%3s"%"pid","%15s"%"pname","%15s"%"date of birth","%4s"%"age")
        print('*'*100)
        a=mycur.execute("select * from patients where pname='{}'".format(name))
        rs=mycur.fetchall()
        for r in rs:
            print("%3s"%r[0],"%15s"%r[1],"%15s"%r[2],"%4s"%r[3])
    except Exception as e:
        print(e)
    mycur.close()
    mycon.close()
    
def search_patient_by_age():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        age=input("Enter patient age to be shown")
        print('*'*100)
        print("%3s"%"pid","%15s"%"pname","%15s"%"date of birth","%4s"%"page")
        print('*'*100)
        a=mycur.execute("select * from patients where page='{}'".format(age))
        rs=mycur.fetchall()
        for r in rs:
            print("%3s"%r[0],"%15s"%r[1],"%15s"%r[2],"%4s"%r[3])
    except Exception as e:
        print(e)
    mycur.close()
    mycon.close()
    
def search_patient_by_dob():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        date=input("Enter patient date of birth to be shown")
        print('*'*100)
        print("%3s"%"pid","%15s"%"pname","%15s"%"date of birth","%4s"%"age")
        print('*'*100)
        a=mycur.execute("select * from patients where pdob='{}'".format(date))
        rs=mycur.fetchall()
        for r in rs:
            print("%3s"%r[0],"%15s"%r[1],"%15s"%r[2],"%4s"%r[3])
    except Exception as e:
        print(e)
    mycur.close()
    mycon.close()    
    
def search_patient_menu():
    print('1:Search by patient id')
    print('2.Search by patient name')
    print('3.search by patient age')
    print('4.Search by patient date of birth')
    print('5.Back to Menu')
    ch1=int(input('Enter choice:'))
    if ch1==1:
        search_patient_by_ID()
    elif ch1==2:
        search_patient_by_name()
    elif ch1==3:
        search_patient_by_age()
    elif ch1==4:
        search_patient_by_dob()
    elif ch1==5:
        return               
    
def delete_patient_record():
    try:
        mycon=mysql.connector.connect(host='localhost',user='root',passwd='ishani',database='adis')
        mycur=mycon.cursor()
        no=int(input('Enter number to be deleted:'))
        q='delete from patients where pid={}'.format(no)
        mycur.execute(q)
        mycon.commit()
        print(mycur.rowcount,'Records deleted successfully')
    except Exception as e:
        print(e)
        mycon.rollback()
       
    mycur.close()
    mycon.close()
    
def admin():
    print('WELCOME TO ADMIN OF KSI HOSPITAL')
    ps=input('enter admin password')
    if ps.upper()=='ADIS':
        while True:
            print('1. Display all doctors')
            print('2. Search doctor based on department')
            print('3. Search doctor based on name')
            print('4. Insert doctor record')
            print('5. Update doctor record')
            print('6. Delete doctor record')
            print('7. Refresh at end of week')
            print('8. Display patient information')
            print('9. Update patient details')
            print('10. Search patient menu')
            print('11. Delete patient record')
            print('12. Exit')
            ch=int(input('enter a choice:'))
            if ch==1:
                display_all_doctors()
            elif ch==2:
                search_based_on_department()
            elif ch==3:
                search_by_name()
            elif ch==4:
                insert_record()
            elif ch==5:
                update_record()
            elif ch==6:
                delete_record()
            elif ch==7:
                refresh_week()
            elif ch==8:
                display_all_patients()
            elif ch==9:
                update_patient_details()
            elif ch==10:
                search_patient_menu()
            elif ch==11:
                delete_patient_record()
            elif ch==12:
                break 
            else:
                print("Invalid choice entered")
    else:
        print('wrong password entered')
        
def user():
    print('WELCOME TO KSI HOSPITAL')
    print('*'*25)
    print('USER : Patient')
    while True:
        print('1. Display all doctors')
        print('2. Patient sign up')
        print('3. Display all appointments')
        print('4. Book appointment')
        print('5. Delete appointment')
        print('6. Exit')
        ch=int(input('enter choice'))
        if ch==1:
            display_all_doctors()
        elif ch==2:
            sign_up_patient()
        elif ch==3:
            display_bin()
        elif ch==4:
            book_appointment()
        elif ch==5:
            del_appointment()
        elif ch==6:
            break
        else:
            print('INVALID CHOICE')
                
        
        
s='*'
print(s*50)
print('WELCOME TO THE KSI HOSPITAL')
print(s*50)
while True:
    print('1. Admin')
    print('2. Patient')
    print('3. Exit')
    ch=int(input('choose user-1,2 or 3'))
    if ch==1:
        admin()
    elif ch==2:
        user()
    elif ch==3:
        break
    else:
        print("Invalid choice entered")
    
'''Output:
**************************************************
WELCOME TO THE KSI HOSPITAL
**************************************************
1. Admin
2. Patient
3. Exit
choose user-1,2 or 31
WELCOME TO ADMIN OF KSI HOSPITAL
enter admin passwordADIS
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:1
Doctors:
(111, 'Ravi Kumar', 45, 'Indian', datetime.date(2003, 5, 15), 'M', 'Cardiology')
(222, 'Maryam Mansour', 36, 'Emirati', datetime.date(2004, 5, 25), 'F', 'Gynaecology')
(333, 'Luca Patrizio', 41, 'Italian', datetime.date(2013, 6, 30), 'M', 'Paediatrics')
(444, 'William Smith', 52, 'Canadian', datetime.date(2001, 12, 20), 'M', 'Paediatrics')
(555, 'Rasha Fathima', 33, 'Indian', datetime.date(2016, 1, 13), 'F', 'Cardiology')
(666, 'Sharma Jain', 46, 'Indian', datetime.date(2005, 10, 16), 'M', 'Orthopedics')
(777, 'Immanuel Abeo', 35, 'Nigerian', datetime.date(2012, 5, 28), 'M', 'Orthodontics')
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:2
Enter required department to be displayedCardiology
************************************************************
Number       Name        Age Nationality   DOJ      Gender     Department
************************************************************
   111      Ravi Kumar     45     Indian      2003-05-15   M      Cardiology
   555   Rasha Fathima     33     Indian      2016-01-13   F      Cardiology
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:3
Enter doctor name to be shownMaryam Mansour
****************************************************************************************************
Number       Name        Age Nationality   DOJ      Gender     Department
****************************************************************************************************
   222  Maryam Mansour     36    Emirati      2004-05-25   F     Gynaecology
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:4
Enter doctor ID to be inserted:888
Enter name of doctor:Khush Das
Enter age of doctor:42
Enter nationality of doctor:Indian
Enter date of joining:2000-03-05
Enter genderM
Enter dept nameENT
Timings for Sunday
enter timings8.15
enter timings8.45
enter timings9.20
Timings for Monday
enter timings8.25
enter timings9.00
enter timings9.40
Timings for Tuesday
enter timings12.40
enter timings13.20
enter timings14.10
Timings for Wednesday
enter timings10.30
enter timings12.00
enter timings12.50
Timings for Thursday
enter timings13.20
enter timings13.50
enter timings14.20
do you want to continue adding?....Y/NN
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:1
Doctors:
(111, 'Ravi Kumar', 45, 'Indian', datetime.date(2003, 5, 15), 'M', 'Cardiology')
(222, 'Maryam Mansour', 36, 'Emirati', datetime.date(2004, 5, 25), 'F', 'Gynaecology')
(333, 'Luca Patrizio', 41, 'Italian', datetime.date(2013, 6, 30), 'M', 'Paediatrics')
(444, 'William Smith', 52, 'Canadian', datetime.date(2001, 12, 20), 'M', 'Paediatrics')
(555, 'Rasha Fathima', 33, 'Indian', datetime.date(2016, 1, 13), 'F', 'Cardiology')
(666, 'Sharma Jain', 46, 'Indian', datetime.date(2005, 10, 16), 'M', 'Orthopedics')
(777, 'Immanuel Abeo', 35, 'Nigerian', datetime.date(2012, 5, 28), 'M', 'Orthodontics')
(888, 'Khush Das', 42, 'Indian', datetime.date(2000, 3, 5), 'M', 'ENT')
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:5
Enter ID to be updated:888
(888, 'Khush Das', 42, 'Indian', datetime.date(2000, 3, 5), 'M', 'ENT')
Enter name of doctor:Khush Pradeep
Enter age of doctor:42
Enter nationality of doctor:Indian
Enter date of joining:2000-03-05
Enter genderM
Enter dept nameENT
1 Records updated
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:1
Doctors:
(111, 'Ravi Kumar', 45, 'Indian', datetime.date(2003, 5, 15), 'M', 'Cardiology')
(222, 'Maryam Mansour', 36, 'Emirati', datetime.date(2004, 5, 25), 'F', 'Gynaecology')
(333, 'Luca Patrizio', 41, 'Italian', datetime.date(2013, 6, 30), 'M', 'Paediatrics')
(444, 'William Smith', 52, 'Canadian', datetime.date(2001, 12, 20), 'M', 'Paediatrics')
(555, 'Rasha Fathima', 33, 'Indian', datetime.date(2016, 1, 13), 'F', 'Cardiology')
(666, 'Sharma Jain', 46, 'Indian', datetime.date(2005, 10, 16), 'M', 'Orthopedics')
(777, 'Immanuel Abeo', 35, 'Nigerian', datetime.date(2012, 5, 28), 'M', 'Orthodontics')
(888, 'Khush Pradeep', 42, 'Indian', datetime.date(2000, 3, 5), 'M', 'ENT')
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:6
Enter ID to be deleted:888
1 Record deleted successfully
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:1
Doctors:
(111, 'Ravi Kumar', 45, 'Indian', datetime.date(2003, 5, 15), 'M', 'Cardiology')
(222, 'Maryam Mansour', 36, 'Emirati', datetime.date(2004, 5, 25), 'F', 'Gynaecology')
(333, 'Luca Patrizio', 41, 'Italian', datetime.date(2013, 6, 30), 'M', 'Paediatrics')
(444, 'William Smith', 52, 'Canadian', datetime.date(2001, 12, 20), 'M', 'Paediatrics')
(555, 'Rasha Fathima', 33, 'Indian', datetime.date(2016, 1, 13), 'F', 'Cardiology')
(666, 'Sharma Jain', 46, 'Indian', datetime.date(2005, 10, 16), 'M', 'Orthopedics')
(777, 'Immanuel Abeo', 35, 'Nigerian', datetime.date(2012, 5, 28), 'M', 'Orthodontics')
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:8
No of records= 5
pid           pname   date of birth  age
  1             sia      2003-08-19   16
  2      ramanathan      1965-12-30   55
  3           aryan      2014-12-04    6
  4           kiara      1995-08-04   25
  5            john      1957-08-14   63
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit

enter a choice:10
1:Search by patient id
2.Search by patient name
3.search by patient age
4.Search by patient date of birth
5.Back to Menu
Enter choice:1
Enter patient ID to be shown5
****************************************************************************************************
pid           pname   date of birth  age
****************************************************************************************************
  5            john      1957-08-14   63
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:10
1:Search by patient id
2.Search by patient name
3.search by patient age
4.Search by patient date of birth
5.Back to Menu
Enter choice:2
Enter patient name to be shownsia
****************************************************************************************************
pid           pname   date of birth  age
****************************************************************************************************
  1             sia      2003-08-19   16
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:10
1:Search by patient id
2.Search by patient name
3.search by patient age
4.Search by patient date of birth
5.Back to Menu
Enter choice:3
Enter patient age to be shown6
****************************************************************************************************
pid           pname   date of birth page
****************************************************************************************************
  3           aryan      2014-12-04    6
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:10
1:Search by patient id
2.Search by patient name
3.search by patient age
4.Search by patient date of birth
5.Back to Menu
Enter choice:4
Enter patient date of birth to be shown2003-08-19
****************************************************************************************************
pid           pname   date of birth  age
****************************************************************************************************
  1             sia      2003-08-19   16
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit

enter a choice:11
Enter number to be deleted:4
1 Records deleted successfully
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit
enter a choice:8
No of records= 4
pid           pname   date of birth  age
  1             sia      2003-08-19   16
  2      ramanathan      1965-12-30   55
  3           aryan      2014-12-04    6
  5            john      1957-08-14   63
1. Display all doctors
2. Search doctor based on department
3. Search doctor based on name
4. Insert doctor record
5. Update doctor record
6. Delete doctor record
7. Refresh at end of week
8. Display patient information
9. Update patient details
10. Search patient menu
11. Delete patient record
12. Exit


enter a choice:12
1. Admin
2. Patient
3. Exit
choose user-1,2 or 32
WELCOME TO KSI HOSPITAL
*************************
USER : Patient
1. Display all doctors
2. Patient sign up
3. Display all appointments
4. Book appointment
5. Delete appointment
6. Exit
enter choice1
Doctors:
(111, 'Ravi Kumar', 45, 'Indian', datetime.date(2003, 5, 15), 'M', 'Cardiology')
(222, 'Maryam Mansour', 36, 'Emirati', datetime.date(2004, 5, 25), 'F', 'Gynaecology')
(333, 'Luca Patrizio', 41, 'Italian', datetime.date(2013, 6, 30), 'M', 'Paediatrics')
(444, 'William Smith', 52, 'Canadian', datetime.date(2001, 12, 20), 'M', 'Paediatrics')
(555, 'Rasha Fathima', 33, 'Indian', datetime.date(2016, 1, 13), 'F', 'Cardiology')
(666, 'Sharma Jain', 46, 'Indian', datetime.date(2005, 10, 16), 'M', 'Orthopedics')
(777, 'Immanuel Abeo', 35, 'Nigerian', datetime.date(2012, 5, 28), 'M', 'Orthodontics')
1. Display all doctors
2. Patient sign up
3. Display all appointments
4. Book appointment
5. Delete appointment
6. Exit

enter choice4
enter id to be booked222
enter patient id1
enter which day you want to book appointmentSunday
20.15
20.45
21.25
enter timing for appointment20.45

1. Display all doctors
2. Patient sign up
3. Display all appointments
4. Book appointment
5. Delete appointment
6. Exit
enter choice4
enter id to be booked555
enter patient id3
enter which day you want to book appointmentWednesday
15.45
16.15
16.55
enter timing for appointment15.45
1. Display all doctors
2. Patient sign up
3. Display all appointments
4. Book appointment
5. Delete appointment
6. Exit
enter choice4
enter id to be booked777
enter patient id5
enter which day you want to book appointmentTuesday
13.25
13.5
14.2
enter timing for appointment13.25
1. Display all doctors
2. Patient sign up
3. Display all appointments
4. Book appointment
5. Delete appointment
6. Exit

enter choice3
******************************************************************************************************************************************************
Doctor ID                                                      Timings                                                 Appointments
******************************************************************************************************************************************************
      111 [[12.0, 13.0, 14.0], [15.15, 16.35, 17.35], [9.0, 10.0, 11.0], [12.0, 13.0, 14.0], [15.0, 16.0, 17.0]]      [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
      222 [[20.15, 20.45, 21.25], [2.0, 3.0, 4.0], [10.0, 11.0, 12.15], [17.0, 18.0, 19.0], [20.0, 21.0, 22.0]]      [[0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
      333 [[11.15, 12.15, 12.55], [7.15, 8.0, 9.0], [10.15, 14.15, 15.15], [13.0, 14.0, 15.0], [9.0, 10.0, 11.0]]      [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
      444 [[7.55, 8.15, 9.45], [8.3, 10.15, 11.2], [15.2, 16.3, 17.1], [17.5, 18.15, 19.35], [14.35, 15.15, 16.25]]      [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
      555 [[8.3, 9.1, 9.3], [8.45, 10.3, 11.35], [12.15, 14.2, 15.15], [15.45, 16.15, 16.55], [14.2, 15.35, 16.55]]      [[0, 0, 0], [0, 0, 0], [0, 0, 0], [3, 0, 0], [0, 0, 0]]
      666 [[10.25, 11.3, 12.15], [9.1, 9.55, 10.25], [8.55, 9.45, 10.15], [11.25, 11.55, 12.5], [14.3, 15.25, 15.55]]      [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
      777 [[8.1, 8.55, 9.15], [9.2, 9.55, 12.2], [13.25, 13.5, 14.2], [14.25, 14.55, 16.25], [17.5, 18.1, 18.35]]      [[0, 0, 0], [0, 0, 0], [5, 0, 0], [0, 0, 0], [0, 0, 0]]
************************************************************
The End'''
