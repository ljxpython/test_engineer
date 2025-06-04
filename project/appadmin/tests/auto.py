import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.coder-ljx.cn:7524/user/login")
    page.get_by_role("textbox", name="用户名: admin or user").click()
    page.get_by_role("textbox", name="用户名: admin or user").fill("test")
    page.get_by_role("textbox", name="用户名: admin or user").press("Enter")
    page.get_by_role("textbox", name="密码: ant.design").click()
    page.get_by_role("textbox", name="密码: ant.design").fill("test")
    page.get_by_role("button", name="登 录").click()
    page.get_by_role("menuitem", name="partition 接口测试").locator("div").click()
    page.get_by_role("link", name="接口测试模块").click()
    expect(page.locator("thead")).to_contain_text("更新")
    page.get_by_role("cell", name="-10-31").first.click()
    page.get_by_role("cell", name="test_user").get_by_label("复制").click()
    page.get_by_text("条/页").click()
    page.get_by_role("main").click()
    expect(page.locator("tbody")).to_match_aria_snapshot("- text: 编辑 查看\n- img \"ellipsis\"")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
