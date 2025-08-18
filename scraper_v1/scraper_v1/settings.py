# Scrapy settings for scraper_v1 project

BOT_NAME = "scraper_v1"

SPIDER_MODULES = ["scraper_v1.spiders"]
NEWSPIDER_MODULE = "scraper_v1.spiders"

# -----------------------------------------
# Playwright integration
# -----------------------------------------

# Use Scrapy-Playwright download handler
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# 🚨 REMOVE THIS (causes your error)
# DOWNLOADER_MIDDLEWARES = {
#     "scrapy_playwright.middleware.ScrapyPlaywrightDownloaderMiddleware": 543,
# }

# Async reactor required for Playwright
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Browser options
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

# -----------------------------------------
# Crawl behavior
# -----------------------------------------

ROBOTSTXT_OBEY = False
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    "products.json": {"format": "json", "overwrite": True},
}

CONCURRENT_REQUESTS = 8
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 8

# -----------------------------------------
# Logging
# -----------------------------------------
LOG_LEVEL = "INFO"
