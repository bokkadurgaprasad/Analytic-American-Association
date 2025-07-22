# Import Libraires and Class

import csv
import pickle
import shelve
import re
import time

# Import Classes
import Address as adr
import main_util as m
import start as s

class Employee:
    employees = []#Class Variable
    def __init__(self, employee_name,phone_no,mail_id,std_bill,house_no,building_no,road_no,street_name,landmark,city,state,zip_code):
        self.employee_id = m.generate_id('EMP_')
        self.employee_name = m.validate_name(employee_name)
        self.std_bill = m.validate_rate_card(std_bill)
        self.employee_address = adr.Address(phone_no,mail_id,house_no,building_no,road_no,street_name,landmark,city,state,zip_code)
        #super().__init__(phone_no,mail_id, house_no, building_no, road_no, street_name, landmark, city, state, zip_code)

    @staticmethod
    def load_employees(file_name):
        Employee.employees.clear()

        with open(file_name, 'r') as file:# Read data from CSV file
            reader = csv.reader(file)
            print("Reader ----------------->", reader)
            next(reader)  # Skip header row
            for row in reader:
                name,mail,ph_no,std_bill,house_no,building_no,road_no,street_name,land_mark,city,state,zip_code = row
                employee_obj = Employee(name,ph_no,mail,std_bill,house_no,building_no,road_no,street_name,land_mark,city,state,zip_code)
                Employee.employees.append(employee_obj)
        
        # Write objects to a file using shelve
        with shelve.open('employees_object_shelve.db', 'c') as file:
            for employee_obj in Employee.employees:
                file[employee_obj.employee_id] = employee_obj
            else:
                print("All Employees are created in the system successfully!")
                
    @staticmethod
    def load_employees_db(file_name, connection):

        with open(file_name, 'r') as file:# Read data from CSV file
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                name,mail,ph_no,std_bill,house_no,building_no,road_no,street_name,land_mark,city,state,zip_code = row
                employee_obj = Employee(name,ph_no,mail,std_bill,house_no,building_no,road_no,street_name,land_mark,city,state,zip_code)
                Employee.create_employee_common(connection, employee_obj, False)
                time.sleep(1)
            print("All Employees are created in the system successfully!")
            print("\n")
            s.employee_management_db('Employee', connection)

    def create_employee(self, file_name, emp_obj):
        # Create an Employee object
        '''employee_obj = Employee(self.employee_name, self.phone_no, self.mail_id, self.house_no, self.building_no, 
                                self.road_no, self.street_name, self.landmark, self.city, self.state, self.zip_code)'''
        try:
            with shelve.open(file_name, 'c') as file:# Store the employee object in file using shelve module employee_id as the key
                file[self.employee_id] = emp_obj
                print(f"Employee {emp_obj.employee_id} has been saved successfully.")
                
                return dict(file)  # Return the updated dictionary of all employees stored in the shelve
        except Exception as e:
            print(f"An error occurred while saving the employee: {e}")
    
    def create_employee_db(self, connection, emp_obj):
        Employee.create_employee_common(connection, emp_obj, True)

    @staticmethod
    def create_employee_common(connection, emp_obj, main):
        address_sql_query = '''insert into address (
        mail_id,phone_number,house_no,
        building_number,road_number,
        street_name,land_mark,city,
        state,zip_code) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        
        data = (emp_obj.employee_address.mail_id, emp_obj.employee_address.phone_no,
        emp_obj.employee_address.house_no,emp_obj.employee_address.building_no,
        emp_obj.employee_address.road_no,emp_obj.employee_address.street_name,
        emp_obj.employee_address.land_mark,emp_obj.employee_address.city,
        emp_obj.employee_address.state,emp_obj.employee_address.zip_code)
        
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(address_sql_query,data)
        connection.commit()
        # Get the newly inserted address_id
        address_id = my_cursor.lastrowid
        
        emp_sql_query = "insert into employee (emp_id,employee_name,std_bill_rate,address_id) values (%s,%s,%s,%s)"
        emp_data = (emp_obj.employee_id,emp_obj.employee_name,emp_obj.std_bill,address_id)
        my_cursor.execute(emp_sql_query,emp_data)
        connection.commit()
        created_emp_id = my_cursor.lastrowid
        print(f"Employee Created {emp_obj.employee_id} in the system successfully.")
        print("\n")
        if main:
            press = input("Press Any Key To Continue..")
            s.employee_management_db('Employee', connection)
            
    
    @staticmethod
    def update_employee(employee_id):#EMP_852151
        '''Employee ID: EMP_852151
            Name: Arjun
            Phone Number: Arju.kanakala@gmail.com
            Email: 9290279321
            Address: 84/251/2, 776, 5
            City: Hyderabad, State: Telangana, Zip Code: 500018'''
        loaded_employees = []
        # Read objects from shelve file
        with shelve.open('employees_object_shelve.db', 'r') as file:
            for key in file:
                employee_obj = file[key]
                loaded_employees.append(employee_obj)
        
        print("Length of the employees ---> ", len(loaded_employees))
        if len(loaded_employees) != 0:
            employee_found = False
            for emp_obj in loaded_employees:
                if emp_obj.employee_id == employee_id:
                    employee_found = True
                    u_phone_no = input("Enter Employee Phone No to update: ")
                    u_mail_id = input("Enter Employee Mail Id to update: ")
                    u_std_bill = input("Enter Employee Standard Bill Rate to update: ")
                    u_house_no = input("Enter Employee House No to update: ")
                    u_building_no = input("Enter Employee Building No to update: ")
                    u_road_no = input("Enter Road No to update: ")
                    u_street_name = input("Enter Street Name to update: ")
                    u_landmark = input("Enter Land Mark to update: ")
                    u_city = input("Enter City to update: ")
                    u_state = input("Enter state: ")
                    u_zip_code = input("Enter Zip Code: ")
                    
                    # Update employee object attributes
                    emp_obj.employee_address.phone_no = u_phone_no
                    emp_obj.employee_address.mail_id = u_mail_id
                    emp_obj.employee_address.house_no= u_house_no
                    emp_obj.employee_address.building_no= u_building_no
                    emp_obj.employee_address.road_no = u_road_no
                    emp_obj.employee_address.street_name= u_street_name
                    emp_obj.employee_address.landmark= u_landmark
                    emp_obj.employee_address.city = u_city
                    emp_obj.employee_address.state= u_state
                    emp_obj.employee_address.zip_code= u_zip_code
                    break  # Exit the loop since we found and updated the employee
            
            if employee_found:
                # Write updated objects back to the pickle file
                with shelve.open('employees_object_shelve.db', 'c') as file:
                    for employee_obj in loaded_employees:
                        file[employee_obj.employee_id] = employee_obj
                    print(f"Employee with {employee_id} has been updated successfully.")
            else:
                print(f"Employee with {employee_id} not found in the system.")
        else:
            print("No More Employees are available in the system.")
            
    @staticmethod
    def update_employee_db(employee_id, connection):#EMP_852151
        '''Employee ID: EMP_852151
            Name: Arjun
            Phone Number: Arju.kanakala@gmail.com
            Email: 9290279321
            Address: 84/251/2, 776, 5
            City: Hyderabad, State: Telangana, Zip Code: 500018'''
        loaded_employees = []
        # Read objects from shelve file
        with shelve.open('employees_object_shelve.db', 'r') as file:
            for key in file:
                employee_obj = file[key]
                loaded_employees.append(employee_obj)
        
        print("Length of the employees ---> ", len(loaded_employees))
        if len(loaded_employees) != 0:
            employee_found = False
            for emp_obj in loaded_employees:
                if emp_obj.employee_id == employee_id:
                    employee_found = True
                    u_phone_no = input("Enter Employee Phone No to update: ")
                    u_mail_id = input("Enter Employee Mail Id to update: ")
                    u_std_bill = input("Enter Employee Standard Bill Rate to update: ")
                    u_house_no = input("Enter Employee House No to update: ")
                    u_building_no = input("Enter Employee Building No to update: ")
                    u_road_no = input("Enter Road No to update: ")
                    u_street_name = input("Enter Street Name to update: ")
                    u_landmark = input("Enter Land Mark to update: ")
                    u_city = input("Enter City to update: ")
                    u_state = input("Enter state: ")
                    u_zip_code = input("Enter Zip Code: ")
                    
                    # Update employee object attributes
                    emp_obj.employee_address.phone_no = u_phone_no
                    emp_obj.employee_address.mail_id = u_mail_id
                    emp_obj.employee_address.house_no= u_house_no
                    emp_obj.employee_address.building_no= u_building_no
                    emp_obj.employee_address.road_no = u_road_no
                    emp_obj.employee_address.street_name= u_street_name
                    emp_obj.employee_address.landmark= u_landmark
                    emp_obj.employee_address.city = u_city
                    emp_obj.employee_address.state= u_state
                    emp_obj.employee_address.zip_code= u_zip_code
                    break  # Exit the loop since we found and updated the employee
            
            if employee_found:
                # Write updated objects back to the pickle file
                with shelve.open('employees_object_shelve.db', 'c') as file:
                    for employee_obj in loaded_employees:
                        file[employee_obj.employee_id] = employee_obj
                    print(f"Employee with {employee_id} has been updated successfully.")
            else:
                print(f"Employee with {employee_id} not found in the system.")
        else:
            print("No More Employees are available in the system.")        
    
    
    @staticmethod
    def delete_employee(employee_id):#EMP_551499
        # Read objects from shelve file
        with shelve.open('employees_object_shelve.db', 'c') as file:
            print("Get the employee with Id : ", file[employee_id])
            if employee_id in file:
                del file[employee_id]
                print(f"Employee id {employee_id} Successfully deleted from the system.")
            else:
                print(f"Employee id {employee_id} does not exist in the system.")
    
    @staticmethod
    def delete_employee_db(employee_id, connection):
        sql_query = "select * from employee where emp_id = %s"
        data = (employee_id,)
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(sql_query, data)
        emp_count = my_cursor.rowcount
        
        if emp_count == 1:
            print(f"Employee: {employee_id} id available in the system.")
            confirmation = input(f"Are you sure, you want to delete {employee_id} [Yes/No]: ")
            if confirmation.lower() == 'yes':
                sql = 'delete from employee where emp_id = %s'
                data = (employee_id,)
                my_cursor.execute(sql,data)
                connection.commit()
                print(f"Employee: {employee_id} deleted from system successfully.")
                print("\n")
                press = input("Press Any key To Continue..")
                print("\n")
                s.employee_management_db('Employee', connection)
                #s.menu_db(connection)
        else:
            print(f"No More Employees are availabel with id {employee_id} to delete")
        
    
    @staticmethod
    def search_employee(employee_id):
        # Read objects from shelve file
        with shelve.open('employees_object_shelve.db', 'c') as file:
            if employee_id in file:
                employee_obj = file[employee_id]
                print("\n")
                print(f"Employee ID: {employee_obj.employee_id}")
                print(f"Name: {employee_obj.employee_name}")
                print(f"Phone Number: {employee_obj.employee_address.phone_no}")
                print(f"Email: {employee_obj.employee_address.mail_id}")
                print(f"Address: House N: {employee_obj.employee_address.house_no}, Building No: {employee_obj.employee_address.building_no}, Road No: {employee_obj.employee_address.road_no}")
                print(f"City: {employee_obj.employee_address.city}, State: {employee_obj.employee_address.state}, Zip Code: {employee_obj.employee_address.zip_code}")
                print("-" * 40)
            else:
                print(f"No Employee with Id {employee_id} not availabel in the system to search.")
    
    @staticmethod
    def search_employee_db(employee_id, connection):
        sql = '''SELECT e.emp_id, e.employee_name, e.std_bill_rate, 
                   a.mail_id, a.phone_number, a.house_no, 
                   a.building_number, a.road_number, a.street_name, 
                   a.land_mark, a.city, a.state, a.zip_code
                FROM employee e 
                    JOIN address a ON e.address_id = a.address_id 
                WHERE e.emp_id = %s;'''
        my_cursor = connection.cursor(buffered=True)
        data = (employee_id,)
        my_cursor.execute(sql, data)
        emp_data = my_cursor.fetchall()
        if len(emp_data) != 0:
            for emp in emp_data:
                print('Below is the Employee Information: ')
                print('\n')
                print(f"Employee ID: {emp[0]}")
                print(f"Name: {emp[1]}")
                print(f"Bill Rate: {emp[2]}")
                print(f"Email: {emp[3]}")
                print(f"Phone Number: {emp[4]}")
                print(f"Address: {emp[5]}, {emp[6]}, {emp[7]}")
                print(f"City: {emp[10]}, State: {emp[11]}, Zip Code: {emp[12]}")
                print("\n")
            s.employee_management_db('Employee', connection)
        else:
            print("\n")
            print(f"No More Tasks are availabel with id {employee_id}")
            print("\n")
            s.employee_management_db('Employee', connection)
    

    @staticmethod
    def get_all_employee_ids():
        empoyees_list = []
        with shelve.open('employees_object_shelve.db', 'r') as file:
            for key in file:
                empoyees_list.append(key)
        
        if len(empoyees_list) != 0:
            #print("Available Employees are: ", empoyees_list)
            return empoyees_list
        else:
            return empoyees_list
            print("No More Employees are availabel to display")
    
    @staticmethod
    def get_all_employee_ids_db(connection):
        sql = "select emp_id from employee;"
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(sql)
        employee_ids = [empid[0] for empid in my_cursor.fetchall()]
        print(f"All Employees ids are: \n\t\t{employee_ids}")
        print("\n")
        s.employee_management_db('Employee', connection)
    
    
    @staticmethod    
    def list_employees():
        try:
            with shelve.open('employees_object_shelve.db', 'r') as file:
                for key in file:
                    employee_obj = file[key]
                    print(f"Employee ID: {employee_obj.employee_id}")
                    print(f"Name: {employee_obj.employee_name}")
                    print(f"Phone Number: {employee_obj.employee_address.phone_no}")
                    print(f"Email: {employee_obj.employee_address.mail_id}")
                    print(f"Address: {employee_obj.employee_address.house_no}, {employee_obj.employee_address.building_no}, {employee_obj.employee_address.road_no}")
                    print(f"City: {employee_obj.employee_address.city}, State: {employee_obj.employee_address.state}, Zip Code: {employee_obj.employee_address.zip_code}")
                    print("-" * 40)
        except Exception as e:
            print(f"An error occurred while reading the employee data: {e}")
    
    
    @staticmethod    
    def list_employees_db(connection):
        '''sql = SELECT e.emp_id, e.employee_name, e.std_bill_rate, 
                   a.mail_id, a.phone_number, a.house_no, 
                   a.building_number, a.road_number, a.street_name, 
                   a.land_mark, a.city, a.state, a.zip_code
                FROM employee e 
                    JOIN address a ON e.address_id = a.address_id 
                WHERE e.emp_id = %s;'''
        
        sql = '''SELECT e.emp_id, e.employee_name, e.std_bill_rate, 
                   a.mail_id, a.phone_number, a.house_no, 
                   a.building_number, a.road_number, a.street_name, 
                   a.land_mark, a.city, a.state, a.zip_code
                FROM employee e 
                    JOIN address a ON e.address_id = a.address_id;'''
                
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(sql)
        employees_data = my_cursor.fetchall()
        #print("Data getting from database --------->", employees_data)
        try:
            if len(employees_data) !=0 :
                for employee in employees_data:
                    print(f"Employee ID: {employee[0]}")
                    print(f"Name: {employee[1]}")
                    print(f"Bill Rate: {employee[2]}")
                    print(f"Email: {employee[3]}")
                    print(f"Phone Number: {employee[4]}")
                    print(f"Address: {employee[5]}, {employee[6]}, {employee[7]}")
                    print(f"City: {employee[10]}, State: {employee[11]}, Zip Code: {employee[12]}")
                    print("-" * 40)
            else:
                print("No Tasks data found in the system")
                print("\n")
                press = input("Press Any key To Continue..")
                #s.menu_db(connection)
                s.employee_management_db('Employee', connection)
        except Exception as e:
            print(f"An error occurred while reading the employee data: {e}")