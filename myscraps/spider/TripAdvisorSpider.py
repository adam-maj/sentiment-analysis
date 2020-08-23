import scrapy

class TripAdvisorSpider(scrapy.Spider):
    name = 'TripAdvisorSpider'
    
    start_urls = [
            'https://www.tripadvisor.com/Attraction_Review-g60827-d3573694-Reviews/-Barclays_Center-Brooklyn_New_York.html'
            ]

    def parse(self, response):
        for review in response.xpath("//div[@class='review-container']"):
            yield {
                'review': review.xpath(".//p[@class='partial_entry']").extract_first()
            }
        
        next_page = response.xpath("//a[@class='nav next taLnk ui_button primary']/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)     
            yield scrapy.Request(url = next_page_link, callback = self.parse)