import streamlit as st
import mysql.connector
import datetime as dt
import pandas as pd

st.title("EMPLOYEE MANAGEMENT SYSTEM")
st.sidebar.image("EMP_IMG.png")
choice=st.sidebar.selectbox("Actions",("Home","Manager Login","Employee Register","Employee Login" ))


if(choice=="Home"):
    st.image("https://www.clipartmax.com/png/full/121-1219685_human-resource-clip-art.png")
    st.markdown("<h1>WELCOME TO MY APPLICATION</h1>",unsafe_allow_html=True)
    st.write("This is a management application made using python's Streamlit and MySQL. It is built for the demonstration of how data flow and transfer works within the application via Database")
    st.write("These management applications are used in almost every field of businesses like schools, organizations, stores, markets, and many more.")

elif(choice=="Manager Login"):
    st.markdown("<h3>MANAGER LOGIN</h3>",unsafe_allow_html=True)
    if 'mgrlgn' not in st.session_state:
        st.session_state['mgrlgn']=False     
    uid=st.text_input("Enter Manager ID")
    pwd=st.text_input("Enter Password")                          
    btn=st.button("LOGIN")

    if btn:
        mydb=mysql.connector.connect(host="localhost",user="root",password="123456789",database="employee",auth_plugin='mysql_native_password')
        c=mydb.cursor()
        c.execute("select * from manager")

        for row in c:

            if(uid==row[0] and pwd==row[1]):
                st.session_state['mgrlgn']=True
                break

        if(st.session_state['mgrlgn']==False):
            st.header("Incorrect ID or Password")

    if(st.session_state['mgrlgn']):
        st.header("Login Successfull")
        choice2=st.selectbox("Management",("Home","View Employees","Remove Employees"))
        if(choice2 == "View Employees"):
            mydb=mysql.connector.connect(host="localhost",user="root",password="123456789",database="employee",auth_plugin='mysql_native_password')
            d=mydb.cursor()
            d.execute("DELETE from info WHERE empid is null")
            mydb.commit()
            d.execute("DELETE from employee WHERE emid is null")
            mydb.commit()
            df=pd.read_sql("select * from info",mydb)
            st.dataframe(df)

        elif(choice2 == "Remove Employees"):
            eid=st.text_input("Enter Employee ID")
            btn2=st.button("REMOVE")

            if btn2:
                mydb=mysql.connector.connect(host="localhost",user="root",password="123456789",database="employee",auth_plugin='mysql_native_password')
                flag=False
                d=mydb.cursor()
                d.execute("select * from employee")
                result=d.fetchall()
                for row in result:
                    if(eid == row[0]):
                        flag=True
                        break
                    else:
                        flag=False
                if flag==True:
                    sql1="DELETE from employee WHERE emid = %(emid)s"
                    sql2="DELETE from info WHERE empid = %(empid)s"           
                    d.execute(sql1,{'emid':eid})
                    mydb.commit()
                    d.execute(sql2,{'empid':eid})
                    mydb.commit()
                    st.write("Employee Deleted Successfully")
                    d.execute("DELETE from info WHERE empid =''")
                    mydb.commit()
                    d.execute("DELETE from employee WHERE emid =''")
                    mydb.commit()
                else:
                    st.header("Employee Not Found")


elif(choice=="Employee Login"):
    if 'emplgn' not in st.session_state:
        st.session_state['emplgn']=False
    aid=st.text_input("Enter Employee ID")
    pwd=st.text_input("Enter Password")   
    btn3=st.button("LOGIN")
    
    if btn3:
        mydb=mysql.connector.connect(host="localhost",user="root",password="123456789",database="employee",auth_plugin='mysql_native_password')
        c=mydb.cursor()
        c.execute("select * from employee")

        for row in c:

            if(aid==row[0] and pwd==row[1]):
                st.session_state['emplgn']=True
                break

        if(st.session_state['emplgn']==False):
            st.header("Incorrect ID or Password")

    if(st.session_state['emplgn']):
        st.header("Employee Dashboard")
        mydb = mysql.connector.connect(host="localhost", user="root", password="123456789", database="employee",
                                   auth_plugin="mysql_native_password")
        c=mydb.cursor()
        sql="SELECT * from info WHERE empid = %(empid)s"
        c.execute(sql, {'empid':aid })
        result = c.fetchall()
        for x in result:
            st.write("EMPLOYEE ID : ",x[0])
            st.write("EMPLOYEE SALARY : ",x[1])
            st.write("EMPLOYEE NAME : ",x[2])
            st.write("LOAN : ",x[3])

elif(choice=="Employee Register"):
    ctr = 0

    name = st.text_input("Enter Name")
    salary = st.text_input("Enter Monthly Salary")
    loan = st.text_input("Enter loan taken, if not, enter 0")
    eid = st.text_input("Enter Employee ID")
    psd = st.text_input("Choose Password")
    btn4 = st.button("SUBMIT")
    if btn4:
        if(name=="" or salary=="" or loan=="" or eid=="" or psd==""):
            st.header("PLEASE FILL ALL FIELDS")
        else:
            mydb = mysql.connector.connect(host="localhost", user="root", password="123456789", database="employee",
                                           auth_plugin="mysql_native_password")

            c = mydb.cursor()
            c.execute("select * from employee")
            result=c.fetchall()
            for row in result:
                if eid == row[0]:
                        ctr = ctr + 1
            if ctr == 0:
                c.execute("insert into info values(%s,%s,%s,%s)", (eid, salary, name, loan))
                mydb.commit()
                c.execute("insert into employee values(%s,%s)", (eid, psd))
                mydb.commit()
                st.header("Successfully Registered")
            else:
                st.header("Employee Already Exists")     
