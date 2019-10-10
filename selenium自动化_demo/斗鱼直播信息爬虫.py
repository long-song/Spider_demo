import time
from selenium import webdriver

class DouYuSpider:
    def __init__(self):
        self.start_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome(executable_path="e:\chromedriver.exe")

    def get_content_list(self):
        self.driver.maximize_window()
        li_list = self.driver.find_elements_by_xpath("//*[@id='listAll']/section[2]/div[2]/ul/li")
        for li in li_list:
            item = {}
            item["room_name"] = li.find_element_by_xpath("./div/a[1]/div[2]/div[1]/h3").get_attribute("title")
            item["game_name"] = li.find_element_by_xpath("./div/a[1]/div[2]/div[1]/span").text
            item["user_name"] = li.find_element_by_xpath(".//div/a[1]/div[2]/div[2]/h2").text
            # item["image"] = li.find_element_by_xpath(".//img[@class='DyImg-content is-normal ']").get_attribute("src")
            item["hot"] = li.find_element_by_xpath(".//span[@class='DyListCover-hot']").text
            print(item)


    def run(self):
        # 1.发送请求
        self.driver.get(self.start_url)
        # 2.提取数据
        while True:
            self.get_content_list()
            next = self.driver.find_element_by_xpath(
                "//*[@id='listAll']/section[2]/div[2]/div/ul/li[9]")
            if next.get_attribute('class') != "dy-Pagination-disabled dy-Pagination-next":
                 next.click()
            else:
                break
            time.sleep(1)

if __name__ == "__main__":
    douyu = DouYuSpider()
    douyu.run()