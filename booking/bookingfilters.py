from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

class BookingFilters:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        posilbitites = ["o", "m", "q", "4"]

        try:
            time.sleep(2)
            # Locate the star rating filter box
            star_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
            
            for star_value in star_values:
                child_divs = star_box.find_elements(By.TAG_NAME, 'div')
                time.sleep(1)
                for div in child_divs:
                    try:
                        time.sleep(1)
                        data_filters_item = div.get_attribute("data-filters-item")
                        
                        # Check if the star value matches
                        if data_filters_item == f"class:class={star_value}":
                            # Wait until the div is clickable
                            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(div))
                            
                            # Click the div
                            print(f"Selected stars: {star_value}")
                            div.click()
                            break  # Exit the loop once the matching div is found and clicked

                    except StaleElementReferenceException:
                        # Re-locate the star_box and child divs if the element is stale
                        print(f"StaleElementReferenceException: retrying to find elements for star value {star_value}")
                        star_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
                        child_divs = star_box.find_elements(By.TAG_NAME, 'div')
    
        except Exception as e:
            print(f"Error occurred: {e}")
                    
    def sort_lowest_price(self):
        # Wait for the drop-down filter box to be clickable and click it
        dropBox = self.driver.find_element(By.CSS_SELECTOR,"button[data-testid='sorters-dropdown-trigger']")
        time.sleep(2)
        dropBox.click()
        #//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[1]/div/div/div/span/button

        time.sleep(2)

        # Define the possible values for the element's identifier
        # possibilities = ["74","75","76","77","78"]

        #"div[data-testid='sorters-dropdown']"
        div = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='sorters-dropdown']"))
        )
        # div = None  # Initialize div to None
        # for i in range(0, len(possibilities)):  # Adjust range to 3 to cover all possibilities
        #     try:
        #         div = WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, f'//*[@id=":r{possibilities[i]}:"]/div'))
        #         )
        #         break  # Exit the loop if the element is found
        #     except:
        #         print(f"Unable to find the element with the {possibilities[i]} class number. Trying again.")

        # # Check if div was successfully found
        # #span[data-testid='price-and-discounted-price']
    
        if div:
            # Now look for the button within the div element

            button = div.find_element(By.XPATH,'.//button[@data-id="price"]')
            button.click()

        else:
            print("Unable to find any matching element for sorting by price.")

        
    