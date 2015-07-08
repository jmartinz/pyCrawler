from selenium import webdriver

service_args = [
    '--proxy=proxy-msc.msc.es:8080',
    '--proxy-type=http',
    '--proxy-auth=xxx:xxx',
    ]    
    
driver = webdriver.PhantomJS("/home/jmartinpit/phantomjs/bin/phantomjs",service_args=service_args)
#driver = webdriver.Firefox(capabilities=service_args)
driver.set_window_size(1120, 550)
#driver.get("https://duckduckgo.com/")
driver.get("https://contrataciondelestado.es")
print driver.page_source

#driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
#driver.find_element_by_id("search_button_homepage").click()
print driver.current_url
driver.quit()
