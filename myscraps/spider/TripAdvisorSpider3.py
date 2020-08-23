import scrapy
from myscraps.items import ReviewItem
from scrapy.loader import ItemLoader

class TripAdvisorSpider(scrapy.Spider):
    name = 'TripAdvisorSpiderThree'
    
    start_urls = [
            'https://www.tripadvisor.com/Attraction_Review-g60827-d3573694-Reviews/-Barclays_Center-Brooklyn_New_York.html'
            ]
    
    base_url = 'https://www.tripadvisor.com'
    
    def parse(self, response):
        for link in response.xpath("//a[@class='title ']/@href").extract():
            review_link = self.base_url + link
            yield scrapy.Request(url = review_link, callback = self.parse_review)

        next_page = response.xpath("//a[@class='nav next taLnk ui_button primary']/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)     
            yield scrapy.Request(url = next_page_link, callback = self.parse)
    
    def parse_review(self, response):
        l = ItemLoader(item = ReviewItem(), selector = response)
        l.add_xpath('review', "//span[@class='fullText ']")
        
        rating = response.xpath("//span[contains(@class, 'ui_bubble_rating')]").extract()[1]
        l.add_value('rating', rating)
    
        return l.load_item()