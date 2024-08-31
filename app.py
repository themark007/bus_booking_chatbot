from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def search_buses(source, destination, date):
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.get("https://www.redbus.in/")
    
    try:
        source_input = driver.find_element(By.ID, "src")
        source_input.clear()
        source_input.send_keys(source)
        time.sleep(2)
        source_input.send_keys(Keys.ENTER)
        
        destination_input = driver.find_element(By.ID, "dest")
        destination_input.clear()
        destination_input.send_keys(destination)
        time.sleep(2)
        destination_input.send_keys(Keys.ENTER)
        
        date_input = driver.find_element(By.ID, "onward_cal")
        date_input.click()
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)
        
        search_button = driver.find_element(By.ID, "search_btn")
        search_button.click()
        
        time.sleep(5)
        
        buses = []
        bus_elements = driver.find_elements(By.CLASS_NAME, "bus-item")
        for bus in bus_elements:
            try:
                bus_name = bus.find_element(By.CLASS_NAME, "travels").text
                bus_timing = bus.find_element(By.CLASS_NAME, "departure").text + " - " + bus.find_element(By.CLASS_NAME, "arrival").text
                bus_fare = bus.find_element(By.CLASS_NAME, "fare").text
                bus_link = bus.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                buses.append({
                    'name': bus_name,
                    'time': bus_timing,
                    'fare': bus_fare,
                    'link': bus_link
                })
            except Exception as e:
                continue
        
        driver.quit()
        return buses
    except Exception as e:
        driver.quit()
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    date = data.get('date')

    if not (source and destination and date):
        return jsonify({'reply': 'Please provide source, destination, and date.'})

    # Simulate a typing delay
    time.sleep(1)

    try:
        buses = search_buses(source, destination, date)
        
        if buses:
            reply = 'Here are some buses you can take:\n' + '\n'.join(
                f"{bus['name']} | {bus['time']} | Fare: {bus['fare']} - {bus['link']}" for bus in buses
            )
        else:
            reply = 'No buses found for the given criteria.'
    except Exception as e:
        reply = f'Sorry, there was an error processing your request: {str(e)}'

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
