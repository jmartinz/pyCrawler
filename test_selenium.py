from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Firefox()
driver.get("https://duckduckgo.com/")
driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
html_page = driver.page_source
driver.quit()
soup = BeautifulSoup(html_page)
titles = [h1.text for h1 in soup.findAll('h2')]

for t in titles:
    print(t)

