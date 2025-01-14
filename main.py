import time
import urllib.parse

from lxml import html
from selenium import webdriver

URL = "https://www.target.com/s?searchTerm={}"


def chrome_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_page_items(tree) -> list:
    container = tree.xpath("//section[contains(@class, 'sc-e0eaa558-1 haoIOG')]")
    if container:
        return container[0].xpath(".//div[@class='sc-5da3fdcc-0 ksJpxP']/div")
    else:
        return []


def create_search_record(item):
    description = "".join(item.xpath(".//div[@class='styles_truncate__Eorq7 sc-4d32bc34-0 kkvIvZ']/text()"))
    price = "".join(item.xpath(".//span[@data-test='current-price']/span/text()"))
    reviews = "".join(item.xpath(".//span[@class='sc-94776d85-1 ickohb']/text()"))
    url = f"https://www.target.com{"".join(item.xpath(".//a[@class='sc-e851bd29-0 sc-f76ad31b-1 hNVRbT dpaMdN h-display-block ']/@href"))}"
    return description, price, reviews, url


def scroll_the_page(driver, scroll_amount=200):
    scroll_amount = scroll_amount  # Pixels to scroll each time
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(0.2)  # Pause for a short time

        # Check if we've reached the bottom of the page
        scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
        page_height = driver.execute_script("return document.body.scrollHeight")
        if scroll_position >= page_height:
            break


def get_number_of_pages(tree) -> int:
    num_pages = "".join(tree.xpath('//*[@id="select-custom-button-id"]/span/text()')).split()[3]
    return int(num_pages)


def scrape_target(keywords: str):
    url = URL.format(keywords.replace(" ", "-"))
    driver = chrome_webdriver()
    driver.get(url)
    time.sleep(2)
    scroll_the_page(driver, 200)
    time.sleep(2)
    tree = html.fromstring(driver.page_source)
    page_data = list()

    num_pages = get_number_of_pages(tree)
    nao_query = 0

    for num in range(num_pages):
        items = get_page_items(tree)
        if not items:
            break

        for item in items:
            record = create_search_record(item)
            if record[0] or record[1]:
                page_data.append(record)

        if num >= (num_pages-1):
            driver.close()
            break

        nao_query += 24
        driver.get(f"{url}&Nao={nao_query}")
        time.sleep(2)
        scroll_the_page(driver)
        time.sleep(2)
        tree = html.fromstring(driver.page_source)


if __name__ == '__main__':
    scrape_target("dell laptop")
