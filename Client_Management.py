# Import Libraires and Class
import main_util as m
import csv
import pickle
import shelve
import re

# Import Classes
import Address as adr
import main_util as m

class Client:
    clients = []#Class Variable
    def __init__(self, client_name,phone_no,mail_id,std_bill, desc,house_no,building_no,road_no,street_name,landmark,city,state,zip_code):
        self.client_id = m.generate_id('CLT_')
        self.client_name = m.validate_name(client_name)
        self.client_address = adr.Address(phone_no,mail_id,house_no,building_no,road_no,street_name,landmark,city,state,zip_code)
        #super().__init__(phone_no,mail_id, house_no, building_no, road_no, street_name, landmark, city, state, zip_code)

    @staticmethod
    def load_clients(file_name):
        Client.clients.clear()

        with open(file_name, 'r') as file:# Read data from CSV file
            reader = csv.reader(file)
            print("Reader ----------------->", reader)
            next(reader)  # Skip header row
            for row in reader:
                name,ph_no,mail,std_bill,house_no,building_no,road_no,street_name,land_mark,city,state,zip_code = row
                client_obj = Client(name,ph_no,mail,std_bill,house_no,building_no,road_no,street_name,land_mark,city,state,zip_code)
                Client.clients.append(client_obj)
        
        # Write objects to a file using shelve
        with shelve.open('client_object_shelve.db', 'c') as file:
            for client_obj in Client.clients:
                file[client_obj.client_id] = client_obj
            else:
                print("All client are created in the system successfully!")

    def create_client(self, file_name, clt_obj):
        # Create an client object
        '''client_obj = client(self.client_name, self.phone_no, self.mail_id, self.house_no, self.building_no, 
                                self.road_no, self.street_name, self.landmark, self.city, self.state, self.zip_code)'''
        try:
            with shelve.open(file_name, 'c') as file:# Store the client object in file using shelve module client_id as the key
                file[self.client_id] = clt_obj
                print(f"client {clt_obj.client_id} has been saved successfully.")
                
            return dict(file)  # Return the updated dictionary of all client stored in the shelve
        except Exception as e:
            print(f"An error occurred while saving the client: {e}")

    
    @staticmethod
    def update_client(client_id):#
        loaded_clients = []
        # Read objects from shelve file
        with shelve.open('client_object_shelve.db', 'r') as file:
            for key in file:
                client_obj = file[key]
                loaded_clients.append(client_obj)
        
        print("Length of the client ---> ", len(loaded_clients))
        if len(loaded_clients) != 0:
            client_found = False
            for clt_obj in loaded_clients:
                if clt_obj.client_id == client_id:
                    client_found = True
                    u_phone_no = input("Enter client Phone No to update: ")
                    u_mail_id = input("Enter client Mail Id to update: ")
                    u_std_bill = input("Enter client Standard Bill Rate to update: ")
                    u_house_no = input("Enter client House No to update: ")
                    u_building_no = input("Enter client Building No to update: ")
                    u_road_no = input("Enter Road No to update: ")
                    u_street_name = input("Enter Street Name to update: ")
                    u_landmark = input("Enter Land Mark to update: ")
                    u_city = input("Enter City to update: ")
                    u_state = input("Enter state: ")
                    u_zip_code = input("Enter Zip Code: ")
                    
                    # Update client object attributes
                    clt_obj.client_address.phone_no = u_phone_no
                    clt_obj.client_address.mail_id = u_mail_id
                    clt_obj.client_address.house_no= u_house_no
                    clt_obj.client_address.building_no= u_building_no
                    clt_obj.client_address.road_no = u_road_no
                    clt_obj.client_address.street_name= u_street_name
                    clt_obj.client_address.landmark= u_landmark
                    clt_obj.client_address.city = u_city
                    clt_obj.client_address.state= u_state
                    clt_obj.client_address.zip_code= u_zip_code
                    break  # Exit the loop since we found and updated the client
            
            if client_found:
                # Write updated objects back to the pickle file
                with shelve.open('client_object_shelve.db', 'c') as file:
                    for client_obj in loaded_clients:
                        file[client_obj.client_id] = client_obj
                    print(f"client with {client_id} has been updated successfully.")
            else:
                print(f"client with {client_id} not found in the system.")
        else:
            print("No More client are available in the system.")
    
    @staticmethod
    def delete_client(client_id):#EMP_551499
        # Read objects from shelve file
        with shelve.open('client_object_shelve.db', 'c') as file:
            if client_id in file:
                print("Get the client with Id : ", file[client_id])
                del file[client_id]
                print(f"client id {client_id} Successfully deleted from the system.")
            else:
                print(f"client id {client_id} does not exist in the system.")
        
    
    @staticmethod
    def search_client(client_id):
        # Read objects from shelve file
        with shelve.open('client_object_shelve.db', 'c') as file:
            if client_id in file:
                client_obj = file[client_id]
                print("\n")
                print(f"client ID: {client_obj.client_id}")
                print(f"Name: {client_obj.client_name}")
                print(f"Phone Number: {client_obj.client_address.phone_no}")
                print(f"Email: {client_obj.client_address.mail_id}")
                print(f"Address: House N: {client_obj.client_address.house_no}, Building No: {client_obj.client_address.building_no}, Road No: {client_obj.client_address.road_no}")
                print(f"City: {client_obj.client_address.city}, State: {client_obj.client_address.state}, Zip Code: {client_obj.client_address.zip_code}")
                print("-" * 40)
            else:
                print(f"No client with Id {client_id} not availabel in the system to search.")

    @staticmethod
    def get_all_client_ids():
        clients_list = []
        with shelve.open('client_object_shelve.db', 'r') as file:
            for key in file:
                clients_list.append(key)
        
        if len(clients_list) != 0:
            #print("Available client are: ", clients_list)
            return clients_list
        else:
            print("No More client are availabel to display")
            return clients_list
    
    
    @staticmethod    
    def list_client():
        
        try:
            # Read objects from pickle file
            with shelve.open('client_object_shelve.db', 'r') as file:
                for key in file:
                    client_obj = file[key]
                    print(f"client ID: {client_obj.client_id}")
                    print(f"Name: {client_obj.client_name}")
                    print(f"Phone Number: {client_obj.client_address.phone_no}")
                    print(f"Email: {client_obj.client_address.mail_id}")
                    print(f"Address: {client_obj.client_address.house_no}, {client_obj.client_address.building_no}, {client_obj.client_address.road_no}")
                    print(f"City: {client_obj.client_address.city}, State: {client_obj.client_address.state}, Zip Code: {client_obj.client_address.zip_code}")
                    print("-" * 40)
        except Exception as e:
            print(f"An error occurred while reading the client data: {e}")