from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as Firefox_Options
import time 

class ParseAvito:
    def web_settings(self, url):
        firefox_options = Firefox_Options()

        driver = Service('/home/ekwize/Documents/ParseBot/core/parser/geckodriver')
        firefox_options.add_argument('headless')
        firefox_options.add_argument('window-size=1920x935')
        
        try:
            browser = webdriver.Firefox(service=driver, options=firefox_options)
            browser.get(url=url)
            time.sleep(5)
        
            self.index_selenium = browser.page_source
        
        except Exception as ex:
            print(ex)
        finally:
            browser.close()
            browser.quit()


    def get_data_with_selenium(self, query):
        url = f'https://www.avito.ru/all?q={query}'
        self.web_settings(url)

        # get hotels urls
        soup = BeautifulSoup(self.index_selenium, "lxml")
        
        all_blocks = soup.find_all("a", class_="styles-module-root-QmppR styles-module-root_noVisited-aFA10")
        data = []
        for block in all_blocks:
            link = 'https://www.avito.ru' + block.get('href')
            name = block.get('title')
            data.append([str(name), str(link)])
        
        return data
             

    








