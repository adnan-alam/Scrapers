import logging
from sqlalchemy.orm import sessionmaker
from football_transfers.models import FutureStar, db_engine


logger = logging.getLogger()


class FutureStarDataPipeline:
    def __init__(self):
        # Initializes database connection and session
        try:
            self.engine = db_engine
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            logger.exception(e)

    def save_player_data(self, item):
        try:
            scraped_data_dict = item["data_dict"]
            data_to_save = FutureStar(**scraped_data_dict)

            session = self.Session()
            session.add(data_to_save)
            session.commit()
        except Exception as e:
            session.rollback()
            msg = "ROLLBACK! {}".format(e)
            logger.exception(msg)
        finally:
            session.close()

    def process_item(self, item, spider):
        self.save_player_data(item)
        return item
