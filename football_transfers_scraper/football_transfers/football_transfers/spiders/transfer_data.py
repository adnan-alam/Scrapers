import logging
import scrapy
from football_transfers.football_transfers.items import FootballTransfersItem


logger = logging.getLogger(__name__)


class TransferDataSpider(scrapy.Spider):
    name = "transfer_data_spider"
    allowed_domains = ["footballtransfers.com"]
    start_urls = [
        "https://www.footballtransfers.com/en/statistics/players/actions/future-star-football-players"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, body="page=1&pageItems=25")

    def parse(self, response):
        json_data = response.json()
        total_pages = json_data.get("pages")

        for page_num in range(1, total_pages + 1):
            yield scrapy.Request(
                self.start_urls[0],
                callback=self.parse_data,
                body=f"page={page_num}&pageItems=25",
            )

    def parse_data(self, response):
        json_data = response.json()
        records_data_list = json_data.get("records", [])

        for record_data_dict in records_data_list:
            data_dict = record_data_dict.copy()
            data_dict.pop("id")
            player_img_url = data_dict.pop("player_picture")
            team_img_url = data_dict.pop("team_picture")
            image_urls = [player_img_url, team_img_url]

            item = FootballTransfersItem()
            item["data_dict"] = data_dict
            item["image_urls"] = image_urls
            yield item
