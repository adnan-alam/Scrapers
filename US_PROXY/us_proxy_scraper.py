import json
import logging
import os
import subprocess
import sys


logging.basicConfig(
    filename="scraper.log", level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

try:
    from selenium import webdriver
except ImportError:
    logging.exception("Selenium not installed. Installing...")
    subprocess.call(["pip", "install", "selenium"])
    sys.exit(1)


# chrome driver settings
chrome_path = os.path.join(os.getcwd(), "chromedriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
chrome_options.add_argument("disable-logging")
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_path)


def get_data():
    msg = "Scraper initialized ..."
    print(msg)
    logging.info(msg)

    data_list = []
    count = 0

    try:
        driver.get("https://www.us-proxy.org/")
        while True:
            table = driver.find_element_by_id("proxylisttable")
            tbody = table.find_element_by_tag_name("tbody")
            tr_list = tbody.find_elements_by_tag_name("tr")
            td_list = [tr.find_elements_by_tag_name("td") for tr in tr_list]
            for li in td_list:
                ip_address = li[0].text
                port = li[1].text
                anonymity = li[4].text
                https = li[6].text
                data_dict = {
                    "ip_address": ip_address,
                    "port": port,
                    "anonymity": anonymity,
                    "https": https,
                }
                data_list.append(data_dict)
                count += 1
                print("IP Address scraped: {}".format(count), end="\r")

            next_btn = driver.find_element_by_id("proxylisttable_next")
            next_btn_cls = next_btn.get_attribute("class")
            if "disabled" not in next_btn_cls:
                next_btn_a_tag = next_btn.find_element_by_tag_name("a")
                driver.execute_script("arguments[0].click();", next_btn_a_tag)
            else:
                break
    except Exception as e:
        logging.exception(e)

    msg = "Total scraped data: {}".format(count)
    print(msg)
    logging.info(msg)

    return data_list


def get_output(data_list):
    file_path = "proxies.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4)

    msg = "Scraped data saved as - {}".format(file_path)
    print(msg)
    logging.info(msg)


if __name__ == "__main__":
    try:
        data_list = get_data()
        if data_list:
            get_output(data_list)
        else:
            msg = "No scraped data to write in output file"
            print(msg)
            logging.info(msg)
    except Exception as e:
        logging.exception(e)

    try:
        driver.close()
        driver.quit()
    except Exception as e:
        logging.exception(e)
