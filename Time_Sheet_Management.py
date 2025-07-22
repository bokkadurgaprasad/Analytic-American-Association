# Import Libraires and Class
import main_util as m
import pickle
import shelve
import random
import re
import os

# Import Classes
import Address as adr
import main_util as m
import Employee_Management as emp
import Client_Management as clt
import Task_Management as taskm

# Initiations
time_sheet_date_pattern = re.compile(r'^\d{4}/\d{2}/\d{2}$')

class TimeSheet:
    time_sheets = []#Class Variable
    def __init__(self, timesheet_date, employee_id, client_id, task_id, hours):
    #def __init__(self):
        self.timesheet_id = m.generate_id('TMS_')
        self.timesheet_date = timesheet_date
        self.employee_id = employee_id
        self.client_id = client_id
        self.task_id = task_id
        self.hours = hours

    @staticmethod
    def validate_time_sheet_date():
        while True:
            timesheet_date = input("Enter Time Sheet Date : ")
            if re.match(time_sheet_date_pattern, timesheet_date):
                return timesheet_date
            else:
                print("Invalid date format. Use yyyy/MM/dd format.")
    
    @classmethod
    def validate_client_id(cls):
        client_list = clt.Client.get_all_client_ids()
        while True:
            client_id = input("Enter Client Id : ")
            if client_id in client_list:
                return client_id
            else:
                print(f"Client Id {client_id} not available in system.")
    
    @classmethod    
    def validate_employee_id(cls):
        emp_list = emp.Employee.get_all_employee_ids()
        while True:
            employee_id = input("Enter Employee Id : ")
            if employee_id in emp_list:
                return employee_id
            else:
                print(f"Employee Id {employee_id} not available in system.")
    @classmethod
    def validate_task_id(cls):
        task_list = taskm.TaskManager.get_all_task_ids()
        while True:
            task_id = input("Enter Task Id : ")
            if task_id in task_list:
                return task_id
            else:
                print(f"Task Id {task_id} not available in system.")
    
    @staticmethod
    def validate_hours():
        while True:
            try:
                hours = int(input("Enter Number of hours : "))
                
                if isinstance(hours, (int, float)) and 1 <= hours <= 8:
                    return hours
                else:
                    print("Hours must be a number between 0 and 8.")
            except:
                print("Hours must be a integer number or float number between 1 to 8 only.")
    
    def create_time_sheet(self, file_name, tms_obj):
        try:
            with shelve.open(file_name, 'c') as file:
                file[self.timesheet_date] = tms_obj
                print(f"Time Sheet Date {tms_obj.timesheet_date} has been saved successfully.")
                return dict(file)
        except Exception as e:
            print(f"An error occurred while saving the employee: {e}")

    @staticmethod
    def delete_time_sheet(time_sheet_date):
        # Read objects from shelve file
        with shelve.open('time_sheet_objects_shelve.db', 'c') as file:
            if time_sheet_date in file:
                del file[time_sheet_date]
                print(f"Time Sheet date {time_sheet_date} Successfully deleted from the system.")
            else:
                print(f"Time Sheet date {time_sheet_date} does not exist in the system.")
    
    @staticmethod
    def search_time_sheet(time_sheet_date):
        with shelve.open('time_sheet_objects_shelve.db', 'c') as file:
            if time_sheet_date in file:
                time_sheet_obj = file[time_sheet_date]
                print("\n")
                print(f"Time Sheet ID: {time_sheet_obj.timesheet_date}")
                print(f"Time Sheet Date: {time_sheet_obj.employee_id}")
                print(f"Employee Id: {time_sheet_obj.employee_id}")
                print(f"Client Id: {time_sheet_obj.client_id}")
                print(f"Task _d: House N: {time_sheet_obj.task_id}")
                print(f"Hours: {time_sheet_obj.hours}")
                print("-" * 40)
            else:
                print("No More Time Sheets are availabel to search")

    @staticmethod
    def get_all_time_sheet_ids():
        time_sheet_list = []
        with shelve.open('time_sheet_objects_shelve.db', 'r') as file:
            for key in file:
                time_sheet_list.append(key)
        #print("Time Sheets Object are ---->", time_sheet_list)
        if len(time_sheet_list) != 0:
            return time_sheet_list
        else:
            return time_sheet_list
            print("No More time sheets are availabel to display")
    
    
    @staticmethod    
    def list_time_sheet():
        try:
            with shelve.open('time_sheet_objects_shelve.db', 'r') as file:
                for key in file:
                    time_sheet_obj = file[key]
                    print("\n")
                    print(f"Time Sheet ID: {time_sheet_obj.timesheet_date}")
                    print(f"Time Sheet Date: {time_sheet_obj.employee_id}")
                    print(f"Employee Id: {time_sheet_obj.employee_id}")
                    print(f"Client Id: {time_sheet_obj.client_id}")
                    print(f"Task _d: House N: {time_sheet_obj.task_id}")
                    print(f"Hours: {time_sheet_obj.hours}")
                    print("-" * 40)
        except Exception as e:
            print(f"An error occurred while reading the Time Sheet data: {e}")