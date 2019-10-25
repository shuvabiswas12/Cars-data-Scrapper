from selenium import webdriver
from parsel import Selector
from time import sleep

import csv


file_name = "report-5.csv"
row = ['Car-Name', 'Engine', 'Image', 'MPG', 'Seating', 'Transmission', 'Power', 'Drivetrain', 'Features']
writer = csv.writer(open(file_name, 'w+'))
writer.writerow(row)


class Spider():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.sel = None
        self.cars = ['MINI', 'MISC', 'Mitsubishi', 'Morgan', 'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac', 'Porsche', 'RAM', 'Rolls-Royce']
        sleep(2)
        self.car_data = {}

    def startRequest(self, url=None):
        for car in self.cars:
            url = 'https://www.autoblog.com/'
            url += car

            self.driver.get(url)
            sleep(5)
            self.sel = Selector(text=self.driver.page_source)
            cars_url = self.sel.xpath(
                '//div[@class="slick-track"]//div//a[@class="card"]/@href').extract()
            for url in cars_url:
                full_url = 'https://www.autoblog.com' + url
                self.gettingScraped(url=full_url)

    def gettingScraped(self, url=None):
        self.driver.get(url)
        sleep(5)
        self.sel = Selector(text=self.driver.page_source)

        car_name = self.sel.xpath('//header/h1/span/text()').extract_first()
        image = self.sel.xpath(
            '//div[@class="slider masthead-photo"]/img[@class="lazy"]/@src').extract_first()
        engine = self.sel.xpath(
            '//div[@class="overview-specs"]/table//tr[@class="engine"]//td[2]/text()').extract_first()
        mpg = self.sel.xpath(
            '//div[@class="overview-specs"]/table//tr[@class="mpg"]//td[2]/text()').extract_first()
        seating = self.sel.xpath(
            '//div[@class="overview-specs"]/table//tr[@class="seating"]//td[2]/text()').extract_first()
        transmission = self.sel.xpath(
            '//div[@class="overview-specs"]/table//tr[@class="transmission"]//td[2]/text()').extract_first()
        power = self.sel.xpath(
            '//div[@class="overview-specs"]/table//tr[@class="power"]//td[2]/text()').extract_first()
        drivetrain = self.sel.xpath(
            '//div[@class="overview-specs"]/table//tr[@class="drivetrain"]//td[2]/text()').extract_first()
        features = self.sel.xpath(
            '//div[@class="features col-tn-12 col-sm-5"]/h4[contains(text(), "Features")]/following-sibling::ul//li/text()').extract()

        data = {
            'Car-Name': car_name,
            'Engine': engine,
            'Image': image,
            'MPG': mpg,
            'Seating': seating,
            'Transmission': transmission,
            'Power': power,
            'Drivetrain': drivetrain,
            'Features': features,
        }

        print(data, '\n')

        writer.writerow([car_name, engine, image, mpg, seating,
                         transmission, power, drivetrain, features])
        sleep(2)

    def closeDriver(self):
        self.driver.quit()


spider = Spider()
spider.startRequest()
sleep(2)
spider.closeDriver()
