# Import Libraires and Class
import main_util as m
import csv
import pickle
import re
import start as s
import time

class TaskManager:
    tasks = []#Class Variable
    def __init__(self, task_name, chargeable, rate_card):
        self.task_id = m.generate_id('TSK_')
        self.task_name = m.validate_name(task_name)
        self.chargeable = m.validate_chargeable(chargeable)
        self.rate_card = m.validate_rate_card(rate_card)

    @staticmethod
    def load_tasks(file_name):
        TaskManager.tasks.clear()
        # Read data from CSV file
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                task_name, chargeable, rate_card = row
                task = TaskManager(task_name, chargeable, float(rate_card))
                TaskManager.tasks.append(task)
        
        # Write objects to a file using pickle
        with open('tasks_objects.pickle', 'wb') as file:
            pickle.dump(TaskManager.tasks, file)
    
    @staticmethod
    def load_tasks_db(file_name, connection):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                task_name, chargeable, rate_card = row
                task_obj = TaskManager(task_name, chargeable, rate_card)
                TaskManager.create_task_db(task_obj,connection, False)
                time.sleep(1)
            s.task_management_db('Task', connection)
    @staticmethod
    def create_task(task_name, chargeable, rate_card):
        TaskManager.tasks.clear()
        task = TaskManager(task_name, chargeable, float(rate_card))
        TaskManager.tasks.append(task)
        
        with open('tasks_objects.pickle', 'ab') as file:
            pickle.dump(TaskManager.tasks, file)
            
    @staticmethod
    def create_task_db(task_obj, connection, main):
        '''sql_query = 'select * from tasks where task_name = %s'
        my_cursor = conn.cursor(buffered=True)
        data = (task_name,)
        
        # Execute the sql query
        my_cursor.execute(sql_query, data)'''

        my_cursor = connection.cursor(buffered=True)
        data = (task_obj.task_id, task_obj.task_name, task_obj.chargeable, task_obj.rate_card)
        print("Task Object Data is ", data)
        sql = "insert into tasks (task_id,task_name,chargable,rate_card) values (%s,%s,%s,%s)"
        my_cursor.execute(sql, data)
        connection.commit()
        print("Task Created in the system to successfully.")
        print("\n")
        if main:
            press = input("Press Any Key To Continue..")
            #s.menu_db(connection)
            s.task_management_db('Task', connection)
        
            
    
    @staticmethod
    def update_task(task_id):#TSK_196779
        loaded_tasks = []
        # Read objects from pickle file
        with open('tasks_objects.pickle', 'rb') as file:
            loaded_tasks = pickle.load(file)
            '''for task_obj in loaded_tasks:
                task_list.append(task_obj.task_id)'''
        
        if len(loaded_tasks) != 0:
            task_found = False
            for task_obj in loaded_tasks:
                if task_obj.task_id == task_id:
                    print("Task Id, Name,Charg, Rate Card", task_obj.task_id, task_obj.task_name, task_obj.chargeable, task_obj.rate_card)
                    task_found = True
                    u_task_name = input("Enter task name to update : ")                      
                    u_chargeable = m.validate_chargeable(input("Is task chargiable? : "))
                    u_rate_card = None
                    if u_chargeable in ['True', 'Yes']:
                        u_rate_card = m.validate_rate_card(int(input("Enter Task Rate : ")))
                    elif u_chargeable in ['False', 'No']:
                        u_rate_card = float(0)
                    
                    # Update task object attributes
                    task_obj.task_name = u_task_name
                    task_obj.chargeable = u_chargeable
                    task_obj.rate_card = u_rate_card
                    #task_obj.save()
                    break  # Exit the loop since we found and updated the task
            
            if task_found:
                # Write updated objects back to the pickle file
                with open('tasks_objects.pickle', 'wb') as file:
                    pickle.dump(loaded_tasks, file)
                    print(f"Task {task_id} has been updated successfully.")
            else:
                print(f"Task {task_id} not found in the system.")
        else:
            print("No More Tasks are available in the system.")
            
        #Testing code to verify object cahnged or not    
        '''for task_obj in loaded_tasks:
                if task_obj.task_id == task_id:
                    print("Task Id, Name, Chargeable, Rate Card", task_obj.task_id, task_obj.task_name, task_obj.chargeable, task_obj.rate_card)'''
    
    @staticmethod
    def update_task_db(task_id, connection):#TSK_291283
        sql = "select * from tasks where task_id = %s"
        my_cursor = connection.cursor(buffered=True)
        data = (task_id,)
        my_cursor.execute(sql, data)
        task_data = my_cursor.rowcount
        
        if task_data == 1:
            print(f"Found Task: {task_id}, please enter required fields to update.")
            u_task_name = input("Enter task name to update : ")
            u_chargeable = m.validate_chargeable(input("Is task chargiable? : "))
            u_rate_card = 0
            if u_chargeable:
                u_rate_card = m.validate_rate_card(input("Enter Task Rate : "))
                
            sql_query = 'UPDATE tasks SET task_name = %s,chargable = %s,rate_card = %s WHERE task_id = %s;'
            data = (u_task_name,u_chargeable,u_rate_card, task_id)
            my_cursor.execute(sql_query, data)
            connection.commit()
            print(f"Updated Task: {task_id} into Records")
            press = input("Press Any Key To Continue..")
            #s.menu_db(connection)
            s.task_management_db('Task', connection)
        else:
            print(f"No More Tasks are available with task: {task_id} in the system.")
    
    
    @staticmethod
    def delete_task(task_id):
        loaded_tasks = []
        # Read objects from pickle file
        with open('tasks_objects.pickle', 'rb') as file:
            loaded_tasks = pickle.load(file)
        
        total_tasks_size = len(loaded_tasks)
        print("Size of the list ", len(loaded_tasks))
        if len(loaded_tasks) != 0:
            '''updated_tasks = [task for task in loaded_tasks if task.task_id != task_id]
            if len(updated_tasks) < len(loaded_tasks):
                
                # Task was found and removed, write back the updated list to the file
                with open('tasks_objects.pickle', 'wb') as file:
                    pickle.dump(updated_tasks, file)
                print(f"Task {task_id} has been deleted successfully.")
            else:
                print(f"Task {task_id} not found in the system.")'''
            
            for task in loaded_tasks:
                if task.task_id == task_id:
                    loaded_tasks.remove(task)
                    print(f"Task with Id: {task_id} has been deleted successfully.")
                else:
                    print(f"Task Id: {task_id} not found in the system.")
            
            if len(loaded_tasks) < total_tasks_size:
                print("Size of the list ", len(loaded_tasks))
                with open('tasks_objects.pickle', 'wb') as file:
                    pickle.dump(loaded_tasks, file)
            else:
                print(f"Task id: {task_id} not found in the system.")
        else:
            print("No More Tasks are availabel to delete")
    
    @staticmethod
    def delete_task_db(task_id, connection):
        sql_query = "select * from tasks where task_id = %s"
        data = (task_id,)
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(sql_query, data)
        task_count = my_cursor.rowcount
        
        if task_count == 1:
            print(f"Task: {task_id} id available in the system.")
            confirmation = input("Are you sure, you want to delete {task_id} [Yes/No]: ")
            if confirmation.lower() == 'yes':
                sql = 'delete from tasks where task_id = %s'
                data = (task_id,)
                my_cursor.execute(sql,data)
                connection.commit()
                print(f"Task: {task_id} deleted from system successfully.")
                print("\n")
                press = input("Press Any key To Continue..")
                s.task_management_db('Task', connection)
                #s.menu_db(connection)
        else:
            print(f"No More Tasks are availabel with id {task_id} to delete")
    
    
    @staticmethod
    def search_task(task_id):
        loaded_tasks = []
        # Read objects from pickle file
        with open('tasks_objects.pickle', 'rb') as file:
            loaded_tasks = pickle.load(file)
        
        if len(loaded_tasks) != 0:
            for task in loaded_tasks:
                if task.task_id == task_id:
                    print('\n')
                    print('Below is the Task Information: ')
                    print('Task Id: ', task.task_id)
                    print('Task Name: ', task.task_name)
                    print('Is Task Chargeable: ', task.chargeable)
                    print(f'Task Rate Card: {task.rate_card}$')
        else:
            print("No More Tasks are availabel to delete")
            
    @staticmethod
    def search_task_db(task_id, connection):
        sql_query = "select * from tasks where task_id = %s"
        data = (task_id,)
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(sql_query,data)
        task_data = my_cursor.fetchall()
        
        if len(task_data) != 0:
            for task in task_data:
                print('Below is the Task Information: ')
                print('\n')
                print('Task Id: ', task[0])
                print('Task Name: ', task[1])
                print('Is Task Chargeable: ', task[2])
                print(f'Task Rate Card: {task[3]}$')
            s.task_management_db('Task', connection)
        else:
            print("\n")
            print(f"No More Tasks are availabel with id {task_id}")
            

    @staticmethod
    def get_all_task_ids():
        task_list = []
        # Read objects from pickle file
        with open('tasks_objects.pickle', 'rb') as file:
            loaded_tasks = pickle.load(file)
            for i in loaded_tasks:
                task_list.append(i.task_id)
        
        if len(task_list) != 0:
            #print("Available Tasks are: ", task_list)
            return task_list
        else:
            print("No More Tasks are availabel to display")
            return task_list
    
    @staticmethod
    def get_all_task_ids_db(connection):
        sql_query = "select task_id from tasks;"
        my_cursor = connection.cursor(buffered=True)
        my_cursor.execute(sql_query)
        task_ids = [tid[0] for tid in my_cursor.fetchall()]
        print(f"All the task ids available in the system:\n\t{task_ids}")
        print("\n")
        s.task_management_db('Task', connection)
    
    @staticmethod    
    def list_tasks():
        loaded_tasks = []
        # Read objects from pickle file
        with open('tasks_objects.pickle', 'rb') as file:
            loaded_tasks = pickle.load(file)
            
        for task_obj in loaded_tasks:
            print("Task Id: ", task_obj.task_id)
            print("Task Name: ", task_obj.task_name)
            print("Task Chargeable: ", task_obj.chargeable)
            print(f"Task Rate Card: {task_obj.rate_card}$", )
            print("-" * 40)
            
    
    @staticmethod    
    def list_tasks_db(connection):
        # Read objects from Database
        sql = "select * from tasks;"
        my_cursor = connection.cursor()
        my_cursor.execute(sql) 
        tasks_data = my_cursor.fetchall()
        if len(tasks_data) !=0 :
            for task_obj in tasks_data:
                print("Task Id: ", task_obj[0])
                print("Task Name: ", task_obj[1])
                print("Task Chargeable: ", task_obj[2])
                print(f"Task Rate Card: {task_obj[3]}$", )
                print("-" * 40)
            s.task_management_db('Task', connection)
        else:
            print("No Tasks data found in the system")
            print("\n")
            press = input("Press Any key To Continue..")
            #s.menu_db(connection)
            s.task_management_db('Task', connection)