
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

    def testGetFordInventory(self):
        self.setUpIntegration(active = False)
        html = """<div class="vehicleDetailsColumn col-md-8 col-sm-8 pad-1x">
                  <span class="notranslate">2022 Ford Explorer ST In-Transit</span>
                  <span style="font-weight:bold;font-size:1.4em;" class="pull-right primaryPrice">$64,900</span>
                  <li class="transmissionDisplay"><strong>Transmission: </strong>10-Speed Automatic</li>
                  <li class="extColor"><strong>Ext. Color: </strong>Forged Green Metallic</li>
                  <li class="intColor"><strong>Int. Color: </strong>Seating Surfaces Ebony Interior</li>
                  <li class="vinDisplay"><strong>VIN #: </strong><span>1FM5K8GC3NGA03189</span></li>
                  </div>"""

        soup = BeautifulSoup(html, "html.parser")
        actual = self.new_dealer.getFordInventory(soup)
        expected = "[\nDealer: Corwin Ford Reno\nYear: 2022\nMake: Ford\nModel: Explorer ST In-Transit\nPrice: $64,900\nTransmission: 10-Speed Automatic\nExt. Color: Forged Green Metallic\nInt. Color: Seating Surfaces Ebony Interior\nVIN #: 1FM5K8GC3NGA03189\n]"
        self.assertEqual(str(actual), expected)

    def testGetHondaInventory(self):
        self.setUpIntegration(active = False)
        html = """<span class="d-none d-sm-inline">230 Vehicles</span>
                  <div class="vehicle-card-details-container">
                  <span class="price-value" data-style-editor-id="srp-pre-owned-price-value" data-style-editor-text=".srp .inv-type-pre-owned.pricing-detail .final-price .price-value">$7,994</span>
                  <a href="/used/Chevrolet/2011-Chevrolet-Aveo-near-reno-nv-f063a9760a0e09a82f043eac9f082e0a.htm">2011 Chevrolet Aveo Aveo 5</a>
                  <li class="transmission">Transmission:  Automatic </li>
                  <li class="normalized-swatch-container exteriorColor"><span class="normalized-swatch normalized-swatch-red"></span>Sport Red Exterior</li>
                  <li class="normalized-swatch-container interiorColor"><span class="normalized-swatch normalized-swatch-gray"></span>Light Gray/Charcoal Interior</li>
                  </div>"""

        soup = BeautifulSoup(html, "html.parser")
        actual = self.new_dealer.getHondaInventory(soup)
        expected = "[\nDealer: Michael Hohl Honda\nYear: 2011\nMake: Chevrolet\nModel: Aveo Aveo 5\nPrice: $7,994\nTransmission:  Automatic \nSport Red Exterior\nLight Gray/Charcoal Interior\n]"
        self.assertEqual(str(actual), expected)

    def testGetToyotaInventory(self):
        self.setUpIntegration(active = False)
        html = """<span class="d-none d-sm-inline">100 Vehicles</span>
                  <div class="vehicle-card-details-container">
                  <span class="price-value" data-style-editor-id="srp-new-price-value" data-style-editor-text=".srp .inv-type-new.pricing-detail .final-price .price-value">$40,957</span>
                  <a href="/new/Toyota/2022-Toyota-RAV4+Hybrid-Reno-8f45ee220a0e0971574eb683a08245d6.htm">2022 Toyota RAV4 Hybrid XSE SUV</a>
                  <li class="transmission">continuously variable automatic </li>
                  <li class="normalized-swatch-container exteriorColor"><span class="normalized-swatch normalized-swatch-blue"></span>Cavalry Blue/Midnight Black Exterior</li>
                  <li class="normalized-swatch-container interiorColor"><span class="normalized-swatch normalized-swatch-black"></span>Black Interior</li>
                  </div>"""

        soup = BeautifulSoup(html, "html.parser")
        actual = self.new_dealer.getToyotaInventory(soup)
        expected = "[\nDealer: Dolan Reno Toyota\nYear: 2022\nMake: Toyota\nModel: RAV4 Hybrid XSE SUV\nPrice: $40,957\ncontinuously variable automatic \nCavalry Blue/Midnight Black Exterior\n]"
        self.assertEqual(str(actual), expected)


        
if __name__ == "__main__":
    unittest.main()
