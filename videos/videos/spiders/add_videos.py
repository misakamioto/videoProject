import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from videos.items import VideosItem

class AddVideosSpider(CrawlSpider):
    name = "add_videos"
    allowed_domains = ["1080zyk.com"]
    start_urls = ["https://1080zyk.com/?m=vod-type-id-4-pg-1.html"]

    rules = (Rule(LinkExtractor(allow=r"/?m=vod-type-id-4-pg-\d+\.html"),
                  callback="parse_item",
                  follow=False),)

    def parse_item(self, response):
        anime_list = response.xpath("//div[@class='xing_vb']//span[@class='xing_vb4']//a/@href")
        for item in anime_list:
            anime_page_url = f"https://1080zyk.com{item.extract()}"
            # 获取动漫id
            ret = re.match('.*/?m=vod-detail-id-(\d+)\.html', anime_page_url)
            anime_id = ret.group(1)
            yield scrapy.Request(url=anime_page_url,callback=self.anime_page,meta={"page_url":anime_page_url,'page_id':anime_id})
    def anime_page(self,response):
        page_url = response.meta["page_url"]
        page_id = response.meta["page_id"]
        name = response.xpath("//div[@class='vodh']/h2/text()").extract_first()
        url_list = response.xpath("//div[@id='play_1']//li/a[@target='_self']/@onclick")
        src = response.xpath("//div[@class='vod']//img/@src").extract_first()
        reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url = []
        for item in url_list:
            #         使用正则提取链接,并插入到url列表中
            url.append(re.findall(reg,item.extract())[0])
        video_data = VideosItem(name=name,url=str(url),src=src,page_url=page_url,page_id=page_id)
        yield video_data