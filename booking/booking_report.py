from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import re
class BookingReport:
    def __init__(self, boxesSectionElement: WebElement):
        self.boxesSectionElement = boxesSectionElement
        self.dealBoxes = self.pullDealBoxes()
        
    def pullDealBoxes(self):
        # Extract all the property cards
        return self.boxesSectionElement.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")
    
    def pullDealBoxesAttributes(self):
        collection = []
        for dealBox in self.dealBoxes:
            # Extract hotel name
            hotel_name = dealBox.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text.strip()
            
            # Extract hotel price
            hotel_price = dealBox.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text.strip()
            
            # Extract hotel score
            try:
                score_div = dealBox.find_element(By.CSS_SELECTOR, "div[data-testid='review-score']").text.strip()
                numbers_in_text = re.findall(r'\d+,\d+', score_div)  # Finds patterns like "8,5"
                hotel_score = numbers_in_text[0] if numbers_in_text else "N/A"
            except:
                hotel_score = "N/A"
            
            # Extract hotel link
            try:
                hotel_link = dealBox.find_element(By.CSS_SELECTOR, "a[data-testid='title-link']").get_attribute('href')
            except:
                hotel_link = "N/A"
            
            # Append hotel attributes to the collection
            collection.append({
                'name': hotel_name,
                'price': hotel_price,
                'score': hotel_score,
                'link': hotel_link
            })
        
        return collection
