from flask import Flask, request, jsonify, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def search_buses(source, destination, date):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_query = f"buses from {source} to {destination} on {date}"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        search_results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        top_links = []
        for result in search_results:
            parent = result.find_element(By.XPATH, '..')
            link = parent.get_attribute("href")
            text = result.text
            if link:
                top_links.append({'link': link, 'text': text})
            if len(top_links) >= 5:
                break

        buses = [{'link': item['link'], 'description': item['text']} for item in top_links]
        driver.quit()
        return buses
    except Exception as e:
        driver.quit()
        return []

def chat_with_gemini(user_input):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to Gemini website
        driver.get("https://www.gemini.com/")

        # Wait for the page to load and locate the "Chat with Gemini" button
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Chat with Gemini")))
        chat_button = driver.find_element(By.LINK_TEXT, "Chat with Gemini")
        chat_button.click()

        # Wait for the chat interface to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        
        # Send the user input to the chat
        textarea.send_keys(user_input)
        textarea.send_keys(Keys.RETURN)

        # Wait for a response
        time.sleep(5)
        response = driver.find_elements(By.CSS_SELECTOR, ".message")[-1].text
        
        driver.quit()
        return response
    except Exception as e:
        driver.quit()
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('chatbot'))
    return render_template('index2.html')  # Render the login page

@app.route('/chatbot')
def chatbot():
    return render_template('index.html')  # Render the chatbot page

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')
    date = data.get('date')
    next_step = data.get('next_step', None)

    if not next_step:
        if not (source and destination and date):
            return jsonify({'reply': 'Please provide source, destination, and date.'})
        
        try:
            buses = search_buses(source, destination, date)
            if buses:
                reply = 'Here are some bus options:\n' + '\n\n'.join(
                    f"Link {idx + 1}: <a href='{bus['link']}' target='_blank' style='color:#ffcc00;'>{bus['link']}</a>\nDetails: {bus['description']}" 
                    for idx, bus in enumerate(buses)
                )
                reply += "\n\nWould you like to search for more buses or ask something else?"
            else:
                reply = 'No buses found for the given criteria.\n\nWould you like to search for more buses or ask something else?'
        except Exception as e:
            reply = f'Sorry, there was an error processing your request: {str(e)}'
    else:
        if next_step == "search_buses":
            return jsonify({'reply': 'Where are you starting your journey? (Source)', 'reset': True})
        else:
            gemini_response = chat_with_gemini(data.get('user_input', ''))
            reply = f"Gemini Response: {gemini_response}\n\nWould you like to search for more buses or ask something else?"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
