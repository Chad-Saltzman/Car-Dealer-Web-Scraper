from bs4 import BeautifulSoup
import unittest

from WebScraper import *
from Vehicle import Vehicle

class TestWebScraperUnitTest(unittest.TestCase):

    def setUp(self):
        self.driver = ""

    def setUpIntegration(self, active = True):
        if active:
            self.driver = setupWebDriver()
        else:
            self.driver = ""
        self.new_dealer = Dealer(self.driver, "new")
        self.new_vehicle = Vehicle("test dealer", "2000", "Honda", "Civic", "$10000")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def testWebScrapeFordDealerNewCars(self):
        self.setUpIntegration()
        self.assertTrue(self.new_dealer.getFordInventory())

    def testWebScrapeFordDealerUsedCars(self):
        self.setUpIntegration()
        self.new_dealer.age_status = "used"
        self.assertTrue(self.new_dealer.getFordInventory())

    def testWebScrapeHondaDealerNewCars(self):
        self.setUpIntegration()
        self.assertTrue(self.new_dealer.getHondaInventory())

    def testWebScrapeHondaDealerUsedCars(self):
        self.setUpIntegration()
        self.new_dealer.age_status = "used"
        self.assertTrue(self.new_dealer.getHondaInventory())

    def testWebScrapeToyotaDealerNewCars(self):
        self.setUpIntegration()
        self.assertTrue(self.new_dealer.getToyotaInventory())

    def testWebScrapeToyotaDealerUsedCars(self):
        self.setUpIntegration()
        self.new_dealer.age_status = "used"
        self.assertTrue(self.new_dealer.getToyotaInventory())


if __name__ == "__main__":
    unittest.main()