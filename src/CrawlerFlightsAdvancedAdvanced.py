import asyncio
import aiohttp
from lxml import etree
import pandas as pd
import numpy as np
from tqdm.asyncio import tqdm  # 异步版本的进度条


# 请求头和Cookies配置
cookies = {
    '_RDG': '289fda7de3273426211d373ea0161b1ef2',
    '_RGUID': 'f09ac836-d3f1-4c04-8d4b-de170ffcd0d5',
    '_RSG': '4mKyJR3oQ2FL3D_FSXtBr8',
    'MKT_CKID': '1622443083256.9m8qg.vewg',
    '_ga': 'GA1.2.707014534.1622443083',
    'GUID': '09031042214511715343',
    'nfes_isSupportWebP': '1',
    '_bfaStatusPVSend': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22%24device_id%22%3A%2217fb6f458bde18-07dae8d00d6fe-9771a3f-1296000-17fb6f458be72d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fapp.mokahr.com%2F%22%2C%22%24latest_referrer_host%22%3A%22app.mokahr.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D',
    '__zpspc': '9.25.1657444518.1657444870.4%233%7Ccn.bing.com%7C%7C%7C%7C%23',
    'Session': 'SmartLinkCode=51cto&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=blog.51cto.com&SmartLinkLanguage=zh',
    '_RF1': '139.226.176.169',
    '_bfa': '1.1622443080329.1gik74.1.1709048025895.1709048029542.34.2.101021',
    '_ubtstatus': '%7B%22vid%22%3A%221622443080329.1gik74%22%2C%22sid%22%3A34%2C%22pvid%22%3A2%2C%22pid%22%3A101021%7D',
    '_bfaStatus': 'success',
    '_jzqco': '%7C%7C%7C%7C1710593260804%7C1.624638678.1708529546739.1709135182955.1710593260691.1709135182955.1710593260691.0.0.0.22.22',
}

headers = {
    'authority': 'flights.ctrip.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}


# 异步请求函数
async def fetch(session, url, **kwargs):
    async with session.get(url, **kwargs) as response:
        return await response.text()

# 获取所有机场及一级页面链接（保持不变）
async def flight_departure():
    url = 'https://flights.ctrip.com/schedule'
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        page_text = await fetch(session, url)
        tree = etree.HTML(page_text)
        flight_name = tree.xpath("//div[@class='m']/a/text()")
        flight_link = tree.xpath("//div[@class='m']/a/@href")
    print("共获取到", len(flight_name), "机场数！！")
    return flight_name, flight_link

# 获取机场之间的往返航班记录
async def flight_dep_arr(flight_name, flight_link):
    flight_name_2 = {}  # 存储出发-到达的记录
    flight_link_2 = []  # 存储出发-到达的航班明细网页的链接
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = []
        for i in range(len(flight_name)):
            url = 'https://flights.ctrip.com' + flight_link[i]
            tasks.append(fetch(session, url))

        results = await tqdm.gather(*tasks, desc="爬取机场往返记录")
        for i, page_text in enumerate(results):
            tree = etree.HTML(page_text)
            name = tree.xpath("//div[@class='m']/a/text()")
            link = tree.xpath("//div[@class='m']/a/@href")
            flight_name_2[flight_name[i]] = name
            flight_link_2.extend(link)

    return flight_name_2, flight_link_2

# 获取详细航班数据
async def flight_dep_arr_detail(flight_link_2):
    df = pd.DataFrame(columns=np.arange(25))  # 初始化 DataFrame
    url = 'https://flights.ctrip.com/schedule/getScheduleByCityPair'
    rows = []

    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = []
        for link in flight_link_2:
            for num in range(10):  # 最多爬取 10 页
                ploy_data = {
                    "departureCityCode": link.split("/")[-1].split(".")[0].upper(),
                    "arriveCityCode": link.split(".")[-2].upper(),
                    "pageNo": num + 1,
                    "departDate": "2024-02-26",
                }
                tasks.append(session.post(url, json=ploy_data))

        responses = await tqdm.gather(*tasks, desc="爬取航班详细记录")
        for response in responses:
            try:
                json_data = await response.json()
            except:
                continue

            for z in range(len(json_data.get('scheduleVOList', []))):
                values = []
                for key, value in json_data.get('scheduleVOList')[z].items():
                    if key == "currentWeekSchedule":
                        for x, y in value.items():
                            values.append(y)
                    else:
                        values.append(value)
                rows.append(values)

    # 如果有数据，则合并到 DataFrame
    if rows:
        df = pd.concat([df, pd.DataFrame(rows, columns=df.columns)], ignore_index=True)
    return df

# 主函数执行
async def main():
    flight_name, flight_link = await flight_departure()
    flight_name_2, flight_link_2 = await flight_dep_arr(flight_name, flight_link)
    df = await flight_dep_arr_detail(flight_link_2)
    df.to_excel('全国主要机场航班数据.xlsx', header=True)
    print("数据已保存到 '全国主要机场航班数据.xlsx' 文件中。")

# 启动异步任务
if __name__ == "__main__":
    asyncio.run(main())
