from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
import jieba


# https://www.writebug.com/
# https://www.oschina.net/   #开源中国
# https://www.infoq.cn/
# 需要下载驱动 以下为驱动位置


def get_results(key):
    database = []
    urlbase = []
    infos = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    headers = {'User-Agent': user_agent}
    s = Service("E://chromedriver.exe")
    # 验证成功
    driver = webdriver.Chrome(service=s)
    # csdn 搜索网站

    wait = WebDriverWait(driver, 10)
    driver.get('https://so.csdn.net/so/search?q=' + key + '&t=&u=')
    # https://so.csdn.net/so/search?q=python&t=&u=
    #   driver.find_element_by_link_text("page='i'")
    # 等待第一次的列表项目全部加载完
    # driver.find_element(By.ID, "keyword").send_keys(key, Keys.RETURN)
    # for i in range(3):
    name_results = wait.until(presence_of_all_elements_located((By.XPATH, "//*[@class='title substr']")))

    # 某些特定关键字第一项的样式不一样 特别处理后添加到列表里
    first_result = None
    try:
        first_result = driver.find_element(By.XPATH, "//*[@class='title substr flex align-items-center']")
    except:
        print("no_first")
    # btm-dig
    url_results = driver.find_elements(By.XPATH, "//a[@class='block-title']")
    # agree_results = driver.find_elements("title substr")
    agree_results = driver.find_elements(By.XPATH, "//*[@class='btm-dig']")

    if first_result != None:
        name_results.insert(0, first_result)

    for i in range(len(name_results)):
        # print(name_results[i].text)
        # database.append(name_results[i].text)
        # urlbase.append(url_results[i].get_attribute('href') + '\n')
        infos.append({'title': name_results[i].text,
                      'url': url_results[i].get_attribute('href'),
                      'source': 'csdn',
                      'keyword': key})

    print('分割线')
    driver = webdriver.Chrome(service=s)  # 下一个网站f
    # csdn 搜索网站
    driver.get('https://s.geekbang.org/search/c=0/k=' + key + '/t=')
    wait = WebDriverWait(driver, 10)
    name_results2 = wait.until(presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'xie.infoq.cn')]")))
    url_results2 = driver.find_elements(By.XPATH, "//a[contains(@f_c,'3')]")

    for i in range(len(name_results2)):
        # print(name_results2[i].text)
        # database.append(name_results2[i].text)
        # urlbase.append(url_results2[i].get_attribute('href') + '\n')
        infos.append({'title': name_results2[i].text,
                      'url': url_results2[i].get_attribute('href'),
                      'source': '极客帮',
                      'keyword': key})
    print('分割线')
    driver = webdriver.Chrome(service=s)  # 下一个网站
    # csdn 搜索网站
    driver.get('https://juejin.cn/search?query=' + key)
    wait = WebDriverWait(driver, 10)
    name_results3 = wait.until(presence_of_all_elements_located((By.XPATH, "//*[@class='info-row title-row']")))
    url_results3 = driver.find_elements(By.XPATH, "//a[@class='entry-link']")

    for i in range(len(name_results3)):
        infos.append({'title': name_results3[i].text,
                      'url': url_results3[i].get_attribute('href'),
                      'source': '掘金',
                      'keyword': key})
    driver.close()
    driver.quit()

    for i in range(len(infos)):
        print(infos[i].get('title'))
        print(infos[i].get('url'))

    words = []
    for i in range(len(infos)):
        word_ex = jieba.lcut(infos[i].get('title'))
        words = words + word_ex
    # print(words)
    count = {}
    for word in words:  # 使用 for 循环遍历每个词语并统计个数
        if len(word) < 2:  # 排除单个字的干扰，使得输出结果为词语
            continue
        else:
            count[word] = count.get(word, 0) + 1  # 如果字典里键为 word 的值存在，则返回键的值并加一，如果不存在键word，则返回0再加上1

    exclude = ["可以", "一起", "这样", "..."]  # 建立无关词语列表
    for key in list(count.keys()):  # 遍历字典的所有键，即所有word
        if key in exclude:
            del count[key]  # 删除字典中键为无关词语的键值对

    listdata = list(count.items())  # 将字典的所有键值对转化为列表
    listdata.sort(key=lambda x: x[1], reverse=True)  # 对列表按照词频从大到小的顺序排序

    data_analysis = []

    counts = 15
    if len(listdata) < 15:
        counts = len(listdata)

    for i in range(counts):
        word, number = listdata[i]
        data_analysis.append({'word': word,
                              'number': number})

    results = {
        'infos': infos,
        'data_analysis': data_analysis
    }
    return results
