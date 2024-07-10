"""这个python文件的目的是写一个入口文件"""
import asyncio    #导入异步库
from sys import exit  # 导入退出函数
from urllib.parse import urljoin # 导入url连接函数

# from bv_id import BvId
import sync_download_video # 导入下载函数
import search # 导入搜索函数


async def main():
    """该函数的目的是写一个命令行接口"""
    print("Welcome to download bilibili video tool!")
    # print('Type "a" start async download(test).')
    print('Type "s" start sync download.')
    print('Type "one" start download one video.')
    # print('Type "bvid" start search by bvid(test).')
    print('Type "0" exit.')
    while True:
        choose = input("<<")
        if choose == "a":
            """await async_main()"""
        elif choose == "s":
            await sync_main()
        elif choose == "one":
            one()
        elif choose == "bvid":
            """bvid()"""
        elif choose == "0":
            exit()


"""async def async_main():
    content = input("Please type search content >>")
    urls = await search.main(content) 
    task_list = []
    for n in range((6 * 6)):
        task = sync_download_video.main(urls[n])
        task_list.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)"""


async def sync_main():
    """"这个函数的目的是调用下载函数，下载指定b站内容"""
    content = input("Please type search content>>")
    if content == "q":
        # 如果用户输入q，返回主函数
        return
    urls = await search.main(content)  # search.main()是个异步函数，返回页面url列表
    # print(urls)
    for url in urls:
        # 遍历url列表
        if not url.startswith("https"):
            # 如果url并不是完整url
            url = urljoin("https:", url)
            # 那么用urljoin函数将其补充完成
        sync_download_video.main(url)
        # 调用下载函数，下载视频


def one():
    """该函数的目的是下载一个指定视频"""
    try:
        url = input("Please type website >>")
        if content == "q":
        # 如果用户输入q，返回主函数
            return
        # 因为下载指定视频，所以要获取url
        sync_download_video.main(url)
        # 直接调用函数
    except:
        # 一旦发生异常，返回主函数
        return


"""def bvid():
    page_bvid = BvId(input("Please type bvid >>"))
    sync_download_video.main(page_bvid)"""



if __name__ == "__main__":
   asyncio.run(main())
