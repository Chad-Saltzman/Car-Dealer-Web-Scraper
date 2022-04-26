from selenium import webdriver
from Dealer import Dealer

def setupWebDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options = options)

    return driver

def webScraperMain():
    print("\tWelcome to Car Search")
    age_status = input("Would you like to search for new or used cars?\n") or "new"
    dealer_choice = input("Would you like to look at a specific dealer (optional)\n"
                          "1. Ford\n"
                          "2. Honda\n"
                          "3. Toyota\n"
                          ) or "any"

    if dealer_choice == "1":
        dealer_choice = "Ford"
    elif dealer_choice == "2":
        dealer_choice = "Honda"
    elif dealer_choice == "3":
        dealer_choice = "Toyota"
    
    driver = setupWebDriver()
    new_dealer = Dealer(driver, age_status)
    if dealer_choice == "Ford" or dealer_choice == "any":
        new_dealer.getFordInventory()
    if dealer_choice == "Honda" or dealer_choice == "any":
        new_dealer.getHondaInventory()
    if dealer_choice == "Toyota" or dealer_choice == "any":
        new_dealer.getToyotaInventory()
    driver.quit()

    while True:
        model_to_find = input("What is the model you would like to search for? Type Q if you would like to Quit\n")
        if model_to_find.lower() == "q":
            break 
        
        search_results = new_dealer.searchInventory(model_to_find)

        print(f"\t{len(search_results)} vehicles found!")
        for vehicle in search_results:
            print(vehicle)

if __name__ == "__main__":
    webScraperMain()