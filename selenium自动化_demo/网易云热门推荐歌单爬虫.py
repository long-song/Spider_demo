# 1.导入模块
from selenium import webdriver
import time
import os


class WangYiYun_Hot:
    def __init__(self):
        self.start_url = "https://music.163.com/"  # 所有歌单分类网址
        self.driver = webdriver.Chrome(executable_path="e:\chromedriver.exe")  # 调用webdriver的Chrome()方法得到浏览器对象

    # 提取歌单分类数据
    def get_data_cat(self):
        # 点击热门推荐-更多
        self.driver.switch_to.frame("g_iframe")
        self.driver.find_elements_by_link_text("更多")[0].click()
        time.sleep(1)
        # 当前页面的内容在一个id为"g_iframe"的iframe中，因此需要先定位到这个iframe再进行查找元素
        self.driver.refresh()
        self.driver.switch_to.frame("g_iframe")
        # 获取所有歌单分类
        list = self.driver.find_elements_by_class_name("s-fc1 ")
        # 将所有歌单分类data-cat组成列表
        data_cat = [cat.get_attribute("data-cat") for cat in list]
        # print("所有分类:",data_cat)
        # print("分类总数量:",len(data_cat))

        # 如果没有网易云歌单文件夹，则创建
        if not os.path.exists("网易云歌单"):
            os.mkdir("网易云歌单")
        for cat in data_cat:
            with open("网易云歌单/{}类型的歌单信息.txt".format(cat), 'a+', encoding="utf-8") as f:
                f.write("图片，标题，播放量，链接地址，发布者, 发布者用户信息链接\n")
                offset = 0  # 定义url中的页码规律的变量
                while True:
                    # 根据cat和offset参数获取所有页码url
                    url_new = "https://music.163.com/#/discover/playlist/?order=hot&cat={}&limit=35&offset={}".format(
                        cat,
                        offset)
                    # 根据url_new打开新窗口获取数据
                    js = 'window.open("{}");'.format(url_new)
                    self.driver.execute_script(js)  # 执行js
                    handles = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
                    # print(handles)
                    self.driver.switch_to.window(handles[-1])  # 打开最后一个窗口

                    # 获取本页歌单数量
                    self.driver.switch_to.frame("g_iframe")
                    li_list = self.driver.find_elements_by_xpath("//ul[@id='m-pl-container']/li")

                    # 获取歌单图片，标题，播放量，链接地址，发布者, 发布者用户信息链接
                    for li in li_list:
                        image = li.find_element_by_xpath(".//div/img").get_attribute("src")  # 获取专辑图片
                        title = li.find_element_by_xpath(".//div/a").get_attribute("title")  # 获取专辑标题
                        number = li.find_element_by_xpath(".//div/div/span[2]").text  # 获取专辑播放量
                        music = li.find_element_by_xpath(".//div/a").get_attribute("href")  # 获取专辑链接地址
                        user = li.find_element_by_xpath(".//p[2]/a").get_attribute("title")  # 获取专辑发布者
                        userinfo = li.find_element_by_xpath(".//p[2]/a").get_attribute("href")  # 获取专辑发布者用户信息链接
                        str = ','.join([image, title, number, music, user, userinfo])
                        # print(str)
                        f.write(str + "\n")  # 将数据追加写入txt
                    page = offset / 35 + 1
                    print("{}类别 第{}页 {}张歌单写入成功".format(cat, int(page), len(li_list)))
                    self.driver.close()  # 关闭当前窗口
                    self.driver.switch_to.window(handles[0])  # 切换回第一句柄窗口,目的是继续执行当前窗口的js代码，否则无法执行
                    offset += 35  # 改变offset参数数值
                    # 如果本页获取不到数据则停止获取此类歌单信息
                    if len(li_list) == 0:
                        break

    # 根据分类获取歌单信息，并循环翻页
    def get_song_list(self):
        data_cat = self.get_data_cat()

    def run(self):
        # 1.发送请求
        self.driver.get(self.start_url)
        # 将窗口最大化
        self.driver.maximize_window()
        # 2.提取歌单分类数据
        self.get_data_cat()
        # # 3.根据分类获取歌单信息，并循环翻页
        # self.get_song_list()
        # 休眠3秒
        time.sleep(3)
        # 关闭浏览器
        self.driver.quit()


if __name__ == "__main__":
    hot = WangYiYun_Hot()
    hot.run()
