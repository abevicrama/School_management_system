
import connection
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"  


def login():
    st.session_state.logged_in = True
    

def logout():
    st.session_state.logged_in = False
    st.rerun()


def show_login_page():
    logging()


def show_dashboard():
    st.title("Dashboard")
    admin_Panel()
    if st.button("Logout"):
        logout()


def main():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.page == "admin":
            show_dashboard()
        elif st.session_state.page == "student":
            student_page()
        elif st.session_state.page == "teacher":
            teachers_page()
        elif st.session_state.page == "subject":
            subjects_page()



def logging():
    
    st.title("SMS")
    userid = st.selectbox(label="Select your ID", options=("001", "002", "003"))
    Uname = st.text_input("User Name")
    Pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        sql = "SELECT uname, password FROM admin"
        connection.mycurser.execute(sql)
        result = connection.mycurser.fetchall()

        if userid == "001" and Uname == result[0][0] and Pwd == result[0][1]:
            st.session_state.logged_in = True
            st.session_state.page = "admin"  # Redirect to admin panel
            st.rerun()

        elif userid == "002" and Uname == result[1][0] and Pwd == result[1][1]:
            st.session_state.logged_in = True
            st.session_state.page = "admin"
            st.rerun()

        elif userid == "003" and Uname == result[2][0] and Pwd == result[2][1]:
            st.session_state.logged_in = True
            st.session_state.page = "admin"
            st.rerun()
            
        else:
            st.warning("Something went wrong. Check your credentials.")


def admin_Panel():
    st.subheader("Admin Panel")


    if st.button("Students page"):
        st.session_state.page = "student"
        st.rerun()

    elif st.button("Teachers page"):
        st.session_state.page = "teacher"
        st.rerun()

    elif st.button("Subject page"):
        st.session_state.page = "subject"
        st.rerun()

def student_page():
    st.sidebar.button("Back to Admin", on_click=lambda: setattr(st.session_state, "page", "admin"))
    
    option = st.sidebar.selectbox(label="Select an operation", options=("Register", "Search", "Update", "Delete","ViweAll"))
    
    sql = "SELECT COUNT(ID) AS NumberOfProducts FROM student;"
    connection.mycurser.execute(sql)
    student_count = connection.mycurser.fetchall()

    st.write("Registerd Student Count : "+str(student_count[0][0]))

    if option == "Register":
        stdname = st.text_input("Student name")
        stdaddress = st.text_input("Student Address")
        stdrel = st.text_input("Student Religion")
        stnDOB = st.date_input("Date of Birth", min_value=date(2008,1,1))
        stdsibcot = st.text_input("Sibling count")
        stdgard = st.text_input("Guardian Name")
        stdcontact = st.text_input("Guardian Mobile")
       
        if st.button("Insert"):
            sql = "INSERT INTO student (name, address, religion, DOB, sibling_count, gardian, contact) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (stdname, stdaddress, stdrel, stnDOB, stdsibcot, stdgard, stdcontact)
            connection.mycurser.execute(sql, val)
            connection.mydb.commit()
            st.success("Student registered successfully!")
    
    elif option=="Search":
        searchID = st.number_input("Search By ID", min_value=1)
        if st.button("Search By ID"):
            try:
                sql = "SELECT * FROM student WHERE ID = %s"
                val = (searchID,)
                connection.mycurser.execute(sql, val)
            
                details = connection.mycurser.fetchall()
            
                if details:  
                    student_data = details[0]
                
                
                    st.write(f"**Student ID:** {student_data[0]}")
                    st.write(f"**Name:** {student_data[1]}")
                    st.write(f"**Address:** {student_data[2]}")
                    st.write(f"**Religion:** {student_data[3]}")
                    st.write(f"**Date of Birth:** {student_data[4]}")
                    st.write(f"**Sibling Count:** {student_data[5]}")
                    st.write(f"**Guardian Name:** {student_data[6]}")
                    st.write(f"**Guardian Contact:** {student_data[7]}")

                else:
                    st.warning("No student found with this ID.")

            except Exception as e:
                st.error(f"An error occurred: {e}")


        searchName = st.text_input("Search By Name")
        if st.button("Search By Name"):
            try:
                sql = "SELECT * FROM student WHERE name = %s"
                val = (searchName,)
                connection.mycurser.execute(sql, val)
            
                details = connection.mycurser.fetchall()
            
                if details:  
                    student_data = details[0]
                
                
                    st.write(f"**Student ID:** {student_data[0]}")
                    st.write(f"**Name:** {student_data[1]}")
                    st.write(f"**Address:** {student_data[2]}")
                    st.write(f"**Religion:** {student_data[3]}")
                    st.write(f"**Date of Birth:** {student_data[4]}")
                    st.write(f"**Sibling Count:** {student_data[5]}")
                    st.write(f"**Guardian Name:** {student_data[6]}")
                    st.write(f"**Guardian Contact:** {student_data[7]}")

                else:
                    st.warning("No student found with this name.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif option=="Update":
        updateID = st.number_input("Enter Student ID", min_value=1)
        update_option = st.selectbox(label="Select: What you want to change", options=("Name", "Address", "Religion", "DOB","Sibling","Guardian","Contact"))
        if update_option=="Name":
            new = st.text_input("Enter New Name")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET name = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Address":
            new = st.text_input("Enter New Address")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET address = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Religion":
            new = st.text_input("Enter New Religion")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET religion = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="DOB":
            new = st.text_input("Enter New Birthday")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET BOD = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Sibling":
            new = st.text_input("Enter New Sibling count")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET BOD = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Guardian":
            new = st.text_input("Enter New Guardion")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET gardion = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Contact":
            new = st.text_input("Enter New Contact No")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET contact = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Update error")

    elif option=="Delete":
        deleteID = st.number_input("Enter Student ID", min_value=1)
        deleteOption = st.selectbox(label="Select: What you want to delete", options=("All","Name","Address","Religion","DOB","Sibling","Guardian","Contact"))
        if deleteOption=="All":
            if st.button("Delete"):
                try:
                    sql = "DELETE FROM student WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Name":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET name = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Address":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET address = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Religion":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET religion = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        
    else:
        st.warning("somthing going to wrong")
    
    if st.button("Back"):
        admin_Panel()

def teachers_page():
    st.write("teachers Page")


    if st.button("Back"):
        admin_Panel()

def subjects_page():
    st.write("subject Page")


    if st.button("Back"):
        admin_Panel()






if __name__ == "__main__":
    main() 