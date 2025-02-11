
import connection
import streamlit as st
import pandas as pd
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
    
    st.title("Mini School Management System")
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
    st.subheader("Student Details")
    sql = "SELECT COUNT(ID) AS NumberOfProducts FROM student;"
    connection.mycurser.execute(sql)
    student_count = connection.mycurser.fetchall()

    st.write("Registerd Student Count : "+str(student_count[0][0]))

    if option == "Register":
        stdname = st.text_input("Student name")
        stdaddress = st.text_input("Student Address")
        stdrel = st.text_input("Student Religion")
        stnDOB = st.date_input("Date of Birth", min_value=date(2001,1,1))
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
            new = st.date_input("Date of Birth", min_value=date(2001,1,1))
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET DOB = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Sibling":
            new = st.text_input("Enter New Sibling count")
            if st.button("Update"):
                try:     
                    sql = "UPDATE student SET sibling = %s WHERE ID = %s"
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
        elif deleteOption=="DOB":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET DOB = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Sibling":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET sibling = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Guardian":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET gardion = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Contact":
            if st.button("Delete"):
                try:
                    sql = "UPDATE student SET contact = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
    elif option=="ViweAll":
        try:
            sql = "select * from student"
            connection.mycurser.execute(sql)
            student_table = connection.mycurser.fetchall()
            df = pd.DataFrame(student_table, columns=["ID","name", "address", "religion", "DOB", "sibling_count", "gardian", "contact"])
            st.dataframe(df)
        except:
            st.warning("Cannot viwe Table")

    else:
        st.warning("somthing going to wrong")
    


def teachers_page():
    st.sidebar.button("Back to Admin", on_click=lambda: setattr(st.session_state, "page", "admin"))
    
    option = st.sidebar.selectbox(label="Select an operation", options=("Register", "Search", "Update", "Delete", "ViewAll"))
    st.subheader("Teacher Details")

    sql = "SELECT COUNT(ID) AS NumberOfProducts FROM teachers;"
    connection.mycurser.execute(sql)
    t_count = connection.mycurser.fetchall()
    st.write("Registered Teacher Count : " + str(t_count[0][0]))

    if option == "Register":
        tcr_name = st.text_input("Teacher Name")
        tcr_address = st.text_input("Teacher Address")    
        tcr_contact = st.text_input("Mobile")

        
        subject_count = st.number_input("How many subjects does the teacher teach?", min_value=1, step=1)

        
        if "tcr_subjects" not in st.session_state or len(st.session_state.tcr_subjects) != subject_count:
            st.session_state.tcr_subjects = [""] * subject_count  

        
        for i in range(subject_count):
            st.session_state.tcr_subjects[i] = st.text_input(f"Subject {i+1}", 
                                                             value=st.session_state.tcr_subjects[i], 
                                                             key=f"subject_{i}_{subject_count}") 

        if st.button("Insert"):
            sql = "INSERT INTO teachers (name, address, subject, contact) VALUES (%s, %s, %s, %s)"
            val = (tcr_name, tcr_address, ", ".join(st.session_state.tcr_subjects), tcr_contact)
            connection.mycurser.execute(sql, val)
            connection.mydb.commit()
            st.session_state.tcr_subjects = [""] * subject_count            
            st.success("Teacher registered successfully!")


    
    elif option=="Search":
        searchID = st.number_input("Search By ID", min_value=1)
        if st.button("Search By ID"):
            try:
                sql = "SELECT * FROM teachers WHERE ID = %s"
                val = (searchID,)
                connection.mycurser.execute(sql, val)
            
                details = connection.mycurser.fetchall()
            
                if details:  
                    t_data = details[0]               
                    st.write(f"**Teacher ID:** {t_data[0]}")
                    st.write(f"**Name:** {t_data[1]}")
                    st.write(f"**Address:** {t_data[2]}")
                    st.write(f"**Subjects:** {t_data[3]}")
                    st.write(f"**Contact:** {t_data[4]}")
                else:
                    st.warning("No teacher found with this ID.")

            except Exception as e:
                st.error(f"An error occurred: {e}")


        searchName = st.text_input("Search By Name")
        if st.button("Search By Name"):
            try:
                sql = "SELECT * FROM teachers WHERE name = %s"
                val = (searchName,)
                connection.mycurser.execute(sql, val)
            
                details = connection.mycurser.fetchall()
            
                if details:  
                    t_data = details[0]    
                    st.write(f"**Teacher ID:** {t_data[0]}")
                    st.write(f"**Name:** {t_data[1]}")
                    st.write(f"**Address:** {t_data[2]}")
                    st.write(f"**Subject:** {t_data[3]}")
                    st.write(f"**Contact:** {t_data[4]}")


                else:
                    st.warning("No student found with this name.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    elif option=="Update":
        updateID = st.number_input("Enter Teacher ID", min_value=1)
        update_option = st.selectbox(label="Select: What you want to change", options=("Name", "Address", "Subject", "Contact"))
        if update_option=="Name":
            new = st.text_input("Enter New Name")
            if st.button("Update"):
                try:     
                    sql = "UPDATE teachers SET name = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Address":
            new = st.text_input("Enter New Address")
            if st.button("Update"):
                try:     
                    sql = "UPDATE teachers SET address = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Subject":
            new = st.text_input("Enter New Subjects seperating with comma(,)")
            if st.button("Update"):
                try:     
                    sql = "UPDATE teachers SET religion = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        
        elif update_option=="Contact":
            new = st.text_input("Enter New Contact No")
            if st.button("Update"):
                try:     
                    sql = "UPDATE teachers SET contact = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Update error")

    elif option=="Delete":
        deleteID = st.number_input("Enter teachers ID", min_value=1)
        deleteOption = st.selectbox(label="Select: What you want to delete", options=("All","Name","Address","Subjects","Contact"))
        if deleteOption=="All":
            if st.button("Delete"):
                try:
                    sql = "DELETE FROM teachers WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Name":
            if st.button("Delete"):
                try:
                    sql = "UPDATE teachers SET name = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Address":
            if st.button("Delete"):
                try:
                    sql = "UPDATE teachers SET address = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Subjects":
            if st.button("Delete"):
                try:
                    sql = "UPDATE teachers SET religion = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        
        elif deleteOption=="Contact":
            if st.button("Delete"):
                try:
                    sql = "UPDATE teachers SET contact = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
    elif option=="ViewAll":
        try:
            sql = "select * from teachers"
            connection.mycurser.execute(sql)
            tt_table = connection.mycurser.fetchall()
            df = pd.DataFrame(tt_table, columns=["ID", "Name", "Address", "Subject", "Contact"])
            st.dataframe(df)
        except:
            st.warning("Cannot viwe Table")
        

    else:
        st.warning("somthing going to wrong")



def subjects_page():
    
    st.sidebar.button("Back to Admin", on_click=lambda: setattr(st.session_state, "page", "admin"))
    
    option = st.sidebar.selectbox(label="Select an operation", options=("ADD", "Search", "Update", "Delete", "ViewAll"))
    st.subheader("Subject Details")

    sql = "SELECT COUNT(ID) AS NumberOfProducts FROM subjects;"
    connection.mycurser.execute(sql)
    s_count = connection.mycurser.fetchall()
    st.write("Registered Teacher Count : " + str(s_count[0][0]))

    if option == "ADD":
        tcr_name = st.text_input("subject")
    
        teacher_count = st.number_input("How many teachers do the subject ?", min_value=1, step=1)

        
        if "t_names" not in st.session_state or len(st.session_state.t_names) != teacher_count:
            st.session_state.t_names = [""] * teacher_count  

        
        for i in range(teacher_count):
            st.session_state.t_names[i] = st.text_input(f"Teacher {i+1}", 
                                                             value=st.session_state.t_names[i], 
                                                             key=f"Teacher_{i}_{teacher_count}") 

        if st.button("Insert"):
            sql = "INSERT INTO subjects (subject,teachers) VALUES (%s, %s)"
            val = (tcr_name, ", ".join(st.session_state.t_names))
            connection.mycurser.execute(sql, val)
            connection.mydb.commit()
            st.session_state.t_names = [""] * teacher_count           
            st.success("Subject add successfully!")


    
    elif option=="Search":
        searchID = st.number_input("Search By ID", min_value=1)
        if st.button("Search By ID"):
            try:
                sql = "SELECT * FROM subjects WHERE ID = %s"
                val = (searchID,)
                connection.mycurser.execute(sql, val)
            
                details = connection.mycurser.fetchall()
            
                if details:  
                    s_data = details[0]               
                    st.write(f"**Subject ID:** {s_data[0]}")
                    st.write(f"**Subject:** {s_data[1]}")
                    st.write(f"**Teachers:** {s_data[2]}")
 
                else:
                    st.warning("No subject found with this ID.")

            except Exception as e:
                st.error(f"An error occurred: {e}")


        searchName = st.text_input("Search By Subject")
        if st.button("Search By Name"):
            try:
                sql = "SELECT * FROM subjects WHERE subject = %s"
                val = (searchName,)
                connection.mycurser.execute(sql, val)
            
                details = connection.mycurser.fetchall()
            
                if details:  
                    s_data = details[0]               
                    st.write(f"**Subject ID:** {s_data[0]}")
                    st.write(f"**Subject:** {s_data[1]}")
                    st.write(f"**Teachers:** {s_data[2]}")



                else:
                    st.warning("No subject found with this name.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
      

    elif option=="Update":
        updateID = st.number_input("Enter subject ID", min_value=1)
        update_option = st.selectbox(label="Select: What you want to change", options=("Subject", "Teachers"))
        if update_option=="Subject":
            new = st.text_input("Enter New Subject name")
            if st.button("Update"):
                try:     
                    sql = "UPDATE subjects SET subject = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        elif update_option=="Teachers":
            new = st.text_input("Enter New teachers")
            if st.button("Update"):
                try:     
                    sql = "UPDATE subjects SET teachers = %s WHERE ID = %s"
                    val = (new, updateID)
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Updated")

                except:
                    st.error(f"An error occurred: {e}")
        
        else:
            st.warning("Update error")

    elif option=="Delete":
        deleteID = st.number_input("Enter subjects ID", min_value=1)
        deleteOption = st.selectbox(label="Select: What you want to delete", options=("All","Subject","Teachers"))
        if deleteOption=="All":
            if st.button("Delete"):
                try:
                    sql = "DELETE FROM subjects WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Name":
            if st.button("Delete"):
                try:
                    sql = "UPDATE subjects SET subject = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        elif deleteOption=="Teachers":
            if st.button("Delete"):
                try:
                    sql = "UPDATE subjects SET teachers = NULL WHERE ID=%s"
                    val = (deleteID, )
                    connection.mycurser.execute(sql,val)
                    st.success("Sucessfully Deleted")

                except:
                    st.error(f"An error occurred: {e}")
        
        
        
    elif option=="ViewAll":
        try:
            sql = "select * from subjects"
            connection.mycurser.execute(sql)
            tt_table = connection.mycurser.fetchall()
            df = pd.DataFrame(tt_table, columns=["ID", "Subject", "Teachers"])
            st.dataframe(df)
        except:
            st.warning("Cannot viwe Table")
        

    else:
        st.warning("somthing going to wrong")








if __name__ == "__main__":
    main() 