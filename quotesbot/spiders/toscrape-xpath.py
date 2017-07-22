# -*- coding: utf-8 -*-
import scrapy
import urlparse
from quotesbot.items import ParkItem


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'https://www.nps.gov/findapark/index.htm',
    ]

    def parse(self, response):
        parks = []
        for item in response.xpath('.//select[@data-nonselectedtext="Park Name"]//option'):
            park = ParkItem()
            park["name"] = item.xpath('./text()').extract_first()
            park["code"] = item.xpath('./@value').extract_first()
            parks.append(park)

        for park in parks:
            start = "https://www.nps.gov/"
            end = "/index.htm"
            url = start + str(park.get("code"))[3:7] + end
            request = scrapy.Request(url, callback=self.parse_history)
            request.meta["park"] = park
            yield request

    # Get the specific park website callback
    def parse_history(self, response):
        base_url = "https://www.nps.gov"

        park = response.meta["park"]
        park["history"] = response.xpath('.//p/text()').extract_first()

        hours_url = urlparse.urljoin(base_url, response.xpath('.//li/a[contains(@href, "hours")]/@href').extract_first())
        hours_request = scrapy.Request(hours_url, callback=self.parse_hours, meta={"park": park})
        yield hours_request

    def parse_hours(self, response):
        park = response.meta["park"]
        park["hours"] = response.xpath(".//p/span/text()[contains(., 'a.m.') or contains(., 'am') "
                                       "or contains(., 'A.M.') or contains(., 'AM')]").extract_first()

        fees_url = urlparse.urljoin(response.url, response.xpath('.//li/a[contains(@href, "fees")]/@href').extract_first())
        fees_request = scrapy.Request(fees_url, callback=self.parse_fees, meta={"park": park})
        yield fees_request

    # TODO
    def parse_fees(self, response):
        park = response.meta["park"]
        park["fees"] = response.xpath(".//table//text()[contains(., ' fee ') or contains(., ' charge ')"
                                      "or contains(., ' fees ') or contains(., ' passes ')]").extract_first()

        services_url = urlparse.urljoin(response.url, response.xpath('.//li/a[contains(@href, "services")]/@href')
                                        .extract_first())
        services_request = scrapy.Request(services_url, callback=self.parse_services, meta={"park": park})
        yield services_request

    # TODO Where is this??
    def parse_services(self, response):
        park = response.meta["park"]
        park["goodsandservices"] = response.xpath(".//p/span/text()").extract()

        things2do_url = urlparse.urljoin(response.url, response.xpath('.//li/a[contains(@href, "things2do")]/@href')
                                         .extract_first())
        things2do_request = scrapy.Request(things2do_url, callback=self.parse_things2do, meta={"park": park})
        yield things2do_request

    # TODO Currently use the figure to locate
    def parse_things2do(self, response):
        park = response.meta["park"]
        park["things2do"] = response.xpath(".//div[figure/@class = '-left']//strong/text()").extract()

        news_url = urlparse.urljoin(response.url, response.xpath('.//li/a[contains(@href, "news")]/@href').extract_first())
        news_request = scrapy.Request(news_url, callback=self.parse_news, meta={"park": park})
        #yield news_request
        yield {
            'name': park.get('name'),
            'things': park.get('things2do')
        }

    # TODO Currently use table to locate
    def parse_news(self, response):
        park = response.meta["park"]
        park["news"] = response.xpath(".//table//p//text()").extract()

        nature_url = urlparse.urljoin(response.url, response.xpath('.//li/a[contains(@href, "nature")]/@href').extract_first())
        nature_request = scrapy.Request(nature_url, callback=self.parse_nature, meta={"park": park})
        yield nature_request

    # TODO Currently use table to locate
    def parse_nature(self, response):
        park = response.meta["park"]
        park["nature"] = response.xpath(".//table//p//text()").extract()

        info_url = urlparse.urljoin(response.url, response.xpath('.//li/a[contains(@href, "basicinfo")]/@href').extract_first())
        info_request = scrapy.Request(info_url, callback=self.parse_info, meta={"park": park})
        yield info_request

    # TODO
    def parse_info(self, response):
        park = response.meta["park"]
        park["weather"] = response.xpath(".//p[text()[contains(., ' season ') or contains(., ' weather ') "
                                         "or contains(., ' temperature ')]]").extract_first()

        yield {
            "name": park.get('name'),
            "history": park.get('history'),
            "hours": park.get('hours'),
            "fees": park.get('fees'),
            "goodsandservices": park.get('goodsandservices'),
            "things2do": park.get('things2do'),
            "news": park.get('news'),
            "nature": park.get('nature'),
            "weather": park.get('weather')
        }
