import main_util as m


class Address():
    def __init__(self,phone_no,mail_id, house_no, building_no, road_no, street_name, landmark, city, state, zip_code):
        self.phone_no = m.validate_phone_number(phone_no)
        self.mail_id = m.validate_mail_id(mail_id)
        self.house_no = m.validate_house_no(house_no)
        self.building_no = m.validate_building_number(building_no)
        self.road_no = m.validate_road_number(road_no)
        self.street_name = m.validate_name(street_name)
        self.land_mark = m.validate_name(landmark)
        self.city = m.validate_city(city)
        self.state = m.validate_name(state)
        self.zip_code = m.validate_zip_code(zip_code)