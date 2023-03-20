import asyncio
import random
from playwright.async_api import async_playwright,Browser

PAGE_COUNT = 10   #翻页数量
SEARCH_KEY = '单间'
GROUP_HOME = [
  "https://www.douban.com/group/nanshanzufang/discussion",# 南山租房
  "https://www.douban.com/group/637628/discussion",
  "https://www.douban.com/group/szsh/discussion"
]

async def douban_group(browser: Browser, url):
    group_key = url.split('/')[-2]
    result = {}

    async def deal_page(post_list):
        for post in post_list[1:]:
            link_element = await post.query_selector('a')
            time_element = await post.query_selector('.time')
            link =  await link_element.get_attribute('href')
            title = await link_element.get_attribute('title')
            time = await time_element.inner_text()

            res = '【{}】{}:{}'.format(time,title,link)
            print(res)
            if(title.find(SEARCH_KEY) > -1):
                result[title] = res


    page = await browser.new_page()

    await page.wait_for_timeout(random.randint(1,10) * 1000)
    # 访问豆瓣小组页面
    await page.goto(url)

    try:
        for i in range(0,PAGE_COUNT):

            await page.wait_for_selector('.olt')

            temp = await page.query_selector('.olt')
            post_list = await temp.query_selector_all('tr')
            await deal_page(post_list)

            await page.wait_for_timeout(random.randint(5,10) * 1000)
            await page.click('.next')
    except Exception as e:
        print("Error:",e)

    with open('douban-{}.json'.format(group_key),'w',encoding='utf-8') as f:
        for k in result:
          f.writelines([result[k],'\n'])


async def main():
    async with async_playwright() as p:
        # 启动浏览器并打开新页面
        chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        browser: Browser = await p.chromium.launch(executable_path=chrome_path,
                                          headless=False)

        task = [asyncio.create_task(douban_group(browser, url)) for url in GROUP_HOME]
        [await t for t in task]

        await browser.close()

if __name__ == '__main__':

    asyncio.run(main())
