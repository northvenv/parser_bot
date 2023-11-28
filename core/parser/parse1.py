import logging
import csv
import requests
import bs4
import collections
#from core.handlers.basic import get_name_product

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ozon')





ParseResult = collections.namedtuple(
    'ParsePesult',
    (
        'url',
        'name',
    )
)

class Client:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
        'authority': 'www.ozon.ru',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'content-type': 'application/json',
        # 'cookie': '__Secure-ab-group=26; __Secure-user-id=0; xcid=e0c47d5a9c58478d723e923364f212c3; __Secure-ext_xcid=e0c47d5a9c58478d723e923364f212c3; guest=true; __Secure-refresh-token=3.0.EqtFsrrhTpW_aHsLvq3D2g.26.l8cMBQAAAABlIUsTB9b3Q6N3ZWKgAICQoA..20231102114411.BXJ4I2z3GBcQZJzam4V3hVsH8i2Y3rOfQ_QPPhXkRYE; __Secure-access-token=3.0.EqtFsrrhTpW_aHsLvq3D2g.26.l8cMBQAAAABlIUsTB9b3Q6N3ZWKgAICQoA..20231102114411.oLc2gpAl7tzbEd6ghjklTgjLNP66J08I4FZCbdMD3YQ; abt_data=596ea35e119c6d6ec602d8c125c77e0f:8b9894cbd826e3a169bb0f7bf38e84327f0662df84aba62dee7233fff29cdb644c746c6e645d7b44ca0f661f9da66fbee8629c009f158e1fd0edc143b2857c6ff3ac8e4c4c26d68bc955de9be47d0619469c14f3d1e8a1c687f516596696048a8c2340034f31fc5c0280f5522191872c9e7de1b4c0c87f241fca6440241f7001; cf_clearance=PSI6DExvO5sV_BVx9Jey23c33SseEg1KyxcbIqMu92A-1698918251-0-1-7646f717.98ab0c3b.19cec237-0.2.1698918251; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwtMjg3MDM2NTYzLC0xLC0xMTMxMjI1MjYwLFczc2libUZ0WlNJNklsQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpYkdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01aGJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWxkbFlrdHBkQ0JpZFdsc2RDMXBiaUJRUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKbGJpMVZVeUpkLDAsMSwwLDI0LDIzNzQxNTkzMCw4LDIyNzEyNjUyMCwxLDEsMCwtNDkxMjc1NTIzLFIyOXZaMnhsSUVsdVl5NGdUbVYwYzJOaGNHVWdSMlZqYTI4Z1RHbHVkWGdnZURnMlh6WTBJRFV1TUNBb1dERXhPeUJNYVc1MWVDQjRPRFpmTmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNVGd1TUM0d0xqQWdVMkZtWVhKcEx6VXpOeTR6TmlBeU1EQXpNREV3TnlCTmIzcHBiR3hoLGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZYMTksNjUsLTEyODU1NTEzLDEsMSwtMSwxNjk5OTU0ODg3LDE2OTk5NTQ4ODcsLTE1NjE0ODE2NzAsMTI=; ADDRESSBOOKBAR_WEB_CLARIFICATION=1698918254; __cf_bm=sC.cWXIe74BZcsCLlEMwT9HAsUYXJIuxf7eI6zKZLhc-1698920114-0-AUj4SxnUDu0Of3IB6CIF6oGvfybLBmGiMmwLeCT+kJQI3HdZBQkMZY2k0hMphG0BIs+triZuqeFjGz6MOnY3Rbs=',
        'referer': 'https://www.ozon.ru/brand/sela-24124695/category/odezhda-obuv-i-aksessuary-7500/',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-o3-app-name': 'dweb_client',
        'x-o3-app-version': '27-9-2023_df6aa02e',
        'x-o3-manifest-version': 'df6aa02ee3ff07007b067a367c7b8ffc2a337ead',
        }

        self.result = []

    def load_page(self, page : int = None):
        
        url = 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        print(soup)
        container = soup.select('article.product-card.product-card--hoverable.j-card-item ') #article.product-card.product-card--hoverable.j-card-item   
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        url_block = block.select_one('a.i4s.tile-hover-target')
        if not url_block:
            logger.error('no url_block')
            return
        
        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return 
        

        name_block = block.select_one('span.tsBody500Medium')
        if not name_block:
            logger.error('no name_block on {url}')
            return


        # brand_name = name_block.select_one('span.product-card__brand')
        # if not brand_name:
        #     logger.error('no brand_name')
        #     return

        # brand_name = brand_name[:-2]

        # goods_name = name_block.select_one('span.product-card__name')
        # if not goods_name:
        #     logger.error('no goods_name')
        #     return 
        
        self.result.append(ParseResult(
            url=url,
            name=name_block,
            
        ))
        
        logger.debug('%s, %s', url, name_block)
        logger.debug('-' * 100)

    def save_result(self):
        path = 'core/parser/test.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    
    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Получили {len(self.result)} элементов')

if __name__ == '__main__':
    parser = Client()
    parser.run()















