# spider 项目简介

DFS 与 BFS 的背后用到的数据结构是栈与队列。

这里我利用 DFS 与 BFS的知识写了一个网络爬虫。当我们请求一个 URL 链接时会得到一个 HTML 文档，而在这个 HTML 文档中又会包含 URL 链接，这样利用 DFS 与 BFS 算法就可以不断搜集互联网信息。

本项目搜集了豆瓣图书信息，包括书籍名，书籍评分，评价人数，评论树，读过的人数，书籍链接。



# 依赖安装

本项目用 python 语言编写，用到的第三方库：

- requests: 网络请求库
- selenim: 无头浏览器，没有图行界面的浏览器，在代码里用的多。
- 浏览器 Driver: selenim 依赖具体的浏览器 driver, 例如谷歌浏览器依赖`chromedriver`，下载地址：https://pypi.org/project/selenium/4.0.0.b1/
- 在程序第 22 行指定你下载，解压后的驱动文件即可。

install selenim:

```sh
pip install selenium requests
```


## 目录结构

- book_infos.csv: 用于存储搜集到的书籍信息。
- book_infos_example.csv: 一些搜集到的书籍信息例子。
- main.py：爬虫程序。
- README.md：本说名文档。



##  使用方法

```shell
python -m main
```



## 程序说明

体现 DFS 与 BFS 的代码在第 80 与 81 行：

- set 是集合数据结构，一方面用于保存已访问过的链接，另一方面保证每个链接只访问一次。
- deque 是双端队列，如果是先进先出就是 BFS，如果是后进先出就是 DFS。

程序第 85 行：`open_links.popleft()` 与 程序第 95 行：`open_links.append()`说明本程序用的是先进先出队列，即 BFS。

## 附注

selenim 使用实例：

```pyton
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')
driver.get("https://www.ebay.com/itm/Dyson-V7-Fluffy-HEPA-Cordless-Vacuum-Cleaner-Blue-New/273976851242")

title = driver.find_element_by_xpath('//h1')
current_price = driver.find_element_by_xpath("//span[@id='prcIsum']")
image = driver.find_element_by_xpath("//img[@id='icImg']")

product_data = {
	'title': title.text,
	'current_price': current_price.get_attribute('content'), 
	'image_url': image.get_attribute('src')
}

print(product_data)
driver.quit()
```

