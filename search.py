"""这个python文件的目的是通过playwright包进行自动化搜索b站视频"""
import asyncio  # python异步库
import re       # python正则表达式库
import time

from playwright.async_api import async_playwright # 导入playwright异步自动化库
from bs4 import BeautifulSoup                     # 导入解析库BeauifulSoup


async def run(playwright, content):
    """主要逻辑"""
    browser = await playwright.chromium.launch(headless=True)
    # 初始化浏览器对象

    context = await browser.new_context()
    # 初始化BrowserContext对象

    page = await context.new_page()
    await page.goto("https://www.bilibili.com/")
    # 打开一个标签页，请求b站
    
    pattern = '<input class="nav-search-input" type="text" autocomplete="off" accesskey="s" maxlength="100" x-webkit-speech="" x-webkit-grammar="builtin:translate" value="" placeholder="(.*?)"'
    search = re.findall(pattern, await page.content())[0]
    await page.get_by_placeholder(search).click()
    await page.get_by_placeholder(search).fill(content)
    async with page.expect_popup() as page1_info:
        await page.get_by_placeholder(search).press("Enter")
        page1 = await page1_info.value
    # 搜索查找内容
    
    time.sleep(5)
    # 等待加载

    soup = BeautifulSoup(await page1.content(), "html.parser")
    # 初始化解析类

    a_list = soup.find_all("a")
    # print(a_list)
    # 找到所有a节点
    href_list = []
    # 初始化href属性列表

    for a in a_list:
        href = a.get("href")
        # print(href)
        # 得到所有a节点的href属性
        try:
            if href.startswith('//www.bilibili.com/video/'):
                # 仅仅获取b站视频链接
                href_list.append(href)
                # print(href_list)
                # 加入href_list
        except AttributeError:
            # href属性有可能是None， 所以需要捕获AttributeError异常
            pass
        except:
            # 顺便捕获其他任何异常
            pass

    time.sleep(5)

    await context.close()
    await browser.close()
    # 关闭浏览器和标签页，四方资源

    return href_list
    # 返回href_list，共其他函数使用


async def main(search_content):
    """主函数"""
    async with async_playwright() as playwright:
        return await run(playwright, search_content)

# asyncio.run(main("极客湾"))