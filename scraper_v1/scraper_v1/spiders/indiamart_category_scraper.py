import scrapy
import re
import os
from airflow.providers.standard.operators.bash import BashOperator
class IndiaMartSubcategoriesSpider(scrapy.Spider):
    name = "indiamart_categories"
    allowed_domains = ["dir.indiamart.com"]
    start_urls = [
        "https://dir.indiamart.com/industry/drugs-medicines.html",
        "https://dir.indiamart.com/industry/builders-hardware.html"
    ]
    def parse(self, response):
        match = re.search(r'/industry/([^/.]+)\.html', response.url)
        category_key = match.group(1) if match else "unknown"

        for a in response.css('a[href^="/impcat/"]'):
            text = a.xpath('normalize-space(string())').get()
            url = response.urljoin(a.attrib['href'])

            if "?" in url:
                url = url + "&list_view=1"
            else:
                url = url + "?list_view=1"

            yield {
                'subcategory_text': text,
                'subcategory_url': url,
                'category_key': category_key
            }
