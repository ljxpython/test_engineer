import pytest

from appadmin.pages.login_page import LoginPage


class TestLogin:
    @pytest.mark.nag
    def test_login_001(self, page):
        loginPage = LoginPage(page)
        loginPage.navigate()
        loginPage.login('huice666', '123456')
        assert '不存在' in loginPage.message_loc.text_content()

    # 抖音号 huice_perf

    @pytest.mark.smoke
    def test_login_002(self, page):
        loginPage = LoginPage(page)
        loginPage.navigate()
        loginPage.login('admin', '123456')
        # assert 'http://appadmin.huice.com/' == page.url
        # assert '不存在' in loginPage.message_loc.text_content()
