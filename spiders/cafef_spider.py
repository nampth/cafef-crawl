import scrapy


class CafefSpider(scrapy.Spider):
    name = "cafef"

    def start_requests(self):
        url = "http://cafef.vn/timeline/%s/trang-1.chn";
        for category in range(1, 100):
            replaceUrl = url % (category)
            meta = {}
            meta['id'] = category
            yield scrapy.Request(url=replaceUrl, callback=self.parse_category, meta=meta)

    def parse_category(self, response):
        if response.css('li.tlitem'):
            url = "http://cafef.vn/timeline/%s/trang-%s.chn"
            for page in range(1, 20):
                replaceUrl = url % (response.meta['id'], page)
                yield scrapy.Request(url=replaceUrl, callback=self.parse, priority=1, dont_filter=True)

    def parse(self, response):
        for element in response.css('li.tlitem'):
            if element.xpath('/html/body/li[1]/div/p[1]/a/text()').get():
                obj = {
                    'category': element.xpath('/html/body/li[1]/div/p[1]/a/text()').get(),
                    'title': element.css('a::text').get(),
                    'time': element.css('span.get-timeago::attr(title)').get(),
                    'snippet': element.css('p.sapo::text').getall(),
                    'img': element.css('img::attr(src)').get(),
                    'content': ''
                }
                nextReq = 'http://cafef.vn' + element.css('a::attr(href)').get()
                meta = {}
                meta['obj'] = obj
                yield scrapy.Request(url=nextReq, callback=self.get_content, meta=meta)

    def get_content(self, response):
        # import pdb;pdb.set_trace()

        for content in response.css('span#mainContent'):
            arr = content.css('p::text').getall()
            str = '\\n '.join(arr)
            response.meta['obj']['content'] = str

        yield response.meta['obj']
