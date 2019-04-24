# -*- coding: utf-8 -*-
import scrapy


class GenrecrawlSpider(scrapy.Spider):
    name = 'genrecrawl'
    allowed_domains = ['albumoftheyear.org']
    start_urls = ['https://www.albumoftheyear.org/genre.php']

    def parse(self, response):
        # Box of all genres at right of page
        box = response.xpath('//*[@id="centerContent"]/div/div[2]/div[2]')
        # Genre links are divided into two columns
        links1 = box.xpath('./div[2]/div')
        links2 = box.xpath('./div[3]/div')
        # Get the link for each genre in the two columns and start with 2010s
        links = [l.css('div a::attr(href)').get() for l in (links1 + links2)]
        links = [l + '2010s/' for l in links]
        for l in links:
            yield response.follow(l, callback=self.parse_decade)


    def parse_decade(self, response):
        # If the page has results, go back one decade and look for more
        if response.css('noResultsMessage') is not None:
            prev_decade = response.xpath('//*[contains(@class, "yearNavBoxArrow")]/../@href').get()
            yield response.follow(prev_decade, callback=self.parse_decade)
        # follow links to album pages
        for a in response.css('.albumListCover a'):
            yield response.follow(a, callback=self.parse_album, headers={'referrer': response.url})
        next_link = response.xpath('//div[contains(text(), "NEXT")]/../@href').get()
        if next_link:
            yield response.follow(next_link, callback=self.parse_page)


    def parse_page(self, response):
        # follow links to album pages
        for a in response.css('.albumListCover a'):
            yield response.follow(a, callback=self.parse_album, headers={'referrer': response.url})
        next_link = response.xpath('//div[contains(text(), "NEXT")]/../@href').get()
        if next_link:
            yield response.follow(next_link, callback=self.parse_page)


    def parse_album(self, response):
        url = response.url
        referred = response.request.headers.get('referrer').decode('utf-8')

        artist = response.xpath('//div[@class="artist"]/span/a/span/text()').get()
        album = response.xpath('//div[@class="albumTitle"]/span/text()').get()
        image = response.xpath('//picture/source/source/img/@src').get()

        critic_box = response.xpath('//*[@id="centerContent"]/div[1]/div[4]/div[1]')
        critic_score = critic_box.xpath('./div[2]/span/a/text()').get()
        critic_num = critic_box.xpath('./div[3]/strong/span/text()').get()
        critic_rank = critic_box.xpath('./div[4]/strong/a/text()').get()
        critic_outof = critic_box.xpath('./div[4]/text()').re('/ (\d+)')
        # safely get first group from regex match
        critic_outof = critic_outof[0] if critic_outof else None

        user_box = response.xpath('//*[@id="centerContent"]/div[1]/div[4]/div[2]')
        user_score = user_box.xpath('./div[2]/a/text()').get()
        user_num = user_box.xpath('./div[3]/a/strong/text()').get()
        user_rank = user_box.xpath('./div[4]/strong/a/text()').get()
        user_outof = user_box.xpath('./div[4]/text()').re('/ (\d+)')
        # safely get first group from regex match
        user_outof = user_outof[0] if user_outof else None

        box = response.xpath('//*[@id="centerContent"]/div[1]/div[5]')
        date = box.xpath('./div[2]//text()').getall()
        date = date[:3] if len(date) >= 3 else None
        release_format = box.xpath('./div[3]/text()').get()
        label = box.xpath('./div[4]/text()').get()
        genres = box.xpath('./div[5]/a/text()').getall()
        tags = response.xpath('//div[@class="tag"]//text()').getall()

        yield {
            'url': url,
            'referred': referred,

            'artist': artist,
            'album': album,
            'image_link': image,

            'critic_score': critic_score,
            'critic_num': critic_num,
            'critic_rank': critic_rank,
            'critic_outof': critic_outof,

            'user_score': user_score,
            'user_num': user_num,
            'user_rank': user_rank,
            'user_outof': user_outof,

            'date': date,
            'format': release_format,
            'label': label,
            'genres': genres,
            'tags': tags
        }
