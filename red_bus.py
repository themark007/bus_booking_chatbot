from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def search_buses(source, destination, day, date, time_str):
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.get("https://www.redbus.in/")
    
    try:
        source_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "src"))
        )
        source_input.clear()
        source_input.send_keys(source)
        time.sleep(2)
        source_input.send_keys(Keys.ENTER)
        
        destination_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "dest"))
        )
        destination_input.clear()
        destination_input.send_keys(destination)
        time.sleep(2)
        destination_input.send_keys(Keys.ENTER)
        
        date_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "onward_cal"))
        )
        date_input.click()
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)
        
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "search_btn"))
        )
        search_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "bus-item"))
        )
        
        buses = []
        bus_elements = driver.find_elements(By.CLASS_NAME, "bus-item")
        for bus in bus_elements:
            try:
                bus_name = bus.find_element(By.CLASS_NAME, "travels").text
                bus_timing = bus.find_element(By.CLASS_NAME, "departure").text + " - " + bus.find_element(By.CLASS_NAME, "arrival").text
                bus_fare = bus.find_element(By.CLASS_NAME, "fare").text
                bus_link = bus.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                if day in bus_timing and time_str in bus_timing:
                    buses.append({
                        'name': bus_name,
                        'time': bus_timing,
                        'fare': bus_fare,
                        'link': bus_link
                    })
            except Exception as e:
                print("Error processing bus element:", e)
                continue
        
        driver.quit()
        return buses
    except Exception as e:
        print("An error occurred while searching for buses:", e)
        driver.quit()
        return []
