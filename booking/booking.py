from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import time
from prettytable import PrettyTable
from selenium.webdriver.support.select import Select
from booking.bookingfilters import BookingFilters
import booking.constants as const
from booking.booking_report import BookingReport
import os



class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"../chromedriver-mac-x64", tearDown=False):
        self.driver_path = driver_path
        self.teardown = tearDown
        os.environ['PATH'] += os.pathsep + self.driver_path
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        super(Booking, self).__init__(options=chrome_options)
        self.implicitly_wait(15)
        self.maximize_window()  # Optional: Maximizes the browser window.

    def land_first_page(self):
        self.get(const.BASE_URL)
    
    def change_currency(self, currency=None):
        # Ensure the page is fully loaded
        WebDriverWait(self, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

        # Dismiss the consent popup if it appears
        try:
            currency_element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='onetrust-reject-all-handler']"))
            )

            currency_element.click()

            consent_button = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'button[data-testid="header-currency-picker-trigger"]'))
            )
            consent_button.click()

            currency_elements = WebDriverWait(self, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.CurrencyPicker_currency"))
            )

            # Iterate over the list of elements and click the one with the matching text
            for element in currency_elements:
                if element.text.strip() == currency:
                    element.click()
                    print(f"Clicked on the currency: {currency}")
                    break
            else:
                print(f"Currency '{currency}' not found.")
            close = WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div[class='abcc616ec7 cc1b961f14 c180176d40 f11eccb5e8 ff74db973c']")))
            close.click()



                
        except:
            print("Consent button not found or not clickable.")
        
       

    def select_place_to_go(self,place_to_go:str):
        WebDriverWait(self, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        wait = WebDriverWait(self, 10)
        
        search_field = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id=':rh:']"))
        )
        search_field.clear()
        search_field.send_keys(place_to_go)
        time.sleep(2)
        search_field.click()

        # Wait for the dropdown list to be present
        results = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='group']//li//div//div//div//div")))
        # time.sleep(0.5)
       
        for i, first_result in enumerate(results):
            try:
                # Re-locate the element to avoid stale reference exception
                results = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='group']//li//div//div//div//div")))
                first_result = results[i]

                # Check if the text of the result matches the place to go
                if first_result.text.lower() == place_to_go.lower():
                    print(f"Match found: {first_result.text}")
                    
                    try:
                        # Try to click the element
                        first_result.click()
                    except ElementClickInterceptedException:
                        print(f"Element click intercepted for {first_result.text}, using JavaScript to click.")
                        # Use JavaScript to click the element if click is intercepted
                        self.execute_script("arguments[0].click();", first_result)
                    return  # Exit the function after clicking the result

                

            except StaleElementReferenceException:
                print(f"Element {i} became stale, retrying...")

                # Retry finding the element again after a short wait
                results = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='group']//li//div//div//div//div")))
                first_result = results[i]
                
                # Retry comparison after refreshing the element
                if first_result.text.lower() == place_to_go.lower():
                    print(f"Match found: {first_result.text}")
                    # Scroll the element into view and use JS to click if necessary
                    self.execute_script("arguments[0].scrollIntoView(true);", first_result)

                    try:
                        first_result.click()
                    except ElementClickInterceptedException:
                        self.execute_script("arguments[0].click();", first_result)
                    return

        # If no match found, print this
        print(f"'{place_to_go}' not found.")

    def wait(self,sec):
        time.sleep(sec)

    def select_date(self,checkIn,checkOut):

        checkInElement = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{checkIn}"]')))
        checkInElement.click()

        checkOutElement = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{checkOut}"]')))
        checkOutElement.click()
    
    def select_people(self, adultsCount=1, childrenCount=0, childrenAges=[]):
        # Ensure the number of children matches the number of ages provided
        if childrenCount != len(childrenAges):
            raise ValueError("The number of children must match the number of ages provided.")

        # Open the selection element for adults and children
        selectionElement = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-controls=':ri:']"))
        )
        selectionElement.click()

        # Set the number of adults
        if adultsCount:
            while True:
                decreaseAdultElement = WebDriverWait(self, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id=":ri:"]/div/div[1]/div[2]/button[1]'))
                )
                decreaseAdultElement.click()

                adultValueElement = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="group_adults"]'))
                )
                adultsValue = adultValueElement.get_attribute('value')

                if int(adultsValue) == 1:
                    break

            increaseAdultElement = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id=":ri:"]/div/div[1]/div[2]/button[2]'))
            )
            for _ in range(int(adultsCount) - 1):
                increaseAdultElement.click()

        # Set the number of children and their ages
        if childrenCount:
            while True:
                childrenValueElement = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="group_children"]'))
                )
                childrenValue = childrenValueElement.get_attribute('value')

                if int(childrenValue) != 0:
                    decreaseChildrenElement = WebDriverWait(self, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id=":ri:"]/div/div[2]/div[2]/button[1]'))
                    )
                    decreaseChildrenElement.click()
                if int(childrenValue) == 0:
                    break

            increaseChildrenElement = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id=":ri:"]/div/div[2]/div[2]/button[2]'))
            )
            for _ in range(int(childrenCount)):
                increaseChildrenElement.click()

            # Now select the ages for each child
            for index, age in enumerate(childrenAges):
               
                
                # Re-find the age select elements every time to prevent stale element references
                selectorDivs = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='kids-ages']"))
                )
                ageSelectElements = selectorDivs.find_elements(By.CSS_SELECTOR, "div[data-testid='kids-ages-select']")

                # Find the corresponding select element for this child
                ageElement = ageSelectElements[index].find_element(By.TAG_NAME, 'select')
                
                # Select the age for the current child
                Select(ageElement).select_by_value(str(age))
                selectionElement = WebDriverWait(self, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-controls=':ri:']"))
                )
                selectionElement.click()
                
                # Adding a small delay for each selection to avoid racing conditions

                time.sleep(1)









        
    def clickSearch(self):
        searchButton = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="indexsearch"]/div[2]/div/form/div[1]/div[4]/button')))
        searchButton.click()

    def apply_filters(self,*star_values):
        filtration = BookingFilters(driver=self)
        filtration.apply_star_rating(*star_values)
        filtration.sort_lowest_price()
    
    # def report_results(self):
    #     hotelBoxes = self.find_element(By.XPATH,'//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]')

    #     report = BookingReport(hotelBoxes)
    #     table = PrettyTable(
    #         field_names=["Hotel Name", "Hotel Price","Hotel Score"]
    #     )
    #     table.add_rows(report.pullDealBoxesAttributes())
    #     print(table)

    # def report_results(self):
    #     hotelBoxes = self.find_element(By.XPATH, '//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]')
        
    #     report = BookingReport(hotelBoxes)
        
    #     # Create a PrettyTable object to format the output
    #     table = PrettyTable(
    #         field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
    #     )
        
    #     # Add rows from the report's data
    #     table.add_rows(report.pullDealBoxesAttributes())
        
    #     # Convert the PrettyTable to a string and return it
    #     return str(table)

            

        