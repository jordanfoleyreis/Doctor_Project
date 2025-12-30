import sqlite3

def connect_db():
   
    conn = sqlite3.connect('Doctor.db')
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            patientid INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            gender TEXT,
            insurance INTEGER,
            insurancename TEXT,
            policynumber TEXT,
            phonenumber TEXT,
            email TEXT,
            streetaddress TEXT,
            zipcode TEXT,
            dateofbirth TEXT,
            last4snn TEXT,
            age INTEGER
            
            )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctor(
            doctorid INTEGER PRIMARY KEY AUTOINCREMENT,
            doctorfirstname TEXT,
            doctorlastname TEXT
         )
    """)
    
    cur.execute("""   
        CREATE TABLE IF NOT EXISTS appointment(
            appointmentid INTEGER PRIMARY KEY AUTOINCREMENT,
            appointmentdate TEXT,
            appointment_status TEXT,
            appointmenttime TEXT,
            appointmenttype TEXT,
            doctorid INTEGER,
            patientid INTEGER,
            FOREIGN KEY (doctorid) REFERENCES doctor(doctorid),
            FOREIGN KEY(patientid) REFERENCES patients(patientid)
            
         )
    """)
    cur.execute("""       
        CREATE TABLE IF NOT EXISTS schedule(
            scheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_first_name TEXT,
            staff_last_name TEXT,
            workdate TEXT,
            start_time TEXT,
            end_time TEXT
        
        )
    """)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS visit_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_first_name TEXT,
        patient_last_name TEXT,
        visit_date TEXT,
        visit_time TEXT,
        provider TEXT,
        appointment_type TEXT,
        summary TEXT,
        follow_up_needed TEXT,
        follow_up_timing TEXT,
        next_visit_type TEXT,
        referral_made TEXT,
        referral_to TEXT,
        front_desk_notes TEXT,
        provider_signature TEXT,
        signature_date TEXT
        
    )
    ''')
    conn.commit()
    
    return conn

#main function
def main():
    conn = connect_db()
    user_choice = 0
    while user_choice != 6:
        print("\n Welcome to Doctor Office Database: ")
        print("----------------------------------------")
        print("1. Patient Appointments Menu")
        print("2. Patient Information Menu")  
        print("3. Staff Schedule Menu")
        print("4. Visit Summary Menu")
        print("5. Reports Menu")
        print("6. Exit System")
        print("----------------------------------------")
        
        user_choice = int(input("Please enter a number 1-6: "))
        if user_choice == 1:
            print("\nYou selected: Patient Appointments Menu")
            patientappts(conn) 
        elif user_choice == 2:
            print("\nYou selected: Patient Information Menu")
            patientinfo(conn)  
        elif user_choice == 3:
            print("\n You selected: Staff Schedule Menu")
            staffschedule(conn)  
        elif user_choice == 4:
            print("\nYou selected: Visit Summary Menu")
            visit_sum(conn) 
        elif user_choice == 5:
            print("\nYou Selected: Reports Menu")
            report(conn)
            
        elif user_choice == 6:
            print("\nHave a Good Day!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")
            
    conn.close()
#function 1 
def patientappts(conn):
    user_choice = 0
    while user_choice != 4:
        print('\n Welcome to Patient Appointments Menu')
        print("--------------------------------------")
        print('1. View Appointments')
        print('2. Change Current Appointment')
        print('3. Add Appointment')
        print('4. Exit')
        print("--------------------------------------")
        
        user_choice = int(input("Select a Choice.(1-4): "))
        
        if user_choice == 1:
            print("\nYou selected: View All Appointments or By Day/ By Provider")
            appts_menu(conn)
        elif user_choice == 2:
            print("\nYou selected: Change Current Appointment")
            change_appts(conn)  
        elif user_choice == 3:
            print("\nYou selected: Add Appointment")
            add_appts(conn)
        elif user_choice == 4:
            print("\nExiting Patient Appointment Menu")
        
        else:
            print("\nInvalid Choice, Please Try Again")
def appts_menu(conn):
    user_choice = 0
    while user_choice != 4:
        print('\n Welcome to View Appointments Menu')
        print("--------------------------------------")
        print('1. View All Appointments')
        print('2. View Appointments By Day')
        print('3. View Appointment By Doctor')
        print('4. Exit')
        print("--------------------------------------")
        
        user_choice = int(input("Select a Choice.(1-4): "))
        
        if user_choice == 1:
            print("\nYou selected: View All Appointments")
            print_appts(conn) 
          
        elif user_choice == 2:
            print("\nYou selected: View Appointments By Day")
            view_appts_day(conn)
            
        elif user_choice == 3:
            print("\nYou selected: View Appointments By Doctor")
            view_appts_doc(conn)
        elif user_choice == 4:
            print("\nExiting View Appointment Menu")
        else:
            print("\nInvalid Choice, Please Try Again")    
def view_appts_doc(conn):
    cur = conn.cursor()
    cur.execute (" SELECT * FROM doctor")
    rows = cur.fetchall()
    if not rows:
        print("\nNo Doctors Found.")  
    else:
        print("\nDoctor Names")
        for i in rows:
            print(f"""
Doctor ID  : {i[0]}
Doctor Name: {i[2]}
""")
        doctorid = int(input("\nEnter Doctor ID: "))
        
        cur.execute("""
SELECT A.appointmentid, A.appointmentdate, A.appointmenttime, A.doctorid, A.patientid, A.appointment_status, A.appointmenttype, P.firstname, P.lastname, D.doctorlastname
FROM appointment AS A
JOIN patients AS P on P.patientid = A.patientid
JOIN doctor AS D on D.doctorid = A.doctorid
WHERE D.doctorid = ? 
ORDER BY A.appointmenttime
    """,(doctorid,))
        
        rows = cur.fetchall()
        
        if not rows:
            print("\nNo Appointment Found For This Doctor.")
            
        else:
            print(
"\nAppointment List")
            for row in rows:              
                print(f"""
Patient Name       : {row[7]} {row[8]}
Appointment ID     : {row[0]}
Appointment Date   : {row[1]}
Appointment Time   : {row[2]}
DoctorID           : {row[3]}
Doctor Name        : {row[9]}
Patient ID         : {row[4]}
Appointment Status : {row[5]}
Appointment Type   : {row[6]}
""")
     
def view_appts_day(conn):
    cur = conn.cursor()
    appointmentdate = input("\nEnter Appointment date (YYYY-MM-DD): ").strip()
    
    cur.execute(""" SELECT A.appointmentid, A.appointmentdate, A.appointmenttime, A.doctorid, A.patientid, A.appointment_status, A.appointmenttype, P.firstname, P.lastname, D.doctorlastname
    FROM appointment AS A
    JOIN patients AS P on P.patientid = A.patientid
    JOIN doctor AS D on D.doctorid = A.doctorid
    WHERE A.appointmentdate = ? 
    ORDER BY A.appointmentdate, A.appointmenttime
    """ ,(appointmentdate,))
    
    rows = cur.fetchall()
    
    if not rows:
        print("\nNo Appointment Found.")
             
    else:
        print(
"\nAppointment List")
        for row in rows: 
            print(f"""
Patient Name       : {row[7]} {row[8]}
Appointment ID     : {row[0]}
Appointment Date   : {row[1]}
Appointment Time   : {row[2]}
DoctorID           : {row[3]}
Doctor Name        : {row[9]}
Patient ID         : {row[4]}
Appointment Status : {row[5]}
Appointment Type   : {row[6]}
""")
            
def print_appts(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT A.appointmentid, A.appointmentdate, A.appointmenttime, A.doctorid, A.patientid, A.appointment_status, A.appointmenttype, P.firstname, P.lastname, D.doctorlastname
    FROM appointment AS A
    JOIN patients AS P on P.patientid = A.patientid
    JOIN doctor AS D on D.doctorid = A.doctorid
    ORDER BY A.appointmenttime, A.appointmentdate
    """)
    
    rows = cur.fetchall()
    
    if not rows:
        print("\nNo Appointment Found.")
        
    else:
        print(
"\nAppointment List")
        
        for row in rows:
            print(f"""
Patient Name       : {row[7]} {row[8]}
Appointment ID     : {row[0]}
Appointment Date   : {row[1]}
Appointment Time   : {row[2]}
DoctorID           : {row[3]}
Doctor Name        : {row[9]}
Patient ID         : {row[4]}
Appointment Status : {row[5]}
Appointment Type   : {row[6]}
""")
            
def change_appts(conn):
    user_choice = 0
    while user_choice !=6:
        print("\nWelcome To The Change Appointments Menu")
        print("----------------------------------------")
        print("1. Change Appointment Date")
        print("2. Change Appointment Time")
        print("3. Change Doctor ID")
        print("4. Delete Appointment")
        print("5. Change Appointment Status")
        print("6. Exit To Appointment Menu")
        print("----------------------------------------")
        
        user_choice= int(input("\nEnter Your Choice(1-6): "))
        if user_choice ==1:
            print("\n Entering Date Changing Menu")
            appt_date(conn)
            
        elif user_choice ==2:
            print("\n Entering Time Changing Menu")
            appt_time(conn)
            
        elif user_choice ==3:
            print("\n Entering Change Doctor ID Menu")
            appt_doc(conn)
            
        elif user_choice ==4:
            print("\n Entering Delete Appointment Menu")
            appt_del(conn)
        elif user_choice == 5:
            print("\n Entering Change Appointment Status Menu")
            appt_status(conn)
        elif user_choice ==6:
            print("\n Exiting To Appointment Menu")
            
        else:
            print("\nInvalid Choice Please Try Again")
            
def book_appointment(conn,appointmentdate,appointmenttime, doctorid):
    cur = conn.cursor()
    cur.execute("""SELECT * FROM appointment
                WHERE appointmentdate = ? AND appointmenttime = ? AND doctorid = ?""",(appointmentdate, appointmenttime, doctorid))
    row = cur.fetchall()
    if not row:
        book_status = True
    else:
        book_status = False
    return book_status

def appt_status(conn):
    count = 0
    appointment = None 
    print_appts(conn)
    print("\n Welcome To Appointment Status Menu")
    print("----------------------------------------")
    
    cur = conn.cursor()
    
    while not appointment:
        appointment_id = int(input("Please enter the ID of the appointment you wish to change: "))
        
        cur.execute("SELECT appointmentid FROM appointment WHERE appointmentid = ?", (appointment_id,))
        appointment = cur.fetchone()
            
        if not appointment:
            print("No appointment found with that ID. Please try again.")
            count +=1
            if count == 3:
                return
    apptstatus = input("Please Enter New Appointment Status(Missed/Completed/Canceled/Scheduled): ").lower().strip()
    
    while not(apptstatus == 'missed' or apptstatus =='completed' or apptstatus =='canceled' or apptstatus == 'scheduled'):
        print("\t\nPlease Try Again.")
        apptstatus = input("Please Enter New Appointment Status(Missed/Completed/Canceled/Scheduled): ").lower().strip()
        
    cur.execute("""
    UPDATE appointment
    SET appointment_status = ?
    WHERE appointmentid =?
    """,(apptstatus, appointment_id))
    
    conn.commit()
    
    print("\nAppointment Successfully Updated")
    
def appt_date(conn):
    appointment = None
    count = 0
    print_appts(conn)
    print("\n Welcome To Appointment Date Menu")
    print("----------------------------------------")
    cur = conn.cursor()
    
    while not appointment:
        appointment_id = int(input("Please enter the ID of the appointment you wish to change: "))
        
        cur.execute("SELECT appointmentid FROM appointment WHERE appointmentid = ?", (appointment_id,))
        appointment = cur.fetchone()
         
        if not appointment:
            print("No appointment found with that ID. Please try again.")
            count +=1
            if count == 3:
                return
    apptdate = input("Please Enter The New Date For The Appointment(YYYY-MM-DD): ")
    
    cur.execute("UPDATE appointment SET appointmentdate = ? WHERE appointmentid = ?",(apptdate, appointment_id))
    
    conn.commit()
    
    print("\nAppointment Successfully Updated")
    
def appt_time(conn):
    appointment = None
    count = 0 
    print_appts(conn)
    print("\n Welcome To Appointment Time")
    print("----------------------------------------")
    cur = conn.cursor()
    
    while not appointment:
        appointment_id = int(input("Please enter the ID of the appointment you wish to change: "))
        
        cur.execute("SELECT appointmentid FROM appointment WHERE appointmentid = ?", (appointment_id,))
        appointment = cur.fetchone()
            
        if not appointment:
            print("No appointment found with that ID. Please try again.")
            count +=1
            if count == 3:
                return
    appttime = input("Please Enter The New Time For The Appointment(HH:MM): ")
    
    cur.execute("UPDATE appointment SET appointmenttime = ? WHERE appointmentid = ?",(appointment_id, appttime))
    
    conn.commit()
    
    print("\nAppointment Succesfully Updated")
    
def appt_doc(conn):
    appointment = None
    count = 0 
    print_appts(conn)
    
    cur = conn.cursor()
    
    print("\n Welcome To Change Appointment Doctor Menu")
    print("----------------------------------------")
    
    while not appointment:
        appointment_id = int(input("Please enter the ID of the appointment you wish to change: "))
        
        cur.execute("SELECT appointmentid FROM appointment WHERE appointmentid = ?", (appointment_id,))
        appointment = cur.fetchone()
            
        if not appointment:
            print("No appointment found with that ID. Please try again.")
            count +=1
            if count == 3:
                return
    cur.execute("""
                SELECT doctorid, doctorlastname
                FROM doctor
                """)
    rows = cur.fetchall()
    
    if not rows:
        print("No Doctors Found.")
    
    for row in rows:
        print(f"""
Doctor ID  : {row[0]}
Doctor Name: {row[1]}
""")
                
    doctorid = int(input("Enter Doctor ID: "))
        
    cur.execute (" UPDATE appointment SET doctorid = ? WHERE appointmentid = ?",(doctorid, appointment_id))
    
    conn.commit()
    
    print("\nAppointment Successfully Updated")
    
def appt_del(conn):
    appointment = None
    count = 0
    print_appts(conn)
    
    cur = conn.cursor()
    print("\n Welcome To Appointment Delete Menu")
    print("----------------------------------------")
    
    while not appointment:
        appointment_id = int(input("Please enter the ID of the appointment you wish to change: "))
        
        cur.execute("SELECT appointmentid FROM appointment WHERE appointmentid = ?", (appointment_id,))
        appointment = cur.fetchone()
            
        if not appointment:
            print("No appointment found with that ID. Please try again.")
            count +=1
            if count == 3:
                return

    
    cur.execute ("DELETE FROM appointment WHERE appointmentid = ?", (appointment_id,))
    
    conn.commit()
    
    print("\nAppointment Successfully Deleted.")
    
def add_appts(conn):
    cur = conn.cursor()
    book_status = False
    
    while book_status != True:        
        print("\nWelcome To Add Appointment Menu")
        print("----------------------------------------")
        
        appointmentdate = input("Enter Appointment date (YYYY-MM-DD): ").strip()
        
        appointmenttime = input("Enter Appointment time (24-hour)(HH:MM): ").strip()
        
        appointmenttype = input("Enter Appointment Type: \n\tNew Patient \n\tWellness Check \n\tChronic Condition  \n\tSick Visit  \n\tMedication Refill \n\tOther \n: ").strip().lower()
        while not(appointmenttype == 'new patient' or appointmenttype =='wellness check' or appointmenttype =='chronic condition' or appointmenttype == 'sick visit'or appointmenttype == 'medication refill' or appointmenttype == 'other'):
            
            print("\t\nPlease Try Again.")
            
            appointmenttype = input("Enter Appointment Type: \n\tNew Patient \n\tWellness Check \n\tChronic Condition  \n\tSick Visit  \n\tMedication Refill \n\tOther \n: ").strip().lower()
        
        cur.execute ("SELECT * FROM doctor")
        
        rows = cur.fetchall()
        if not rows:
            print("No Doctors Found.")
            return
        else:
            for i in rows:
                print(f"""
Doctor ID  : {i[0]}
Doctor Name: {i[2]} """)
                
            doctorid = int(input("Enter Doctor ID: "))
            book_status = book_appointment(conn, appointmentdate, appointmenttime, doctorid)
            if book_status == True:
                cur.execute("SELECT patientid, firstname, lastname, zipcode, streetaddress FROM patients")
            
                rows = cur.fetchall()
                if not rows:
                    print("\nNo Patients Found. Please Set Up Patient Profile First.")
                    break
                else:
                    print("\nPatient Table")
                    for i in rows:
                        print(f"""
Patient ID      : {i[0]}
Patient Name    : {i[1]} {i[2]}
Patient Zip Code: {i[3]}
Patient Address : {i[4]}
""")
                patientid = int(input("Enter Patient ID: "))
                appointment_status = 'scheduled'
                cur.execute("""
                INSERT INTO appointment (appointmentdate, appointmenttime, appointmenttype, doctorid, patientid, appointment_status)
                VALUES (?, ?, ?, ?, ?, ? )
            """, (appointmentdate, appointmenttime, appointmenttype, doctorid, patientid, appointment_status))
                conn.commit()
                
                print("\nAppointment Added.")
            else:
                print("There is already an appointment at this time, Please Try Again")
                try_again = input("Try again? (Y for Yes/N for No): ").lower().strip()
                    
                if (try_again == "n"):
                    break        
    #function 2
def patientinfo(conn):
    
    user_choice = 0
    while user_choice !=5:
        print('\n Welcome to the Patient information Menu')
        print("----------------------------------------")
        print('1. View All Patients.')
        print('2. View Specific Patient.')
        print('3. Change Patient Information.')
        print('4. Add New Patient.')
        print('5. Exit')
        print("----------------------------------------")
        
        user_choice = int(input("Select a Choice(1-5): "))
        
        if user_choice == 1:
            print("You Selected: View Current Patients.")
            view_patients(conn)
            
        elif user_choice == 2:
            print("You Selected: View Specific Patient.")
            view_specific_patient(conn)
            
        elif user_choice == 3:
            print("You Selected: Change Patient Information.)")
            change_patientinfo(conn)
            
        elif user_choice == 4:
            print("You Selected: Add Patient.")
            add_patient(conn)
            
        elif user_choice == 5:
            print("Exiting patient info Menu.")
            
        else:
            print("Invalid choice. Please try again.")
            
def view_patients(conn):
    cur = conn.cursor()
    cur.execute(" SELECT * FROM patients")
    rows = cur.fetchall()
    
    if not rows:
        print("No Patients Found.")
        
    for row in rows:
        print(f"""
Patient ID    : {row[0]}
Patient Name  : {row[1]} {row[2]}
Gender        : {row[3]}
Insurance     : {row[4]}
Insurance Name: {row[5]}
Policy Number : {row[6]}
Phone Number  : {row[7]}
Email         : {row[8]}
Street Address: {row[9]}
Zip Code      : {row[10]}
Date of Birth : {row[11]}
Last 4snn     : {row[12]}
Age           : {row[13]}
""")

        
        
def view_specific_patient(conn):
    patient_id = int(input("Please Enter the patient ID: "))
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE patientid = ?", (patient_id,))
    rows = cur.fetchall()
    
    if not rows:
        print("No patient found with that ID.")
    else:
        for row in rows:
            print(f"""
Patient ID    : {row[0]}
Patient Name  : {row[1]} {row[2]}
Gender        : {row[3]}
Insurance     : {row[4]}
Insurance Name: {row[5]}
Policy Number : {row[6]}
Phone Number  : {row[7]}
Email         : {row[8]}
Street Address: {row[9]}
Zip Code      : {row[10]}
Date of Birth : {row[11]}
Last 4snn     : {row[12]}
Age           : {row[13]}
""")     
def change_patientinfo(conn):
    print("Welcome To The 'Change Patient Info Menu")
    user_choice = 0
    
    while user_choice != 10:
        print("1. Change First Name.")
        print("2. Change Last Name. ")
        print("3. Change Insurance. ")
        print("4. Change Insurance Name.")
        print("5. Change Policy Number.")
        print("6. Change Phone Number.")
        print("7. Change Email.")
        print("8. Change Street Address.")
        print("9. Change Zip code.")
        print("10.Exit Program.")
        
        user_choice = int(input("Enter Your Selection(1-10): "))
    
    
        if user_choice == 1:
            print("\n You Selected: Change First Name")
            fname_change(conn)
            
        elif user_choice == 2:
            print("\n You Selected: Change Last Name")
            lname_change(conn)
            
        elif user_choice == 3:
            print("\n You Selected: Change Insurance Status")
            insurance_change(conn)
        
        elif user_choice == 4:
            print("\n You Selected: Change Insurance Name")
            insurancename_change(conn)
        
        elif user_choice ==5:
            print("\n You Selected: Change Policy Number")
            polinum_change(conn)
            
        elif user_choice ==6:
            print("\n You Selected: Change Phone Number")
            phonenum_change(conn)
            
        elif user_choice ==7:
            print("\n You Selected: Change Email")
            email_change(conn)
        
        elif user_choice ==8:
            print("\n You Selected: Change Street Address.")
            address_change(conn)
            
        elif user_choice ==9:
            print("\n You Selected: Change Zipcode.")
            zip_change(conn)
        elif user_choice == 10:
            print("\nExiting Schedule Change Menu.")
            
        else:
            print("\nInvalid Choice, please try again.")

def fname_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID You Wish To Update: "))
    
    new_fname = input("Enter The New First Name: ").strip().lower()
    cur = conn.cursor()
    cur.execute("UPDATE patients SET firstname = ? WHERE patientid = ?",(new_fname, id))
    conn.commit()
    print("First Name Status Updated.")

def lname_change(conn):
    view_patients(conn)
    id = int(input("Enter Patient ID You Wish To Update: "))
    new_lname = input("Enter the New Last Name: ").strip().lower()
    cur = conn.cursor()
    cur.execute("UPDATE patients SET lastname = ? WHERE patientid = ?",(new_lname, id))
    conn.commit()
    print("last name status updated.")
    
def insurance_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_insurance = int(input("Enter the new insurance (1 for Yes or 0 for no): "))
    cur = conn.cursor()
    cur.execute("UPDATE patients SET insurance = ? WHERE patientid = ?",(new_insurance, id))
    conn.commit()
    print("insurance status updated.")
    
def insurancename_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_insurancename = input("Enter the new insurance name: ").strip().lower()
    cur = conn.cursor()
    cur.execute("UPDATE patients SET insurancename = ? WHERE patientid = ?",(new_insurancename, id))
    conn.commit()
    print("insurance name status updated.")
        
def polinum_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_policynumber = input("Enter the new policy number: ")
    cur = conn.cursor()
    cur.execute("UPDATE patients SET policynumber = ? WHERE patientid = ?",(new_policynumber, id))
    conn.commit()
    print("policy number status updated.")
    
def phonenum_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_phonenumber = input("Enter the new phone number(XXX-XXX-XXXX): ")
    cur = conn.cursor()
    cur.execute("UPDATE patients SET phonenumber = ? WHERE patientid = ?",(new_phonenumber, id))
    conn.commit()
    print("phone number status updated.")
    
def email_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_email = input("Enter the new email: ").strip().lower()
    cur = conn.cursor()
    cur.execute("UPDATE patients SET email = ? WHERE patientid = ?",(new_email, id))
    conn.commit()
    print("email status updated.")
    
def address_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_streetaddress = input("Enter the new street address: ").strip().lower()
    cur = conn.cursor()
    cur.execute("UPDATE patients SET streetaddress = ? WHERE patientid = ?",(new_streetaddress, id))
    conn.commit()
    print("street address status updated.")
    
def zip_change(conn):
    view_patients(conn)
    id = int(input("Enter patient ID you wish to update: "))
    new_zipcode = input("Enter the new zip code: ")
    cur = conn.cursor()
    cur.execute("UPDATE patients SET zipcode = ? WHERE patientid = ?",(new_zipcode, id))
    conn.commit()
    print("zipcode status updated.")
    
def add_patient(conn):
    #Personal Info
    firstname = input("Please enter patient's first name: ").strip().lower()
    lastname = input("Please enter patient's last name: ").strip().lower()
    gender = input("Please enter the patient's gender(Male/Female/Other): ").strip().lower()
    while not(gender == 'male' or gender =='female' or gender =='other'):
        print("\t\nPlease Try Again.")
        gender = input("Please enter the patient's gender(Male/Female/Other): ").strip().lower() 
    dateofbirth = (input("Please enter the patient's date of birth(YYYY-MM-DD): ")).strip().lower()
    age = int(input("Please enter the patient's age: "))
    
    #Contact Info
    last4snn = (input("Please enter the patient's last 4 digits of their social security number: "))
    phonenumber = (input("Please enter the patient's phone number(XXX-XXX-XXXX): "))
    streetaddress = input("Please enter the patient's street address: ").strip().lower()
    email = input("Please enter the patient's email: ").strip().lower()
    zipcode =(input("Please enter the patient's zipcode: "))
    
    #Insurance Info:
    insurance = int(input("Please enter the patient's insurance(1 for Yes/0 For No): "))
    if insurance == 1:
        insurancename = input("Please enter the patient's insurance name: ")
        policynumber = input("Please enter the patient's policy number: ")
    else:
        insurancename = 'NULL'
        policynumber = 'NULL'

    
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO patients (firstname, lastname, gender, insurance, insurancename, policynumber, phonenumber, email, streetaddress, zipcode, dateofbirth, last4snn, age)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (firstname, lastname, gender, insurance, insurancename, policynumber, phonenumber, email, streetaddress, zipcode, dateofbirth, last4snn, age))
    conn.commit()
    print(f"\n Patient {firstname} {lastname} added successfully.\n")
    
#function 3   
def staffschedule(conn):
    user_choice = 0
    while user_choice != 3:
        print('\n Welcome to Staff Scheduling Menu')
        print("----------------------------------------")
        print('1. View Staff Schedule.')
        print('2. Change/Add Staff Schedule.')
        print('3. Exit To Main Menu.')
        print("----------------------------------------")
    
        user_choice = int(input("Select a Choice(1-3): "))
        
        if user_choice == 1:
            print("\nYou Selected: View Staff Schedule")
            view_schedule(conn)
            
        elif user_choice == 2:
            print("\nYou Selected: Add/Change Staff Schedule")
            schedule_main(conn)
            
        elif user_choice == 3:
            print("\nExiting Staff Schedule Menu.")
            
        else:
            print("Invalid Choice. Please try again.")
def schedule_main(conn):
    user_choice = 0
    while user_choice != 3:
        print("\n Welcome to Schedule Menu")
        print("----------------------------------------")
        print("1. Change/Delete Schedule.")
        print("2. Add a Schedule.")
        print("3. Exit Scheduling Menu.")
        print("----------------------------------------")
    
        user_choice= int(input("Select A Choice (1-3): "))

        if user_choice == 1:
            print("You Selected Change/Delete Schedule.")
            change_schedule(conn)
        elif user_choice == 2:
            print("You Selected Add to Schedule")
            add_schedule(conn)
        elif user_choice == 3:
            print("Exiting Staff Schedule Menu.")
        else:
            print("Invalid Choice. Please try again.")
            
def view_schedule(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT scheduleID, workdate, start_time, end_time, staff_last_name, staff_first_name
    FROM schedule
    """)
    rows = cur.fetchall()
    if not rows:
        print("\nNo Schedule Found.")
    else:
        for row in rows:
            print(f"""
Schedule ID: {row[0]}
Date       : {row[1]}
Start Time : {row[2]}
End Time   : {row[3]}
Staff Name : {row[4]} {row[5]}
""")
            
def change_schedule(conn):
    user_choice = 0
    while user_choice != 5:
        print("\nWelcome To The Schedule Change Menu")
        print("----------------------------------------")
        print("1. To Change Date.")

        print("2. To Change Start Time.")

        print("3. To Change End Time.")

        print("4. Delete Entire Entry.")
    
        print("5. Exit Program")
        
        user_choice = int(input("Enter Your Selection(1-5): "))
    
        if user_choice == 1:
            print("\n You Selected Change Date")
            date_schedule(conn)
    
        elif user_choice == 2:
            print("\n You Selected: Change Start Time.")
            start_time_schedule(conn)

        elif user_choice == 3:
            print("\n You Selected: Change End Time.")
            end_time_schedule(conn)
        
        elif user_choice == 4:
            print("\nYou Selected: Delete Entire Entry.")
            delete_schedule(conn)
        
        elif user_choice == 5:
            print("\nExiting Schedule Change Menu")
        else:
            print("\nInvalid Choice, please try again.")
         
def print_schedule(conn):
    cur = conn.cursor()
    cur.execute("""SELECT * FROM schedule""")
    rows = cur.fetchall()
    for i in rows:
        print(f"""
ScheduleID: {i[0]}
Staff Name: {i[1]} {i[2]}
Work Date : {i[3]}
Start Time: {i[4]}
End Time  : {i[5]}
""")
 
def date_schedule(conn):
    print_schedule(conn)
    cur = conn.cursor()
    workdate= input("Enter Date Of The Week They Will Work.(YYYY-MM-DD): ")
    id = int(input("Enter Schedule ID: "))
    cur.execute("UPDATE schedule SET workdate = ? WHERE scheduleID = ?",(workdate, id))
    conn.commit()
    print("Schedule Successfully Updated")

def start_time_schedule(conn):
    print_schedule(conn)
    cur = conn.cursor()
    start_time = input("Enter Start Time in 24 Hour Time(e.g HH:MM): " ).strip()
    id = int(input("Enter Schedule ID: "))
    cur.execute("UPDATE schedule SET start_time = ? WHERE scheduleID = ?",(start_time, id))
    conn.commit()
    print("Schedule Successfully Updated")

def end_time_schedule(conn):
    print_schedule(conn)
    cur = conn.cursor()
    id = int(input("Enter Schedule ID: "))
    end_time = input("Enter End Time in 24 Hour Time(e.g HH:MM): ").strip()
    cur.execute("UPDATE schedule SET end_time = ? WHERE scheduleID = ?",(end_time, id))
    conn.commit()
    print("Schedule Successfully Updated")

def delete_schedule(conn):
    print_schedule(conn)
    cur = conn.cursor()
    user_id = int(input("Please enter the ID of the person you want To delete: "))
    
    cur.execute ( """
        DELETE FROM schedule
        WHERE scheduleID = ?
        """,
        (user_id,))
    
    conn.commit()
    print("Schedule Deleted Successfully.")
def add_schedule(conn): 
    staff_first_name = input("Enter Staff First Name: ").strip().lower()
    
    staff_last_name = input ("Enter Staff Last Name: ").strip().lower()
    
    workdate= input("Enter Date Of The Week They Will Work(YYYY-MM-DD): ").strip()
    
    start_time = input("Enter Start Time in 24 Hour Time(e.g HH:MM): " ).strip()
    
    end_time = input("Enter End Time in 24 Hour Time(e.g HH:MM): ").strip()
    
    cur = conn.cursor()
    cur.execute("""INSERT INTO schedule (
        staff_first_name,
        staff_last_name,
        workdate,
        start_time,
        end_time)
        VALUES (?,?,?,?,?)
        """
    , (staff_first_name, staff_last_name, workdate, start_time, end_time))
    conn.commit()
    print("Schedule Updated Successfully.")
#function 4
def visit_sum(conn):
    user_choice = 0
    while user_choice != 4:
        print('\n Welcome to Visit Summary Menu')
        print("----------------------------------------")
        print("1. View Current Visit Summary")
        print('2. Make a Visit Summary')
        print('3. Change Visit Status')
        print('4. Exit Program')
        
        
        user_choice = int(input("Select a Choice.(1-4): "))
    
        if user_choice == 1:
            print("You Selected: 'View Current Visit Summary'")
            current_summary(conn)
        elif user_choice == 2:
            print("You Selected: 'Make a Visit Summary'")
            make_summary(conn)
        elif user_choice ==3:
            print("Going To Visit Status Menu")
            visit_status(conn)
        elif user_choice == 4:
            print("You Selected: Exiting Program")
        else:
            print("Invalid Choice, please try again.")
#work on 
def make_summary(conn):
    cur = conn.cursor()
    print_appts(conn)
    print("\n--- Visit Summary ---")
    
    view_patients(conn)
    patient_id = int(input("Enter Patient ID: "))
    cur.execute('SELECT COUNT(*) FROM appointment WHERE patientid = ? AND appointment_status = "scheduled"', (patient_id,))
    patient = cur.fetchone()[0]
    if patient == 0:
        print("No Patient with Appointment At This Time. Please set up an appointment first.")
        return
    cur.execute("""SELECT P.firstname, P.lastname, A.appointmentdate, A.appointmenttime, D.doctorlastname
                FROM appointment AS A
                JOIN patients AS P ON P.patientid = A.patientid
                JOIN doctor AS D ON D.doctorid = A.doctorid
                WHERE A.patientid = ? 
                ORDER BY A.appointmentdate
                """, (patient_id,))
    row = cur.fetchall()
    
    for rows in row:
        print(f"""
Patient Name: {rows[0]} {rows[1]}
Appointment Date: {rows[2]}
Appointment Time: {rows[3]}
Doctor Last Name: {rows[4]}
""")

    first_name = input("What’s the patient’s first name: ").strip().lower()
    last_name = input("What’s the patient’s last name: ").strip().lower()
    date = input("When was the visit?(YYYY-MM-DD): ").strip()
    time = input("what time was the visit(24-hour)(HH:MM): ").strip()

    provider = input("Who was the provider?(EX: Lewis, Nyguyen, Jones): ").strip().lower()
    while not(provider == 'lewis' or provider =='nyguyen' or provider =='jones'):
        print("\t\nPlease Try Again.")
        provider = input("Who was the provider?(EX: Lewis, Nyguyen, Jones): ").strip().lower()
        
    visit_type = input("What type of appointment was it?\nOptions: New Patient, Wellness Check, Chronic Condition, Sick Visit, Medication Refill, Other: ").strip().lower()
    
    while not(visit_type == 'new patient' or visit_type =='wellness check' or visit_type =='chronic condition' or visit_type == 'sick visit' or visit_type == 'medication refill' or visit_type == 'other'):
        print("Incorrect Input, Try Again")
        visit_type = input("What type of appointment was it?\nOptions: New Patient, Wellness Check, Chronic Condition, Sick Visit, Medication Refill, Other: ").strip().lower()

        
    notes = input("Provider notes or summary for this visit: ").strip()
    
    follow_up_when = ("N/A")
    next_type_known = ("N/A")
    next_type = ("N/A")
    
    follow_up = input("Does the patient need a follow-up? (1 For Yes/0 For No): ")
    
    if follow_up == "1":
        follow_up_when = input("How many days from now: ").strip()
        next_type_known = input("Is it the same as the initial appointment (Enter 1 for Yes or 0 for no): ").strip()
        if next_type_known == "1":
            next_type = visit_type
        elif next_type_known == "0":
            next_type = input("What is the next visit type?\nOptions: New patient, Wellness check, Chronic Condition, Sick Visit, Medication Refill, Other: ").lower().strip()
            while not(next_type == 'new patient' or next_type =='wellness check' or next_type =='chronic condition' or next_type == 'sick visit' or next_type == 'medication refill' or next_type == 'other'):
                print("Please enter a valid input.")
                next_type = input("What type of appointment was it?\n Options: New Patient, Wellness Check, Chronic Condition, Sick visit, Medication Refill, Other: ").strip().lower()
    else:
        print("No follow up needed")
        
    
    referral = input("Was a referral made? (1 For Yes/0 For No): ")

    referral_to = input("Referred to? (doctor or facility) ").strip() if referral == "1" else ""
    
    front_desk_notes = input("Any notes for the front desk or billing team: ").strip()
    signature = input("Provider Signature (Type Name): ").strip().lower()
    signature_date = input("Date of Signature(YYYY-MM-DD): ").strip()
    
    cur.execute('''UPDATE appointment
    SET appointment_status = 'completed'
    WHERE patientid = ? AND appointmentdate = ?
    ''', (patient_id,date))
 
    cur.execute('''
    INSERT INTO visit_summaries (
        patient_first_name, patient_last_name, visit_date, visit_time, provider, appointment_type,
        summary, follow_up_needed, follow_up_timing, next_visit_type,
        referral_made, referral_to, front_desk_notes, provider_signature, signature_date
    ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, date, time, provider, visit_type, notes, follow_up, follow_up_when,
          next_type, referral, referral_to, front_desk_notes, signature, signature_date))
    conn.commit()

    print("\n--- Printed Visit Summary ---")
    print(f"""
Patient         : {first_name} {last_name}
Visit date      : {date} at {time}
Provider        : {provider}
Appointment Type: {visit_type}
Summary/notes   : {notes}
Follow-up needed: {follow_up}
Follow-up Date  : {follow_up_when} days
Next Visit Type : {next_type}
Referral made   : {referral} {f"to {referral_to}" if referral == "1" else ""}
Front desk/notes: {front_desk_notes}
Signed by       : {signature} on {signature_date}
""")

def visit_status(conn):
    cur = conn.cursor()
    
    print_appts(conn)
    
    Appointment_ID = int(input("Enter Appointment ID: "))
    apptstatus = input("Please Enter New Appointment Status(Missed/Completed/Canceled/Scheduled): ").lower().strip()
    
    while not(apptstatus == 'missed' or apptstatus =='completed' or apptstatus =='canceled' or apptstatus == 'scheduled'):
        print("\t\nPlease Try Again.")
        apptstatus = input("Please Enter New Appointment Status(Missed/Completed/Canceled/Scheduled): ").lower().strip()
    cur.execute("""
    UPDATE appointment
    SET appointment_status = ?
    WHERE appointmentid = ?
    """, (apptstatus, Appointment_ID))
    conn.commit()
     
def current_summary(conn): 
    cur = conn.cursor()
    cur.execute("""
           SELECT *
           FROM visit_summaries
    """)
    rows = cur.fetchall()
    if not rows:
        print("\nNo Summaries Found.")
    else:
        print("\n--- Printed Visit Summary ---")
        for row in rows:
    
            print(f"""
Patient              : {row[1]} {row[2]}
Visit Date           : {row[3]} at {row[4]}
Provider             : {row[5]}
Appointment Type     : {row[6]}
Summary/notes        : {row[7]}
Follow-up needed     : {row[8]}
Next Appointment In  : {row[9]} from last visit.
Next Visit Type      : {row[10]}
Referral Made        : {row[11]}
Referral From        : {row[12]}
Front desk/notes     : {row[13]}
Signed by            : {row[14]} on {row[15]}
""")
        
#good function 5
def report(conn):

    user_choice = 0
    
    while user_choice != 5:
        print("\n Report Menu:")
        print("----------------------------------------")
        print("1. View Total Number Of Visits")
        print("2. View Visits Counts by Status/Date Range and Visit Summaries")
        print("3. View Visits By Provider")
        print("4. View Appointments By Type")
        print("5. Exit Menu ")
        print("----------------------------------------")
        user_choice = int(input("Select A Choice(1-5): "))
        
        if user_choice == 1:
            print("\nYou Selected: Total Number Of Visits.")
            total_visit(conn)
            
        elif user_choice ==2:
            print("\nYou Selected: View Visits by Status/Range and Visit Summaries.")
            visit_menu(conn)
            
        elif user_choice ==3:
            print("\nYou Selected: Visits By Provider.")
            visit_provider(conn)
            
        elif user_choice ==4:
            print("\n You Selected: View Appointments By Type.")
            visit_kind(conn)
            
        elif user_choice ==5:
            print("\nLeaving To Main Menu.")
        else:
            print("\n Invalid Input Please Try Again")
def visit_menu(conn):
    user_choice = 0
    while user_choice != 4:
        print("Visit Report Menu")
        print("----------------------------------------")
        print("1. Report: All Visit Summary's")
        print("2. Report: Visit Count By Date Range")
        print("3. Report: Visit Count By Status")
        print("4. Exit Visit Report Menu")
        print("----------------------------------------")
        user_choice = int(input("Select a Choice(1-4): "))
        if user_choice ==1:
            print("Entering: All Visit Summary's")
            all_visit(conn)
        elif user_choice == 2:
            print("Entering: Visit Date Menu")
            date_visit(conn) 
        elif user_choice == 3:
            print("Entering: Visit Count By Status")
            visit_missed(conn)
        elif user_choice == 4:
            print("Exiting: Visit Report Menu")
        else:
            print("Invalid Choice. Please Try Again")
def all_visit(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT patient_first_name, patient_last_name, visit_date, visit_time, provider, appointment_type
    FROM visit_summaries
    """)
    rows = cur.fetchall()
    
    if not rows:
        print("No Visits Found")
    else:
        for row in rows:
            print(f"""
Patient Name    : {row[0]} {row[1]}
Visit Date      : {row[2]}
Visit Time      : {row[3]}
Doctor          : {row[4]}
Appointment Type: {row[5]}
""")

def total_visit(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM appointment WHERE appointment_status = 'completed'")
    rows = cur.fetchone()[0]
    if rows == 0:
        print("No visits found.")
    else:
        print(f" There were {rows} visits")
        
def date_visit(conn):
    cur = conn.cursor()
    start_date = input("Please Enter The Start Date For The Range You Would Like To Check(YYYY-MM-DD): ")
    end_date = input("Please Enter The End Date For For The Range You Would Like To Check(YYYY-MM-DD): ")
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmentdate BETWEEN ? AND ? AND appointment_status = 'completed' """,(start_date, end_date))
    rows = cur.fetchone()[0]
    
    if rows == 0:
        print("No visits found in date range.")
    else:
        print(f" There were {rows} visits from {start_date} to {end_date}")
        
def visit_kind(conn):
    cur = conn.cursor()
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmenttype = 'new patient'AND appointment_status = 'completed'
                """)
    visit_new = cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmenttype = 'wellness check'AND appointment_status = 'completed'
                """)
    visit_well = cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmenttype = 'sick visit'AND appointment_status = 'completed'
                """)
    visit_sick= cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmenttype = 'medication refill'AND appointment_status = 'completed'
                """)
    visit_refill = cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmenttype ='chronic condition'AND appointment_status = 'completed'
                """)
    visit_chronic = cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointmenttype = 'other' AND appointment_status = 'completed'
                """)
    visit_other = cur.fetchone()[0]
    
    print("\nTypes Of Visits:")
    print(f"Number of New Patients             : {visit_new}  " ) 
    print(f"Number of Wellness Checks          : {visit_well}  " )
    print(f"Number of Sick Visits              : {visit_sick}  " )
    print(f"Number of Medication Refills       : {visit_refill} " )
    print(f"Number of Chronic Conditions       : {visit_chronic} " ) 
    print(f"Number of Visits Other             : {visit_other} " ) 
   
def visit_missed(conn):
    cur = conn.cursor()
    cur.execute(""" SELECT COUNT(*)
                FROM appointment
                WHERE appointment_status ='missed'
                """)
    missed_visits = cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointment_status = 'completed'
                """)
    completed_visits = cur.fetchone()[0]
    
    cur.execute("""SELECT COUNT(*)
                FROM appointment
                WHERE appointment_status = 'scheduled'
                """)
    scheduled_visits = cur.fetchone()[0]
    
    total_visits = missed_visits + completed_visits + scheduled_visits
    
    print("\n Visit Summary:")
    print(f"""
Total Visits    : {total_visits}
Completed Visits: {completed_visits}
Missed Visits   : {missed_visits}
Scheduled Visits: {scheduled_visits}
""")

def visit_provider(conn):

    cur= conn.cursor()
    print("Doctors:")
    cur.execute("""
                SELECT doctorid, doctorlastname
                FROM doctor 
                
                """)
    rows = cur.fetchall()
    if not rows:
        print("No Doctors Found.")
    
    else:
        for row in rows:
            print(f"""
Doctor ID  : {row[0]}
Doctor Name: {row[1]}
""")
    
        doctorid = int(input("Enter Doctor ID To View Visit Total: "))
   
        cur.execute("""
        SELECT COUNT(*)
        FROM appointment
        WHERE doctorid = ? AND appointment_status = 'completed' 
                
        """,(doctorid,))
        totalvisit = cur.fetchone()[0]
        if totalvisit >= 1:
            print(f"\n The selected doctor had {totalvisit} visit(s).")
        else:
            print("No visit found.")
    
main()
  