import xlsxwriter
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

class ParseWB:
    def web_settings(self, url):
        firefox_options = Firefox_Options()

        driver = Service('/home/ekwize/Documents/ParseBot/core/parser/geckodriver') ## path where you saved geckodriver
        
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


    def get_data_with_selenium(self, url):
        self.web_settings(url)

        # get hotels urls
        soup = bs4(self.index_selenium, "lxml")
        all_blocks = soup.find_all("div", class_ = "product-card__wrapper")
        data = []
        for block in all_blocks:
            data.append(self.parse_block(block))
        
        
        self.create_excel_file(data)
             
    # def parse_page(self, text: str):
    #     soup = bs4(text, 'lxml')
    #     container = soup.select('article.product-card.product-card--hoverable.j-card-item ') #article.product-card.product-card--hoverable.j-card-item   
    #     for block in container:
    #         self.parse_block(block=block)

    def parse_block(self, block):
        url_block = block.select_one("a", class_="product-card__link j-card-link j-open-full-product-card")
        name = str(url_block.get('aria-label'))
        # brand_name = block.select_one("span", class_="product-card__brand")
        url = str(url_block.get('href'))
        price_block = block.select_one("span", class_="price__wrap")
        price = str(price_block.get('ins'))

        return [name, url, price]
    



    def create_excel_file(self, data):
        
        name_columns = [
            ('Название', 'A1'),
            ('Ссылка на товар', 'B1'), 
            ('Цена', 'C1'),
        ]
        workbook = xlsxwriter.Workbook('wildberries.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_row(0, 40)

        bold = workbook.add_format({'bold': True})
        counter = 0
        for field_data in name_columns:
            name, field = field_data
            worksheet.set_column(counter, counter, 40)
            worksheet.write(field, name, bold)
            counter += 1
        row = 1
        for product in data:
            col_number = 0
            for i in range(len(product)):
                worksheet.write(row, col_number, product[i])
                col_number += 1
            row += 1
        workbook.close()

    def main(self):
        self.get_data_with_selenium("https://www.wildberries.ru/catalog/0/search.aspx?search=привет")


if __name__ == '__main__':
    parser = ParseWB()
    parser.main()
