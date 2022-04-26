
from bs4 import BeautifulSoup
import unittest 

from WebScraper import *
from Vehicle import Vehicle
import socket

class TestWebScraperUnitTest(unittest.TestCase):

    def setUp(self):
        self.driver = ""

    def setUpIntegration(self, active = True):
        # if active:
        #     self.driver = setupWebDriver()
        # else:
        #     self.driver = ""
        self.driver = ""
        self.new_dealer = Dealer(self.driver, "new")
        self.new_vehicle = Vehicle("test dealer", "2000", "Honda", "Civic", "$10000")

    def testWebDriverFail(self):
        def guard(*args, **kwargs):
            raise Exception("No sockets available")
        test = socket.socket
        socket.socket = guard 
        actual = setupWebDriver()
        expected = "Error setting up Web Driver"
        self.assertEqual(actual, expected)
        socket.socket = test

   # def testWebDriverPass(self):
   #     actual = setupWebDriver()
   #     expected = webdriver.chrome.webdriver.WebDriver
   #     self.assertEqual(type(actual), expected)
        
    def testSearchSoupTrue(self):
        self.setUpIntegration(active = False)
        html = '<span class="notranslate">2022 GMC Acadia Denali</span>'
        new_vehicle = Vehicle("test delear", "2000", "Honda", "Civic", "$10000")
        soup = BeautifulSoup(html, "html.parser")
        self.assertTrue(new_vehicle.searchSoup(soup, "span", "notranslate")) 

    def testSearchSoupFalse(self):
        self.setUpIntegration(active = False)
        html = '<span class="notranslate">2022 GMC Acadia Denali</span>'
        new_vehicle = Vehicle("test delear", "2000", "Honda", "Civic", "$10000")
        soup = BeautifulSoup(html, "html.parser")
        self.assertFalse(new_vehicle.searchSoup(soup, "div", "notranslate"))

    def testParseDeviceTitlePass(self):
        title = "2022 GMC Acadia Denali"
        self.setUpIntegration(active = False)
        year,make,model = self.new_dealer.parseDeviceTitle(title)
        self.assertTrue(year == "2022" and make == "GMC" and model == "Acadia Denali")

    def testParseDeviceTitleBadFormat(self):
        title = "2022GMCAcadiaDenali"
        self.setUpIntegration(active = False)
        year,make,model = self.new_dealer.parseDeviceTitle(title)
        self.assertEqual(year, "Title is in the incorrect format!")

    def testGetSourceHTML(self):
        self.setUpIntegration(active = False)
        soup = self.new_dealer.getSourceHTML("https://www.yahoo.com")
        self.assertTrue(soup)

    def testGetSourceHTMLFail(self):
        self.setUpIntegration( active= False)
        soup = self.new_dealer.getSourceHTML("http://badurltest.lkj")
        self.assertEqual("Failed to get HTML", soup)

    def testVehicleOutput(self):
        new_vehicle = Vehicle("test dealer", "2000", "Honda", "Civic", "$10000")
        new_vehicle.transmission = "Transmission: test_tran"
        expected = "\nDealer: test dealer\nYear: 2000\nMake: Honda\nModel: Civic\nPrice: $10000\nTransmission: test_tran\n"
        self.assertEqual(str(expected), str(new_vehicle))

    def testSearchInventoryTrue(self):
        self.setUpIntegration(active = False)
        self.new_dealer.cars["new"].append(self.new_vehicle)
        actual = self.new_dealer.searchInventory("civic")
        expected = [self.new_vehicle]
        self.assertEqual(actual, expected)

    def testSearchInventoryFalse(self):
        self.setUpIntegration(active = False)
        self.new_dealer.age_status = "used"
        self.new_dealer.cars["used"].append(self.new_vehicle)
        actual = self.new_dealer.searchInventory("tacoma")
        expected = []
        
        self.assertEqual(actual, expected)

    def testGetCarsOnPage(self):
        self.setUpIntegration(active = False)
        html = '<p class="srpVehicleCount">(1 - 100 of 324 Vehicles)</p>'
        soup = BeautifulSoup(html, "html.parser")
        max_number_of_cars, page_max_number_of_cars = self.new_dealer.getCarsOnPage(soup)
        self.assertTrue(max_number_of_cars == "324" and page_max_number_of_cars == "100")

    def testGetCarsOnPageBadFormat(self):
        self.setUpIntegration(active = False)
        html = '<p class="srpVehicleCount">(1 - 100)</p>'
        soup = BeautifulSoup(html, "html.parser")
        max_number_of_cars, page_max_number_of_cars = self.new_dealer.getCarsOnPage(soup)
        self.assertTrue(max_number_of_cars == 0 and page_max_number_of_cars == 0)

    def testCheckForMoreCarsTrue(self):
        self.setUpIntegration(active = False)
        max_number = 100
        page_number = 50
        self.assertTrue(self.new_dealer.checkForMoreCars(page_number, max_number))

    def testCheckForMoreCarsFalse(self):
        self.setUpIntegration(active = False)
        max_number = 100
        page_number = 150
        self.assertFalse(self.new_dealer.checkForMoreCars(page_number, max_number))
        
if __name__ == "__main__":
    unittest.main()

