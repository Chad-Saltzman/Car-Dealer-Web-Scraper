class Vehicle:
    def __init__(self, dealer, year, make, model, price):
        self.dealer = dealer 
        self.year = year 
        self.make = make 
        self.model = model 
        self.price = price
        self.body_style = ""
        self.model_code = ""
        self.engine = ""
        self.drive_type = ""
        self.transmission = ""
        self.ext_color = ""
        self.int_color = ""
        self.vin = ""

    def searchSoup(self, soup, tag, value):
        test = soup.find(tag, class_ = value)
        return test

    def __repr__(self):
        vehicle_string = "\n"

        vehicle_string += f"Dealer: {self.dealer}\n"
        vehicle_string += f"Year: {self.year}\n"
        vehicle_string += f"Make: {self.make}\n"
        vehicle_string += f"Model: {self.model}\n"
        vehicle_string += f"Price: {self.price}\n"
        vehicle_string += f"{self.body_style}\n" if self.body_style else ""
        vehicle_string += f"{self.model_code}\n" if self.model_code else ""
        vehicle_string += f"{self.engine}\n" if self.engine else ""
        vehicle_string += f"{self.drive_type}\n" if self.drive_type else ""
        vehicle_string += f"{self.transmission}\n" if self.transmission else ""
        vehicle_string += f"{self.ext_color}\n" if self.ext_color else ""
        vehicle_string += f"{self.int_color}\n" if self.int_color else ""
        vehicle_string += f"{self.vin}\n" if self.vin else ""

        return vehicle_string
