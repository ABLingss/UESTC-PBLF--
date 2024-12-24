import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

header = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'cookie': 'MKT_CKID=1730292097710.vfe09.t0j5; GUID=09031067118870597256; _RF1=58.20.33.185; _RSG=4oa3uKRszKEoheoV0XxD9A; _RDG=288a7d6c60cccb26a132310ea7062d44d5; _RGUID=e53dd9b5-380e-4c84-a24d-ee101fca8af2; _bfaStatusPVSend=1; _bfa=1.1730292107919.48jemx.1.1730511239226.1730511263081.4.2.101021; _ubtstatus=%7B%22vid%22%3A%221730292107919.48jemx%22%2C%22sid%22%3A4%2C%22pvid%22%3A2%2C%22pid%22%3A101021%7D; _jzqco=%7C%7C%7C%7C1730459716543%7C1.1303622818.1730292097712.1730511238884.1730511263120.1730511238884.1730511263120.0.0.0.53.53; _bfi=p1%3D101021%26p2%3D101021%26v1%3D2%26v2%3D1; _bfaStatus=success',
    'origin': 'https://flights.ctrip.com',
    'priority': 'u=1, i',
    'referer': 'https://flights.ctrip.com/schedule/csx.bjs.html?pageno=2',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}


# 异步请求函数
async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.text()


async def fetch_schedule(session, ks, js, header):
    curl = 'https://flights.ctrip.com/schedule/getScheduleByCityPair'
    data = {"departureCityCode": f'{str(ks).upper()}', "arriveCityCode": f'{str(js).upper()}', "pageNo": 1}
    async with session.post(url=curl, headers=header, json=data) as response:
        return await response.json()


# 主程序
async def main():
    url1 = 'https://flights.ctrip.com/schedule/'
    async with aiohttp.ClientSession() as session:
        req = await fetch(session, url1, header)
        soup = BeautifulSoup(req, 'html.parser')
        ac = []

        # 获取所有航班信息
        tasks = []
        for i in soup.select('ul[id="list"] li div a'):
            url2 = 'https://flights.ctrip.com' + i.get('href')
            tasks.append(fetch(session, url2, header))

        page_responses = await asyncio.gather(*tasks)

        # 使用进度条显示进度
        with tqdm(total=len(page_responses), desc="Processing Pages") as pbar:
            # 遍历页面并抓取数据
            for req2 in page_responses:
                soup = BeautifulSoup(req2, 'html.parser')
                for i in soup.select('ul[id="ulD_Domestic"] li div a'):
                    ks, js = i.get('href').replace('/schedule/', '').replace('.html', '').split('.')
                    # 异步获取排班数据
                    schedule_data = await fetch_schedule(session, ks, js, header)
                    max_page = schedule_data['totalPage']
                    ac.extend(schedule_data['scheduleVOList'])

                    # 获取更多页面数据
                    page_tasks = []
                    for i in range(2, max_page + 1):
                        page_tasks.append(fetch_schedule(session, ks, js, header))

                    page_responses = await asyncio.gather(*page_tasks)
                    for page_data in page_responses:
                        ac.extend(page_data['scheduleVOList'])
                pbar.update(1)

        # 保存数据
        df = pd.DataFrame(ac)
        acc = pd.DataFrame(df.pop('currentWeekSchedule').tolist())
        ps = pd.concat([df, acc], axis=1)

        # 继续更新进度条
        with tqdm(total=len(ac), desc="Saving data") as pbar:
            ps.to_csv('飞机票数据.csv', index=False)
            pbar.update(len(ac))


# 运行异步任务
if __name__ == '__main__':
    asyncio.run(main())
