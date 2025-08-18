# from scrapy import Spider
# from scrapy.selector import Selector
# from selenium import webdriver

# class IndiaSpider(Spider):
#     name = 'india'
#     start_urls = ['https://dir.indiamart.com/search.mp?ss=laptop']

#     def __init__(self):
#         self.driver = webdriver.Chrome()  # Or another driver

#     def parse(self, response):
#         self.driver.get(response.url)
#         sel = Selector(text=self.driver.page_source)
#         for prod in sel.xpath("//span[contains(@class,'mListNme')]"):
#             yield {
#                 'title': prod.xpath("./a/text()").get(),
#                 'link': prod.xpath("./a/@href").get()
#             }
#         self.driver.quit()


