# -*- coding: utf-8 -*-
import scrapy
import json
import urllib.parse


class BhxhSpider(scrapy.Spider):
    name = 'bhxh'
    allowed_domains = ['baohiemxahoi.gov.vn']
    urls = [
        'https://baohiemxahoi.gov.vn/UserControls/JpegImage.aspx',
        'https://baohiemxahoi.gov.vn/UserControls/BHXH/BaoHiemYTe/HienThiHoGiaDinh/pListKoOTP.aspx'
    ]
    frmdata = {
        "matinh": '08TTT',
        'mahuyen': '',
        'maxa': '',
        'mathon': '',
        'macd': '',
        'tennhankhau': 'Phan Thai Hong Nam',
        'cmnd': '070952705',
        'ngaysinh': '',
        'namsinh': '',
        'BL_Captcha': '',
        'typetext': 'KhongDau'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.urls[0], callback=self.parse)

    def parse(self, response):
        cookie = response.headers.getlist('Set-Cookie')[0].decode('utf-8')

        file = open("/home/nam/demo/demo/img/1.jpg", 'wb')
        file.write(response.body)
        var = input("Captcha: ")
        self.frmdata['BL_Captcha'] = str(var)

        yield scrapy.Request(url=self.urls[1], callback=self.parse_response, method='POST',
                             body=urllib.parse.urlencode(self.frmdata),
                             # cookies=req_cookie,
                             headers={
                                 'Content-Type': 'application/x-www-form-urlencoded',
                                 'Cookies': cookie,
                                 'Host': 'baohiemxahoi.gov.vn',
                                 'Referer': 'https://baohiemxahoi.gov.vn/tracuu/Pages/tra-cuu-ho-gia-dinh.aspx',
                                 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
                                 'Accept': '*/*',
                                 'Accept-Encoding': 'gzip, deflate, br',
                                 'Accept-Language': 'en-US,en;q=0.5'
                             }
                             )

    def parse_response(self, response):
        for table in response.css("table#tableHoGiaDinh")[0:]:
            self.log(table.css('td::text').getall())
