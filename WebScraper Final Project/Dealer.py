
from bs4 import BeautifulSoup
import re 
import time
import requests

from Vehicle import Vehicle



class Dealer:
    def __init__(self, driver, age_status):
        self.cars = {"new": [],
                     "used": [],
                     }
        self.driver = driver
        self.age_status = age_status
        self.ford_dealer_website = "https://www.corwinfordreno.com/search{}.aspx?pn=100&pt={}"
        self.honda_dealer_website = "https://www.michaelhohlhonda.com/{}-inventory/index.htm?start={}"
        self.toyota_dealer_website = "https://www.dolanrenotoyota.com/{}-inventory/index.htm?start={}"
        
    def getFordInventory(self, soup_provided = None):
        more_pages = True 
        page_number = 1
        while more_pages:
            if soup_provided:
                soup = soup_provided 
            else:
                soup = self.getSourceHTML(self.ford_dealer_website.format(self.age_status, page_number))
            max_number_of_cars, page_max_number_of_cars = self.getCarsOnPage(soup)
            vehicles = soup.find_all("div", class_ = "vehicleDetailsColumn col-md-8 col-sm-8 pad-1x")
            for vehicle in vehicles:
                title = vehicle.find("span", class_ = "notranslate").text
                year, make, model = self.parseDeviceTitle(title)
                price = vehicle.find("span", class_ = "pull-right primaryPrice").text if vehicle.find("span", class_ = "pull-right primaryPrice") else ""
                new_vehicle = Vehicle("Corwin Ford Reno", year, make, model, price)
                new_vehicle.transmission = vehicle.find("li", class_ = "transmissionDisplay").text if vehicle.find("li", class_ = "transmissionDisplay") else ""
                new_vehicle.ext_color = vehicle.find("li", class_ = "extColor").text if vehicle.find("li", class_ = "extColor") else ""
                new_vehicle.int_color = vehicle.find("li", class_ = "intColor").text if vehicle.find("li", class_ = "intColor") else ""
                new_vehicle.vin = vehicle.find("li", class_ = "vinDisplay").text if vehicle.find("li", class_ = "vinDisplay") else ""
                self.cars[self.age_status].append(new_vehicle)
            if soup_provided:
                break
            if page_max_number_of_cars >= max_number_of_cars:
                more_pages = False
            else:
                page_number += 1
        
        return self.cars["new"] + self.cars["used"]
             

    def getHondaInventory(self, soup_provided = None):
        more_pages = True 
        page_number = 0
        while more_pages:
            if soup_provided:
                soup = soup_provided 
            else:
                soup = self.getSourceHTML(self.ford_dealer_website.format(self.age_status, page_number))
            page_max_number_of_cars = 0
            vehicles = soup.find_all("div", class_ = "vehicle-card-details-container")
            for vehicle in vehicles:
                page_max_number_of_cars += 1
                title = vehicle.find("a").getText()
                year, make, model = self.parseDeviceTitle(title)
                price = vehicle.find("span", class_ = "price-value").text
                new_vehicle = Vehicle("Michael Hohl Honda", year, make, model, price)
                new_vehicle.transmission = vehicle.find("li", class_= "transmission").text if vehicle.find("li", class_= "transmission") else ""
                new_vehicle.ext_color = vehicle.find("li", class_= "normalized-swatch-container exteriorColor").text if vehicle.find("li", class_= "normalized-swatch-container exteriorColor") else ""
                new_vehicle.int_color = vehicle.find("li", class_= "normalized-swatch-container interiorColor").text if vehicle.find("li", class_= "normalized-swatch-container interiorColor") else ""
                new_vehicle.vin = vehicle.find("li", class_= "vin").text if vehicle.find("li", class_= "vin") else ""
                self.cars[self.age_status].append(new_vehicle)
            if soup_provided:
                break
            page_number += page_max_number_of_cars

            more_pages = self.checkForMoreCars(page_number, page_max_number_of_cars)

       
        return self.cars["new"] + self.cars["used"]


        

    def getToyotaInventory(self, soup_provided = None):
        more_pages = True 
        page_number = 0
        while more_pages:
            if soup_provided:
                soup = soup_provided 
            else:
                soup = self.getSourceHTML(self.ford_dealer_website.format(self.age_status, page_number))
            page_max_number_of_cars = 0
            vehicles = soup.find_all("div", class_ = "vehicle-card-details-container")
            for vehicle in vehicles:
                page_max_number_of_cars += 1
                title = vehicle.find("a").getText() 
                year, make, model = self.parseDeviceTitle(title)
                price = vehicle.find("span", class_ = "price-value").text
                new_vehicle = Vehicle("Dolan Reno Toyota", year, make, model, price)
                new_vehicle.transmission = vehicle.find("li", class_= "transmission").text if vehicle.find("li", class_= "transmission") else ""
                new_vehicle.ext_color = vehicle.find("li", class_= "normalized-swatch-container exteriorColor").text if vehicle.find("li", class_= "normalized-swatch-container exteriorColor") else ""
                new_vehicle.int_color = vehicle.find("li", class_= "normalized-swatch-container interiorColor").text if vehicle.find("li", class_= "nnormalized-swatch-container interiorColor") else ""

                self.cars[self.age_status].append(new_vehicle)
            if soup_provided:
                break
            page_number += page_max_number_of_cars
            
            more_pages = self.checkForMoreCars(page_number, page_max_number_of_cars)
        
        return self.cars["new"] + self.cars["used"]

    def checkForMoreCars(self, page_number, max_number):
        return False if page_number >= max_number else True
            

    def getSourceHTML(self, URL):
        try:
            self.driver.get(URL)
            time.sleep(5)
            lenofpage = self.driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            for i in range(1,lenofpage//100):
                self.driver.execute_script(f"window.scrollTo(0, {i*100});")
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
        except:
            try:
                html = requests.get(URL)
                soup = BeautifulSoup(html, html.parser)
            except:
                soup = "Failed to get HTML"

        return soup

    def searchInventory(self, model):
        if self.age_status == "new":
            inventory_to_search = self.cars["new"]
        else:
            inventory_to_search = self.cars["used"]
        found_matching_vehicles = []
        for vehicle in inventory_to_search:
            if model.lower() in vehicle.model.lower():
                found_matching_vehicles.append(vehicle)
        return found_matching_vehicles

    def parseDeviceTitle(self, title):
        try:
            year = title.split(" ")[0]
            make = title.split(" ")[1]  
            model = title.replace(f"{year} {make} ", "")
            return year, make, model
        except:
            return "Title is in the incorrect format!" , None, None 

    def getCarsOnPage(self, soup):
        try:
            cars_on_page = soup.find("p", class_ = "srpVehicleCount").text
            result = re.search(r"\d - (?P<page_max_car_number>\d+) of (?P<total_cars>\d+) Vehicles", cars_on_page)
            max_number_of_cars = result.group('total_cars')
            page_max_number_of_cars = result.group("page_max_car_number") 
            return max_number_of_cars, page_max_number_of_cars
        except:
            return 0, 0


            