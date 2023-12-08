import requests

url = "https://search.wb.ru/exactmatch/ru/male/v4/search"

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "x-userid": "61637444",
    "Origin": "https://www.wildberries.ru",
    "Connection": "keep-alive",
    "Referer": "https://www.wildberries.ru/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site"
}

class ParseWB:
    def web_settings(self, product):
        url = "https://search.wb.ru/exactmatch/ru/male/v4/search"
        querystring = {"TestGroup":"rec_search_goods_new_model","TestID":"370","appType":"1","curr":"rub","dest":"-3524932","query":f"{product}","resultset":"catalog","sort":"popular","spp":"26","suppressSpellcheck":"false","uclusters":"1"}

        payload = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "x-userid": "61637444",
            "Origin": "https://www.wildberries.ru",
            "Connection": "keep-alive",
            "Referer": "https://www.wildberries.ru/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }

        response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
        ).json()

        return response

    def parse(self, product: str):
        response = self.web_settings(product)
        products = response["data"]["products"]
        data = []
        for product in products:
            name = product["name"]
            id = product['id']
            url = f'https://www.wildberries.ru/catalog/{id}/detail.aspx'
            price = str(product["salePriceU"])[:-2] + '₽'
            data.append([str(name), str(url), str(price)])

        return data

