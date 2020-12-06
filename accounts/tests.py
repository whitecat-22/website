# from django.test import TestCase

# Create your tests here.
from django.test import LiveServerTestCase
from django.urls import reverse_lazy
from selenium.webdriver.chrome.webdriver import WebDriver


class TestLogin(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(executable_path='C:/Program Files/chromedriver_win32/chromedriver.exe')    # <Chromeドライバ配置場所>


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # ログインページを開く
        self.selenium.get('http://127.0.0.1:8000' + str(reverse_lazy('account_login')))    # '127.0.0.1' or 'localhost' を指定する

        # ログイン
        username_input = self.selenium.find_element_by_name("login")
        username_input.send_keys('mmmmmmmm@exam.com')    # <ユーザー登録済みのメールアドレス>
        password_input = self.selenium.find_element_by_name("password")    # <ログインパスワード>
        password_input.send_keys('xxxxxxxx')
        self.selenium.find_element_by_class_name('btn').click()

        # ページタイトルの検証
        self.assertEquals('ブログ一覧 | しろねこプロダクト', self.selenium.title)
