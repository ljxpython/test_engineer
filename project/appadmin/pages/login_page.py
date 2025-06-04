from playwright.sync_api import Page
from appadmin.repository import loginObject


class LoginPage:
    def __init__(self, page: Page):
        """
        定义封装页面对象
        :param page:
        """
        # self.username = 'input[placeholder="账号"]'  # 识别属性

        self.page = page
        # self.username_loc = page.locator(loginPageObject.username)
        self.username_loc = page.locator(loginObject.username)  # 页面对象
        self.password_loc = page.locator(loginObject.password)
        self.submit_loc = page.locator(loginObject.submit)
        self.message_loc = page.locator(loginObject.message)

    def navigate(self):
        self.page.goto('http://appadmin.huice.com/fecadmin/login/index')

    def login(self, username, password):
        self.username_loc.fill(username)
        self.password_loc.fill(password)
        self.submit_loc.click()


if __name__ == '__main__':
    page: Page
    loginPage = LoginPage(page)
    loginPage.navigate()
    loginPage.login('huice666', '123456')
