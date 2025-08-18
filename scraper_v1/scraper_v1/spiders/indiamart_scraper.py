import scrapy
import re

class IndiaMartSubcategoriesSpider(scrapy.Spider):
    name = "indiamart_subcategories"
    allowed_domains = ["dir.indiamart.com"]
    start_urls = [

        "https://dir.indiamart.com/industry/drugs-medicines.html",
        "https://dir.indiamart.com/industry/agro-farm.html",

    ]

    def parse(self, response):
        # Dynamically extract the category key from the URL
        match = re.search(r'/industry/([^/.]+)\.html', response.url)
        category_key = match.group(1) if match else "unknown"

        for a in response.css('a[href^="/impcat/"]'):
            text = a.xpath('normalize-space(string())').get()
            url = response.urljoin(a.attrib['href'])
            yield {
                'subcategory_text': text,
                'subcategory_url': url,
                'category_key': category_key
            }