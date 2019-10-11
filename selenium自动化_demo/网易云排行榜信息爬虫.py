# 1.导入模块
from selenium import webdriver
import time
import os


class WangYiYun_Rank:
    def __init__(self):
        self.start_url = "https://music.163.com/"  # 所有歌单分类网址
        self.driver = webdriver.Chrome(executable_path="e:\chromedriver.exe")  # 调用webdriver的Chrome()方法得到浏览器对象

    # 提取提取所有榜单
    def get_rank_list(self):
        # 点击排行榜
        self.driver.find_element_by_xpath("//*[@id='g_nav2']/div/ul/li[2]/a").click()
        # 当前页面的内容在一个id为"g_iframe"的iframe中，因此需要先定位到这个iframe再进行查找元素
        self.driver.refresh()
        self.driver.switch_to.frame("g_iframe")
        # 获取所有榜单位置列表
        list = self.driver.find_elements_by_xpath("//div[@class='item f-cb']")

        # 将所有榜单logo,name,链接，更新状况组成列表
        rank_list = [(rank.find_element_by_xpath('.//div/a/img').get_attribute('src'),
                      rank.find_element_by_xpath('.//div/a/img').get_attribute('alt'),
                      rank.find_element_by_xpath('.//p[1]/a').get_attribute('href'),
                      rank.find_element_by_xpath('.//p[2]').text) for rank in list]
        # print("所有榜单:",rank_list)
        # print("榜单总数量:",len(rank_list))
        if not os.path.exists("网易云榜单"):
            os.mkdir("网易云榜单")
        for cat in rank_list:
            name = cat[1]
            url = cat[2]
            with open("网易云榜单/{}的歌曲信息.txt".format(name), 'a+', encoding="utf-8") as f:
                f.write("排名，歌曲，时长，歌手\n")
                # 根据url打开新窗口获取数据
                js = 'window.open("{}");'.format(url)
                self.driver.execute_script(js)  # 执行js
                handles = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
                # print(handles)
                self.driver.switch_to.window(handles[-1])  # 打开最后一个窗口

                # 获取榜单列表
                self.driver.switch_to.frame("g_iframe")
                tr_list = self.driver.find_elements_by_xpath("//table[@class='m-table m-table-rank']/tbody/tr")
                for tr in tr_list:
                    num = tr.find_element_by_xpath(".//td[1]/div/span").text
                    song = tr.find_element_by_xpath(".//td[2]/div/div/div/span/a/b").get_attribute('title')
                    time = tr.find_element_by_xpath(".//td[3]/span").text
                    songer = tr.find_element_by_xpath(".//td[4]/div").get_attribute('title')
                    str = ','.join([num, song, time, songer])
                    # print(str)
                    f.write(str + "\n")  # 将数据追加写入txt
                print("{}写入成功".format(name))
                self.driver.close()  # 关闭当前窗口
                self.driver.switch_to.window(handles[0])  # 切换回第一句柄窗口,目的是继续执行当前窗口的js代码，否则无法执行


    def run(self):
        # 1.发送请求
        self.driver.get(self.start_url)
        # 将窗口最大化
        self.driver.maximize_window()
        # 2.提取所有榜单
        self.get_rank_list()
        # 休眠3秒
        time.sleep(3)
        # 关闭浏览器
        self.driver.quit()


if __name__ == "__main__":
    douyu = WangYiYun_Rank()
    douyu.run()
