# Util module, common code
import random
import re

# Define regex patterns
phone_pattern = re.compile(r"(0|91)?[6-9][0-9]{9}")
name_pattern = re.compile(r'^[a-zA-Z0-9-_ ]+$')
mail_pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
house_no_pattern = re.compile(r'^[a-zA-Z0-9\s\-\/,.]+$')
land_mark_pattern = re.compile(r'^[a-zA-Z0-9\s]+$')
zip_code_pattern = re.compile(r'^\d{6}$')


def generate_id(prefix):
    return prefix+str(random.randint(100000, 999999))
    
def action_menu(action):
    print(20*" ","1. Create", action)
    print(20*" ","2. Load and Create", action)
    print(20*" ","3. List", action)
    print(20*" ","4. Update", action)
    print(20*" ","5. Delete", action)
    print(20*" ","6. Search", action)
    print(20*" ","7. Get All", action,"Ids")
    print(20*" ","8. Main Menu")
    
def validate_name(task_name):
    while True:
        if re.match(name_pattern, task_name):
            return task_name
        else:
            raise ValueError("Invalid task name. Only alphabets, digits, '-', '_', and spaces are allowed.")
    
def validate_chargeable(chargeable):
    while True:
        if chargeable.capitalize() in ['True', 'False','Yes','No']:
            chargeable = 1 if chargeable.capitalize() in ['True', 'Yes'] else 0
            return chargeable
        else:
            raise ValueError("Invalid chargeable value. Must be True/False")
    
def validate_rate_card(rate_card):
    if "." in rate_card:
        rate_card = float(rate_card)
    elif rate_card.endswith("$"):
        rate_card = rate_card[:-1]
    else:
        rate_card = int(rate_card)

    while True:
        if isinstance(rate_card, (int, float)):
            return rate_card
        elif rate_card == 0:
            return rate_card
        else:
            raise ValueError("Invalid rate card. Must be an integer or float value.")

def validate_mail_id(mail_id):
    while True:
        if re.match(mail_pattern, mail_id):
            return mail_id
        else:
            raise ValueError("Invalid Mail Id. Only alphabets, digits,'.' '_', and spaces are allowed ex: raghu.ram_123@gmail.com")

def validate_phone_number(phone_number):
    while True:
        if re.match(phone_pattern, phone_number):
            return phone_number
        else:
            raise ValueError("Invalid Phone Number. Only starts with 0 or 91 or 10 digits number starts with [9-6].")          

def validate_house_no(house_no):
    while True:
        if re.match(house_no_pattern, house_no):
            return house_no
        else:
            raise ValueError("Invalid House Number. Allowed only integer, alphabets and special characters also.")

def validate_building_number(building_number):
    while True:
        if re.match(house_no_pattern, building_number):
           return building_number
        else:
            raise ValueError("Invalid House Number. Allowed only some integer, special characters followed with any alphabets.")

def validate_road_number(road_number):
    pattern = r'^[a-zA-Z0-9\s\-\/,.]+$'
    if re.match(pattern, road_number):
        return road_number
    else:
        raise ValueError("Invalid Road Number. Allowed only some integer, special characters followed with any alphabets.")


def validate_city(city):
    while True:
        if city.isalpha():
            return city
        else:
            raise ValueError("Invalid City name. Allowed only alphabets.")


def validate_zip_code(zip_code):
    while True:
        if re.match(zip_code_pattern, zip_code):
            return zip_code
        else:
            raise ValueError("Invalid Zip Code. Allowed only 6 digits.")
