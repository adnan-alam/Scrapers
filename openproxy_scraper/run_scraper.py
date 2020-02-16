import json
import logging
import os
import random
import sys
import time


logging.basicConfig(
    filename="scraper.log", level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(filename)s : %(lineno)d : %(message)s"
)


try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as e:
    logging.exception(e)
    msg = "Selenium not installed !"
    print(msg)
    logging.info(msg)
    sys.exit(1)


with open("user_agents.txt", "r") as f:
    user_agents = f.readlines()
    user_agents = [i.strip().strip("\n") for i in user_agents]
user_agent = random.choice(user_agents)


# chrome driver settings
chrome_path = os.path.join(os.getcwd(), "chromedriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent={}".format(user_agent))
chrome_options.add_argument("headless")
chrome_options.add_argument("disable-logging")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_path)


def get_data():
    data_list = []

    try:
        driver.get("https://openproxy.space/list")
        footer = driver.find_element_by_tag_name("footer")
        driver.execute_script("arguments[0].scrollIntoView();", footer)
        webdriver_wait = WebDriverWait(driver, 30)
        a_tags = webdriver_wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list")))
        proxy_pages_urls = []
        if a_tags:
            a_tags = a_tags[:5]
            for tag in a_tags:
                title = tag.find_element_by_class_name("title").find_element_by_tag_name("span").text
                if title in ("No Title", "FRESH SOCKS5", "FRESH SOCKS4", "FRESH HTTP/S"):
                    url = tag.get_attribute("href")
                    proxy_pages_urls.append(url)

        if proxy_pages_urls:
            msg = "Scraping proxies ..."
            print(msg)
            logging.info(msg)

            for page_url in proxy_pages_urls:
                driver.get(page_url)
                proxies = driver.find_elements_by_class_name("data")
                if proxies:
                    protocols = []
                    anonimity = []
                    last_updated_date, timeout, privacy = [""] * 3

                    proxies_list = proxies[0].find_element_by_tag_name("textarea").text.strip().split()
                    protocols_anonimity = driver.find_elements_by_class_name("pa")
                    if protocols_anonimity:
                        protocols_anonimity = protocols_anonimity[0]
                        protocols_anonimity_divs = protocols_anonimity.find_elements_by_tag_name("div")
                        for div in protocols_anonimity_divs:
                            p_text = div.find_element_by_tag_name("p").text.strip()
                            if "Protocols" == p_text:
                                protocol_span_list = div.find_elements_by_tag_name("span")
                                if protocol_span_list:
                                    protocols = [i.text.strip() for i in protocol_span_list]
                            elif "Anons" == p_text:
                                anonimity_span_list = div.find_elements_by_tag_name("span")
                                if anonimity_span_list:
                                    anonimity = [i.text.strip() for i in anonimity_span_list]

                    details_div = driver.find_elements_by_class_name("details")
                    if details_div:
                        details_div = details_div[0]
                        item_divs = details_div.find_elements_by_class_name("item")
                        last_updated_date = item_divs[0].find_elements_by_tag_name("span")[-1].text
                        timeout = item_divs[1].find_elements_by_tag_name("span")[-1].text
                        privacy = item_divs[2].find_elements_by_tag_name("span")[-1].text

                    data_dict = {
                        "protocols": protocols,
                        "anonimity": anonimity,
                        "proxies": proxies_list,
                        "last_updated_date": last_updated_date,
                        "timeout": timeout,
                        "privacy": privacy,
                    }
                    data_list.append(data_dict)
                time.sleep(5)
    except Exception as e:
        logging.exception(e)
    return data_list


def get_output(data_list):
    file_path = "proxies.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4)

    msg = "Scraped data saved as: {}".format(file_path)
    print(msg)
    logging.info(msg)


if __name__ == "__main__":
    msg = "Scraper initialized ..."
    print(msg)
    logging.info(msg)

    try:
        data_list = get_data()
        if data_list:
            try:
                get_output(data_list)
            except Exception as e:
                logging.exception(e)
        else:
            msg = "No scraped data to write in the output file."
            print(msg)
            logging.info(msg)
    except Exception as e:
        logging.exception(e)

    try:
        driver.close()
        driver.quit()
    except Exception as e:
        logging.exception(e)

    msg = "Scraper stopped."
    print(msg)
    logging.info(msg)
