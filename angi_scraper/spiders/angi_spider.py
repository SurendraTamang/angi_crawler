import scrapy
import json


class AngiSpider(scrapy.Spider):
    name = "angi"
    custom_settings = {
        "FEEDS": {
            f"{name}.json": {"format": "json", "overwrite": True},

        }
    }

    def start_requests(self):
        url = "https://www.angi.com/companylist/us"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath(
            "//li/a[contains(@id,'companylist-state')]/@href")
        for link in links:
            yield response.follow(url=link.get(), callback=self.parse_state)

    def parse_state(self, response):
        links = response.xpath("//li/a[contains(@id, 'all-cities')]/@href")
        for link in links:
            yield response.follow(url=link.get(), callback=self.parse_city)

    def parse_city(self, response):
        links = response.xpath(
            "//li/a[contains(@id, 'city-category-list')]/@href")
        for link in links:
            yield response.follow(url=link.get(), callback=self.parse_category)

    def parse_category(self, response):
        results = response.xpath(
            '//script[@id="__NEXT_DATA__"]/text()').extract()
        for result in results:
            yield json.loads(result)
