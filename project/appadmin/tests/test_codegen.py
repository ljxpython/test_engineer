import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://playwright.dev/python/docs/codegen-intro")
    page.get_by_role("img", name="picking a locator").click()
    page.get_by_role("heading", name="EmulationDirect link to").click()
    page.get_by_role("link", name="Next Running and debugging").click()
