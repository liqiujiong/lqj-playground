import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # 启动浏览器并打开新页面
        chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        browser = await p.chromium.launch(executable_path=chrome_path,
                                          headless=False)
        # browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 访问谷歌搜索页面
        await page.goto('https://www.google.com/')

        # 在搜索框中输入查询词
        await page.fill('input[name="q"]', '北京欢迎你')

        # 点击搜索按钮
        await page.click('input[type="submit"]')

        # 等待搜索结果加载完成
        await page.wait_for_selector('#search')
        # 获取搜索结果列表
        search_results = await page.query_selector_all('.yuRUbf')

        # 打印搜索结果标题和链接
        for result in search_results:
            title = await result.query_selector('h3')
            link = await result.query_selector('a')
            if title and link:

                print(await title.inner_text(), '->', await
                      link.get_attribute('href'))

        # 关闭浏览器
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
