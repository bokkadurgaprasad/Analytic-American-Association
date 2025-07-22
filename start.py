# Import required Libraries
import mysql.connector
import re
import datetime

#Import classes
import main_util as m
import Task_Management as taskm
import Employee_Management as emp
import Client_Management as clt
import Time_Sheet_Management as tms

# Input Files
task_file_name = 'tasks.csv'
employee_file = 'Employee.csv'
client_file = 'Clients.csv'

def task_management(name):
    m.action_menu(name)
    task_choice = int(input("Enter your choice: "))
    if task_choice == 1:
        task_name = input("Enter task name: ")
        task_chargeable = input("Task Chargiable? ")
        task_rate_card = input("Enter Task Rate: ")
        taskm.TaskManager.create_task(task_name, task_chargeable, task_rate_card)
    elif task_choice == 2:
        taskm.TaskManager.load_tasks(task_file_name)
    elif task_choice == 3:
        taskm.TaskManager.list_tasks()
    elif task_choice == 4:
        task_id = input("Enter Task Id: ")
        taskm.TaskManager.update_task(task_id)
    elif task_choice == 5:
        task_id = input("Enter Task Id: ")
        taskm.TaskManager.delete_task(task_id)
    elif task_choice == 6:
        task_id = input("Enter Task Id: ")
        taskm.TaskManager.search_task(task_id)
    elif task_choice == 7:
        taskm.TaskManager.get_all_task_ids()
    else:
        exit(0)
        
def task_management_db(name, connection):
    m.action_menu(name)
    task_choice = int(input("Enter your choice: "))
    if task_choice == 1:
        task_name = input("Enter task name: ")
        task_chargeable = input("Task Chargiable? : ")
        task_rate_card = input("Enter Task Rate: ")
        task_obj = taskm.TaskManager(task_name, task_chargeable, task_rate_card)
        taskm.TaskManager.create_task_db(task_obj,connection, True)
    elif task_choice == 2:
        taskm.TaskManager.load_tasks_db(task_file_name, connection)
    elif task_choice == 3:
        taskm.TaskManager.list_tasks_db(connection)
    elif task_choice == 4:
        task_id = input("Enter Task Id: ")
        taskm.TaskManager.update_task_db(task_id, connection)
    elif task_choice == 5:
        task_id = input("Enter Task Id: ")
        taskm.TaskManager.delete_task_db(task_id, connection)
    elif task_choice == 6:
        task_id = input("Enter Task Id: ")
        taskm.TaskManager.search_task_db(task_id, connection)
    elif task_choice == 7:
        taskm.TaskManager.get_all_task_ids_db(connection)
    elif task_choice == 8:
        #exit(0)
        menu_db(connection)
    else:
        exit(0)

def client_management(name):
    m.action_menu(name)
    client_choice = int(input("Enter your choice: "))
    if client_choice == 1:#Create Client
        client_name = input("Enter Employee name: ")
        print("Note:Description should not exceeded more than 1000 characters")
        client_description = input("Enter Description: ")
        phone_no = input("Enter Employee Phone No: ")
        mail_id = input("Enter Employee Mail Id: ")
        std_bill = input("Enter Employee Standard Bill Rate: ")
        house_no = input("Enter Employee House No: ")
        building_no = input("Enter Employee Building No: ")
        road_no = input("Enter Road No: ")
        street_name = input("Enter Street Name: ")
        landmark = input("Enter Land Mark: ")
        city = input("Enter City: ")
        state = input("Enter state: ")
        zip_code = input("Enter Zip Code: ")
        clt_obj = clt.Client(client_name, phone_no, mail_id, std_bill,client_description, house_no, building_no, road_no, street_name, landmark, city, state, zip_code)
        clt_obj.create_client('employees_object_shelve.db', clt_obj)
    elif client_choice == 2:#Load Clients
        clt.Client.load_clients(client_file)
    elif client_choice == 3:#List Available Clients
        clt.Client.list_client()
    elif client_choice == 4:
        client_id = input("Enter Employee Id: ")
        clt.Client.update_client(client_id)
    elif client_choice == 5:
        client_id = input("Enter Employee Id: ")
        clt.Client.delete_client(client_id)
    elif client_choice == 6:
        client_id = input("Enter Employee Id: ")
        clt.Client.search_client(client_id)
    else:
        exit(0)
        
def employee_management(name):
    m.action_menu(name)
    employee_choice = int(input("Enter your choice: "))
    if employee_choice == 1:
        '''employee_name, phone_no, mail_id, house_no, building_no, road_no, street_name, landmark, city, state, zip_code = emp_obj.employee_inputs'''
        employee_name = input("Enter Employee name: ")
        phone_no = input("Enter Employee Phone No: ")
        mail_id = input("Enter Employee Mail Id: ")
        std_bill = input("Enter Employee Standard Bill Rate: ")
        house_no = input("Enter Employee House No: ")
        building_no = input("Enter Employee Building No: ")
        road_no = input("Enter Road No: ")
        street_name = input("Enter Street Name: ")
        landmark = input("Enter Land Mark: ")
        city = input("Enter City: ")
        state = input("Enter state: ")
        zip_code = input("Enter Zip Code: ")
        emp_obj = emp.Employee(employee_name, phone_no, mail_id, std_bill, house_no, building_no, road_no, street_name, landmark, city, state, zip_code)
        emp_obj.create_employee('employees_object_shelve.db', emp_obj)
    elif employee_choice == 2:
        emp.Employee.load_employees_db(employee_file, connection)
    elif employee_choice == 3:
        #employee_id = input("Enter Employee Id: ")
        emp.Employee.list_employees()
    elif employee_choice == 4:
        employee_id = input("Enter Employee Id: ")
        emp.Employee.update_employee(employee_id)
    elif employee_choice == 5:
        employee_id = input("Enter Employee Id: ")
        emp.Employee.delete_employee(employee_id)
    elif employee_choice == 6:
        employee_id = input("Enter Employee Id: ")
        emp.Employee.search_employee(employee_id)
    elif employee_choice == 7:
        print("{:>50}".format("-->> Thank You Visit Again! <<--"))
        exit(0)
    else:
        print("{:>50}".format("Invalid Input, please enter valid choice."))
        
def employee_management_db(name, connection):
    m.action_menu(name)
    employee_choice = int(input("Enter your choice: "))
    if employee_choice == 1:
        employee_name = input("Enter Employee name: ")
        phone_no = input("Enter Employee Phone No: ")
        mail_id = input("Enter Employee Mail Id: ")
        std_bill = input("Enter Employee Standard Bill Rate: ")
        house_no = input("Enter Employee House No: ")
        building_no = input("Enter Employee Building No: ")
        road_no = input("Enter Road No: ")
        street_name = input("Enter Street Name: ")
        landmark = input("Enter Land Mark: ")
        city = input("Enter City: ")
        state = input("Enter state: ")
        zip_code = input("Enter Zip Code: ")
        emp_obj = emp.Employee(employee_name, phone_no, mail_id, std_bill, house_no, building_no, road_no, street_name, landmark, city, state, zip_code)
        emp_obj.create_employee_db(connection, emp_obj)
    elif employee_choice == 2:
        emp.Employee.load_employees_db(employee_file, connection)
    elif employee_choice == 3:
        #employee_id = input("Enter Employee Id: ")
        emp.Employee.list_employees_db(connection)
    elif employee_choice == 4:
        employee_id = input("Enter Employee Id: ")
        emp.Employee.update_employee(employee_id)
    elif employee_choice == 5:
        employee_id = input("Enter Employee Id: ")
        emp.Employee.delete_employee_db(employee_id, connection)
    elif employee_choice == 6:
        employee_id = input("Enter Employee Id: ")
        emp.Employee.search_employee_db(employee_id, connection)
    elif employee_choice == 7:
        emp.Employee.get_all_employee_ids_db(connection)
    elif employee_choice == 8:
        '''print("{:>50}".format("-->> Thank You Visit Again! <<--"))
        exit(0)'''
        menu_db(connection)
    else:
        print("{:>50}".format("Invalid Input, please enter valid choice."))
        

def time_sheet_management(name):
    m.action_menu(name)
    time_sheet_choice = int(input("Enter your choice: "))
    if time_sheet_choice == 1:
        time_sheet_date = tms.TimeSheet.validate_time_sheet_date()
        employee_id = tms.TimeSheet.validate_employee_id()
        client_id = tms.TimeSheet.validate_client_id()
        task_id = tms.TimeSheet.validate_task_id()
        hours = tms.TimeSheet.validate_hours()
        tms_obj = tms.TimeSheet(time_sheet_date, employee_id, client_id, task_id, hours)
        tms_obj.create_time_sheet('time_sheet_objects_shelve.db', tms_obj)
    elif time_sheet_choice == 2:
        tms.list_time_sheets()
    elif time_sheet_choice == 3:
        tms.TimeSheet.list_time_sheet()
    elif time_sheet_choice == 5:
        time_sheet_date = tms.TimeSheet.validate_time_sheet_date()
        tms.TimeSheet.delete_time_sheet(time_sheet_date)
    elif time_sheet_choice == 6:
        time_sheet_date = tms.TimeSheet.validate_time_sheet_date()
        tms.TimeSheet.search_time_sheet(time_sheet_date)
    else:
        exit(0)
        
def admin():
    #m.action_menu(name)
    print(20*" ","1. Get All Task Ids")
    print(20*" ","2. Get All Employee Ids")
    print(20*" ","3. Get All Client Ids")
    print(20*" ","4. Get All Time Sheet Ids")
    admin_choice = int(input("Enter your choice: "))
    if admin_choice == 1:
        taskm.TaskManager.get_all_task_ids_db()
    elif admin_choice == 2:
        emp.Employee.get_all_employee_ids()
    elif admin_choice == 3:
        clt.Client.get_all_client_ids()
    elif admin_choice == 4:
        all_time_sheets = tms.TimeSheet.get_all_time_sheet_ids()
        print("All Available Time Sheets: ", all_time_sheets)

def admin_db():
    #m.action_menu(name)
    print(20*" ","1. Get All Task Ids")
    print(20*" ","2. Get All Employee Ids")
    print(20*" ","3. Get All Client Ids")
    print(20*" ","4. Get All Time Sheet Ids")
    admin_choice = int(input("Enter your choice: "))
    if admin_choice == 1:
        taskm.TaskManager.get_all_task_ids_db()
    elif admin_choice == 2:
        emp.Employee.get_all_employee_ids()
    elif admin_choice == 3:
        clt.Client.get_all_client_ids()
    elif admin_choice == 4:
        all_time_sheets = tms.TimeSheet.get_all_time_sheet_ids()
        print("All Available Time Sheets: ", all_time_sheets)
    
        
def show_menu():
    print(20*" ","1. Task")
    print(20*" ","2. Employee")
    print(20*" ","3. Client")
    print(20*" ","4. Time Sheet")
    print(20*" ","5. Admin")
    print(20*" ","6. Exit")

def menu():
    #task_obj = taskm.TaskManager()
    #emp_obj = empm.Employee()
    while True:
        print("\n")
        show_menu()
        user_choice = int(input("Enter your choice: "))
        #get the choice
        if user_choice == 1:
            task_management('Task')
        elif user_choice == 2:
            employee_management('Employee')
        elif user_choice == 3:
            client_management("Client")
        elif user_choice == 4:
            time_sheet_management("Time Sheet")
        elif user_choice == 5:
            admin()
        elif user_choice == 6:
            print("{:>50}".format("-->> Thank You Visit Again! <<--"))
            exit(0)


def menu_db(connection):
    #task_obj = taskm.TaskManager()
    #emp_obj = empm.Employee()
    while True:
        print("\n")
        # Initialize shopping cart
        show_menu()
        user_choice = int(input("Enter your choice: "))
        #get the choice
        if user_choice == 1:
            task_management_db('Task', connection)
        elif user_choice == 2:
            employee_management_db('Employee', connection)
        elif user_choice == 3:
            client_management("Client")
        elif user_choice == 4:
            time_sheet_management("Time Sheet")
        elif user_choice == 5:
            admin_db()
        elif user_choice == 6:
            print("{:>50}".format("-->> Thank You Visit Again! <<--"))
            exit(0)            

if __name__ == '__main__':
    #main()
    
    connection = None
    try:
        connection = mysql.connector.connect(host = "localhost", user = 'root', password = 'prasad21', database = "american_analytics")
    except:
        print("Please check the User Name and Password.....")
        exit(0)
    print("{:>45}".format("-->> Welcome <<--"))
    menu_db(connection)