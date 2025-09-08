# Android & iOS自动化测试专题

## 专题概述
本专题涵盖移动端自动化测试的核心技术和实践，包括原生应用、混合应用、跨平台应用的测试策略，是高级测试开发工程师移动端测试领域的核心技能。

**核心技能点**：
- Appium移动端自动化框架
- 原生Android/iOS测试工具
- 移动端特有测试场景
- 设备管理和云测试平台
- 移动端性能和兼容性测试
- App安全测试方法

---

## 题目列表

### ⭐⭐⭐ Appium自动化测试框架设计与实现
**难度**：⭐⭐⭐  
**频率**：🔥🔥🔥

**标准答案**：
**Appium架构和工作原理**：

```
客户端测试脚本 -> Appium Server -> Mobile Driver -> 移动设备/模拟器
                                   ↓
                              UIAutomator2/XCUITest
```

**Appium环境配置和工具类**：
```python
# appium_manager.py - Appium测试管理器
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import os
from typing import Dict, Any, Optional, List

class AppiumTestManager:
    def __init__(self, config_file: str = "mobile_config.json"):
        self.config = self.load_config(config_file)
        self.driver = None
        self.wait = None
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """加载移动端测试配置"""
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def setup_android_driver(self, device_name: str = None) -> webdriver.Remote:
        """配置Android驱动"""
        android_caps = {
            'platformName': 'Android',
            'platformVersion': self.config.get('android_version', '11'),
            'deviceName': device_name or self.config.get('android_device', 'Android Device'),
            'app': self.config.get('android_app_path'),
            'appPackage': self.config.get('android_package'),
            'appActivity': self.config.get('android_activity'),
            'automationName': 'UiAutomator2',
            'newCommandTimeout': 300,
            'noReset': False,
            'fullReset': False,
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'systemPort': self.get_available_port(8200),
            'chromeDriverPort': self.get_available_port(9515),
            # 性能优化配置
            'skipDeviceInitialization': True,
            'skipServerInstallation': True,
            'skipUnlock': True,
            'autoGrantPermissions': True,
            # 等待策略配置
            'waitForIdleTimeout': 100,
            'waitForSelectorTimeout': 1000,
            # 截图配置
            'screenshotWaitTimeout': 5,
            'skipLogcatCapture': False
        }
        
        # 云测试平台配置
        if self.config.get('use_cloud_testing'):
            android_caps.update({
                'browserstack.user': os.getenv('BROWSERSTACK_USERNAME'),
                'browserstack.key': os.getenv('BROWSERSTACK_ACCESS_KEY'),
                'project': self.config.get('project_name'),
                'build': self.config.get('build_name'),
                'name': 'Android Automation Test'
            })
        
        self.driver = webdriver.Remote(
            command_executor=self.config.get('appium_server_url', 'http://localhost:4723/wd/hub'),
            desired_capabilities=android_caps
        )
        
        self.wait = WebDriverWait(self.driver, 30)
        return self.driver
    
    def setup_ios_driver(self, device_name: str = None) -> webdriver.Remote:
        """配置iOS驱动"""
        ios_caps = {
            'platformName': 'iOS',
            'platformVersion': self.config.get('ios_version', '15.0'),
            'deviceName': device_name or self.config.get('ios_device', 'iPhone 13'),
            'app': self.config.get('ios_app_path'),
            'bundleId': self.config.get('ios_bundle_id'),
            'automationName': 'XCUITest',
            'newCommandTimeout': 300,
            'noReset': False,
            'fullReset': False,
            'wdaStartupRetries': 2,
            'wdaStartupRetryInterval': 20000,
            'iosInstallPause': 8000,
            'wdaConnectionTimeout': 60000,
            # WebDriverAgent配置
            'useNewWDA': False,
            'wdaLocalPort': self.get_available_port(8100),
            'mjpegServerPort': self.get_available_port(9100),
            # 权限配置
            'autoAcceptAlerts': True,
            'autoDismissAlerts': False,
            # 性能配置
            'shouldUseSingletonTestManager': False,
            'shouldUseTestManagerForVisibilityDetection': False
        }
        
        # 真机测试配置
        if self.config.get('ios_real_device'):
            ios_caps.update({
                'udid': self.config.get('ios_udid'),
                'xcodeOrgId': self.config.get('xcode_org_id'),
                'xcodeSigningId': self.config.get('xcode_signing_id'),
                'realDeviceLogger': '/usr/local/lib/node_modules/deviceconsole/deviceconsole',
                'showIOSLog': True
            })
        
        self.driver = webdriver.Remote(
            command_executor=self.config.get('appium_server_url', 'http://localhost:4723/wd/hub'),
            desired_capabilities=ios_caps
        )
        
        self.wait = WebDriverWait(self.driver, 30)
        return self.driver
    
    def get_available_port(self, start_port: int) -> int:
        """获取可用端口"""
        import socket
        
        port = start_port
        while port < start_port + 100:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(('localhost', port))
                sock.close()
                return port
            except OSError:
                port += 1
        
        raise RuntimeError(f"No available port found starting from {start_port}")

class MobilePageObject:
    """移动端页面对象基类"""
    
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.touch_action = TouchAction(driver)
    
    def find_element_by_id(self, element_id: str, timeout: int = 30):
        """通过ID查找元素"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    def find_element_by_xpath(self, xpath: str, timeout: int = 30):
        """通过XPath查找元素"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def find_element_by_accessibility_id(self, accessibility_id: str, timeout: int = 30):
        """通过Accessibility ID查找元素（推荐）"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(
            (By.ACCESSIBILITY_ID, accessibility_id)
        ))
    
    def tap_element(self, element, duration: int = 100):
        """点击元素"""
        self.touch_action.tap(element, duration=duration).perform()
    
    def tap_coordinates(self, x: int, y: int, duration: int = 100):
        """点击坐标"""
        self.touch_action.tap(x=x, y=y, duration=duration).perform()
    
    def swipe_element(self, element, direction: str, duration: int = 1000):
        """滑动元素"""
        size = element.size
        location = element.location
        
        start_x = location['x'] + size['width'] // 2
        start_y = location['y'] + size['height'] // 2
        
        if direction.lower() == 'up':
            end_x, end_y = start_x, start_y - size['height'] // 2
        elif direction.lower() == 'down':
            end_x, end_y = start_x, start_y + size['height'] // 2
        elif direction.lower() == 'left':
            end_x, end_y = start_x - size['width'] // 2, start_y
        elif direction.lower() == 'right':
            end_x, end_y = start_x + size['width'] // 2, start_y
        else:
            raise ValueError("Direction must be 'up', 'down', 'left', or 'right'")
        
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    
    def scroll_to_element(self, element_locator: tuple, max_scrolls: int = 10):
        """滚动到元素"""
        for _ in range(max_scrolls):
            try:
                element = self.driver.find_element(*element_locator)
                return element
            except:
                # 向下滚动
                screen_size = self.driver.get_window_size()
                start_x = screen_size['width'] // 2
                start_y = screen_size['height'] * 3 // 4
                end_y = screen_size['height'] // 4
                
                self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
                time.sleep(1)
        
        raise Exception(f"Element {element_locator} not found after {max_scrolls} scrolls")
    
    def long_press(self, element, duration: int = 2000):
        """长按元素"""
        self.touch_action.long_press(element, duration=duration).perform()
    
    def pinch_zoom(self, element, scale: float = 2.0):
        """缩放手势"""
        action1 = TouchAction(self.driver)
        action2 = TouchAction(self.driver)
        
        size = element.size
        location = element.location
        
        center_x = location['x'] + size['width'] // 2
        center_y = location['y'] + size['height'] // 2
        
        # 起始点
        start_x1 = center_x - 50
        start_y1 = center_y - 50
        start_x2 = center_x + 50
        start_y2 = center_y + 50
        
        # 结束点（根据缩放比例计算）
        end_x1 = center_x - int(50 * scale)
        end_y1 = center_y - int(50 * scale)
        end_x2 = center_x + int(50 * scale)
        end_y2 = center_y + int(50 * scale)
        
        action1.press(x=start_x1, y=start_y1).move_to(x=end_x1, y=end_y1).release()
        action2.press(x=start_x2, y=start_y2).move_to(x=end_x2, y=end_y2).release()
        
        multi_action = MultiAction(self.driver)
        multi_action.add(action1, action2)
        multi_action.perform()
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = 30):
        """等待元素可见"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = 30):
        """等待元素可点击"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def hide_keyboard(self):
        """隐藏键盘"""
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except:
            # 如果hide_keyboard不可用，尝试点击其他区域
            screen_size = self.driver.get_window_size()
            self.tap_coordinates(screen_size['width'] // 2, 100)
    
    def take_screenshot(self, filename: str = None) -> str:
        """截图"""
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filepath = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath

# 具体页面实现示例
class LoginPage(MobilePageObject):
    """登录页面"""
    
    # 元素定位器
    USERNAME_FIELD = (By.ID, "username_input")
    PASSWORD_FIELD = (By.ID, "password_input")
    LOGIN_BUTTON = (By.ACCESSIBILITY_ID, "login_button")
    ERROR_MESSAGE = (By.XPATH, "//android.widget.TextView[@content-desc='error_message']")
    FORGOT_PASSWORD_LINK = (By.ID, "forgot_password")
    
    def __init__(self, driver: webdriver.Remote):
        super().__init__(driver)
    
    def enter_username(self, username: str):
        """输入用户名"""
        username_field = self.wait_for_element_visible(self.USERNAME_FIELD)
        username_field.clear()
        username_field.send_keys(username)
        self.hide_keyboard()
        return self
    
    def enter_password(self, password: str):
        """输入密码"""
        password_field = self.wait_for_element_visible(self.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        self.hide_keyboard()
        return self
    
    def tap_login_button(self):
        """点击登录按钮"""
        login_button = self.wait_for_element_clickable(self.LOGIN_BUTTON)
        self.tap_element(login_button)
        return self
    
    def login(self, username: str, password: str):
        """执行登录操作"""
        return (self.enter_username(username)
                   .enter_password(password)
                   .tap_login_button())
    
    def get_error_message(self) -> str:
        """获取错误信息"""
        try:
            error_element = self.wait_for_element_visible(self.ERROR_MESSAGE, timeout=10)
            return error_element.text
        except:
            return ""
    
    def is_login_successful(self) -> bool:
        """检查登录是否成功"""
        try:
            # 检查是否跳转到主页（假设主页有特定元素）
            from .home_page import HomePage
            home_page = HomePage(self.driver)
            return home_page.is_displayed()
        except:
            return False

class HomePage(MobilePageObject):
    """主页"""
    
    WELCOME_MESSAGE = (By.ID, "welcome_message")
    PROFILE_BUTTON = (By.ACCESSIBILITY_ID, "profile_button")
    MENU_BUTTON = (By.ID, "menu_button")
    SEARCH_BAR = (By.ID, "search_bar")
    
    def is_displayed(self) -> bool:
        """检查主页是否显示"""
        try:
            self.wait_for_element_visible(self.WELCOME_MESSAGE, timeout=10)
            return True
        except:
            return False
    
    def open_profile(self):
        """打开个人资料"""
        profile_button = self.wait_for_element_clickable(self.PROFILE_BUTTON)
        self.tap_element(profile_button)
        
        from .profile_page import ProfilePage
        return ProfilePage(self.driver)
    
    def search(self, query: str):
        """执行搜索"""
        search_bar = self.wait_for_element_visible(self.SEARCH_BAR)
        self.tap_element(search_bar)
        search_bar.send_keys(query)
        self.hide_keyboard()
        
        # 点击搜索按钮或回车
        self.driver.press_keycode(66)  # Android回车键

# 测试用例示例
class TestMobileApp:
    def setup_method(self):
        """测试前置设置"""
        self.test_manager = AppiumTestManager()
        
        # 根据测试需要选择平台
        platform = os.getenv('TEST_PLATFORM', 'android').lower()
        if platform == 'android':
            self.driver = self.test_manager.setup_android_driver()
        else:
            self.driver = self.test_manager.setup_ios_driver()
        
        self.login_page = LoginPage(self.driver)
    
    def teardown_method(self):
        """测试后置清理"""
        if self.driver:
            self.driver.quit()
    
    def test_successful_login(self):
        """测试成功登录"""
        # 执行登录
        self.login_page.login("valid_user", "valid_password")
        
        # 验证登录成功
        assert self.login_page.is_login_successful(), "登录失败"
    
    def test_invalid_login(self):
        """测试无效登录"""
        # 执行无效登录
        self.login_page.login("invalid_user", "invalid_password")
        
        # 验证错误信息
        error_message = self.login_page.get_error_message()
        assert "用户名或密码错误" in error_message, f"期望的错误信息未显示：{error_message}"
    
    def test_empty_credentials(self):
        """测试空凭据"""
        self.login_page.tap_login_button()
        
        error_message = self.login_page.get_error_message()
        assert "请输入用户名和密码" in error_message
    
    def test_gesture_operations(self):
        """测试手势操作"""
        # 登录成功后测试手势
        self.login_page.login("valid_user", "valid_password")
        home_page = HomePage(self.driver)
        
        # 测试滑动
        screen_size = self.driver.get_window_size()
        self.driver.swipe(
            screen_size['width'] // 2, screen_size['height'] * 3 // 4,
            screen_size['width'] // 2, screen_size['height'] // 4,
            1000
        )
        
        # 测试搜索功能
        home_page.search("测试搜索")

# 移动端测试配置文件示例
"""
mobile_config.json:
{
    "appium_server_url": "http://localhost:4723/wd/hub",
    "android_app_path": "/path/to/app.apk",
    "android_package": "com.example.app",
    "android_activity": "com.example.app.MainActivity",
    "android_version": "11",
    "android_device": "Android Device",
    "ios_app_path": "/path/to/app.ipa",
    "ios_bundle_id": "com.example.app",
    "ios_version": "15.0",
    "ios_device": "iPhone 13",
    "ios_real_device": false,
    "ios_udid": "device_udid",
    "xcode_org_id": "your_org_id",
    "xcode_signing_id": "iPhone Developer",
    "use_cloud_testing": false,
    "project_name": "Mobile App Test",
    "build_name": "Build 1.0"
}
"""
```

**移动端特有测试场景处理**：
```python
# mobile_scenarios.py - 移动端特有场景测试
class MobileScenarioTests:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.touch_action = TouchAction(driver)
    
    def test_app_lifecycle(self):
        """测试应用生命周期"""
        # 应用切换到后台
        self.driver.background_app(5)  # 后台5秒
        
        # 验证应用恢复状态
        current_activity = self.driver.current_activity
        assert current_activity is not None
        
        # 测试应用终止和重启
        self.driver.terminate_app("com.example.app")
        time.sleep(2)
        self.driver.activate_app("com.example.app")
    
    def test_network_conditions(self):
        """测试网络条件变化"""
        # 设置网络条件（需要模拟器支持）
        try:
            self.driver.set_network_connection(0)  # 关闭网络
            time.sleep(2)
            
            # 测试离线功能
            self.verify_offline_functionality()
            
            # 恢复网络
            self.driver.set_network_connection(6)  # WiFi + 数据
            
            # 测试网络恢复后的同步
            self.verify_online_sync()
            
        except Exception as e:
            print(f"Network testing not supported: {e}")
    
    def test_device_rotation(self):
        """测试设备旋转"""
        # 获取当前方向
        current_orientation = self.driver.orientation
        
        # 旋转到横屏
        self.driver.orientation = "LANDSCAPE"
        time.sleep(2)
        
        # 验证布局适应
        self.verify_landscape_layout()
        
        # 旋转回竖屏
        self.driver.orientation = "PORTRAIT"
        time.sleep(2)
        
        # 验证布局恢复
        self.verify_portrait_layout()
    
    def test_push_notifications(self):
        """测试推送通知"""
        # 发送推送通知（需要外部工具配合）
        self.send_push_notification({
            "title": "测试通知",
            "body": "这是一条测试推送消息",
            "data": {"action": "open_page", "page": "home"}
        })
        
        # 验证通知显示
        time.sleep(5)
        
        # 点击通知（Android）
        if self.is_android():
            self.driver.open_notifications()
            notification = self.driver.find_element(By.XPATH, 
                "//android.widget.TextView[contains(@text, '测试通知')]")
            notification.click()
            
            # 验证应用响应
            self.verify_notification_response()
    
    def test_permissions(self):
        """测试权限请求"""
        # 触发权限请求的功能
        self.trigger_camera_permission()
        
        # 处理权限对话框
        if self.is_android():
            try:
                allow_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "com.android.packageinstaller:id/permission_allow_button"))
                )
                allow_button.click()
            except:
                # 尝试其他可能的权限按钮ID
                try:
                    allow_button = self.driver.find_element(By.XPATH, 
                        "//android.widget.Button[contains(@text, 'Allow') or contains(@text, '允许')]")
                    allow_button.click()
                except:
                    print("无法找到权限允许按钮")
        else:  # iOS
            try:
                allow_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ACCESSIBILITY_ID, "Allow"))
                )
                allow_button.click()
            except:
                print("无法找到iOS权限允许按钮")
    
    def test_deep_links(self):
        """测试深度链接"""
        deep_link = "myapp://open/product/123"
        
        # 打开深度链接
        if self.is_android():
            self.driver.execute_script("mobile: deepLink", {
                "url": deep_link,
                "package": "com.example.app"
            })
        else:  # iOS
            self.driver.execute_script("mobile: launchApp", {
                "bundleId": "com.example.app",
                "arguments": [deep_link]
            })
        
        time.sleep(3)
        
        # 验证应用正确处理深度链接
        current_screen = self.get_current_screen_identifier()
        assert "product" in current_screen.lower()
    
    def test_biometric_authentication(self):
        """测试生物识别认证"""
        # 导航到生物识别登录
        self.navigate_to_biometric_login()
        
        # 触发生物识别
        biometric_button = self.driver.find_element(By.ACCESSIBILITY_ID, "biometric_login")
        biometric_button.click()
        
        # 模拟生物识别成功
        if self.is_android():
            self.driver.execute_script("mobile: fingerprint", {
                "match": True
            })
        else:  # iOS
            self.driver.execute_script("mobile: touchId", {
                "match": True
            })
        
        # 验证登录成功
        self.verify_login_success()
    
    def test_app_updates(self):
        """测试应用更新流程"""
        # 模拟有新版本可用
        self.simulate_app_update_available()
        
        # 检查更新提示
        try:
            update_dialog = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "update_dialog"))
            )
            
            # 点击更新按钮
            update_button = self.driver.find_element(By.ID, "update_button")
            update_button.click()
            
            # 验证跳转到应用商店
            time.sleep(5)
            current_package = self.driver.current_package
            assert "play.google.com" in current_package or "app-store" in current_package
            
        except:
            print("未检测到更新对话框")
    
    def is_android(self) -> bool:
        """判断是否为Android平台"""
        return self.driver.desired_capabilities.get('platformName', '').lower() == 'android'
    
    def verify_offline_functionality(self):
        """验证离线功能"""
        # 实现离线功能验证逻辑
        pass
    
    def verify_online_sync(self):
        """验证在线同步"""
        # 实现在线同步验证逻辑
        pass
    
    def verify_landscape_layout(self):
        """验证横屏布局"""
        # 实现横屏布局验证逻辑
        pass
    
    def verify_portrait_layout(self):
        """验证竖屏布局"""
        # 实现竖屏布局验证逻辑
        pass
    
    def send_push_notification(self, payload: dict):
        """发送推送通知（需要外部服务）"""
        # 实现推送通知发送逻辑
        pass
    
    def verify_notification_response(self):
        """验证通知响应"""
        # 实现通知响应验证逻辑
        pass
    
    def trigger_camera_permission(self):
        """触发相机权限请求"""
        camera_button = self.driver.find_element(By.ACCESSIBILITY_ID, "camera_button")
        camera_button.click()
    
    def get_current_screen_identifier(self) -> str:
        """获取当前屏幕标识"""
        # 实现屏幕识别逻辑
        return "unknown_screen"
    
    def navigate_to_biometric_login(self):
        """导航到生物识别登录"""
        # 实现导航逻辑
        pass
    
    def verify_login_success(self):
        """验证登录成功"""
        # 实现登录成功验证逻辑
        pass
    
    def simulate_app_update_available(self):
        """模拟应用更新可用"""
        # 实现更新模拟逻辑
        pass
```

---

### ⭐⭐⭐ 移动端性能测试方法和工具
**难度**：⭐⭐⭐  
**频率**：🔥🔥

**标准答案**：
**移动端性能测试关键指标**：

1. **启动性能**：冷启动、热启动、温启动时间
2. **CPU使用率**：应用运行时的CPU占用情况
3. **内存使用**：内存占用、内存泄漏检测
4. **电池消耗**：功耗分析和优化
5. **网络性能**：请求响应时间、流量消耗
6. **UI响应性**：界面流畅度、卡顿分析

**移动端性能测试实现**：
```python
# mobile_performance.py - 移动端性能测试
import time
import json
import subprocess
import threading
from typing import Dict, List, Any
import psutil
import matplotlib.pyplot as plt
import pandas as pd

class MobilePerformanceMonitor:
    def __init__(self, package_name: str, platform: str = "android"):
        self.package_name = package_name
        self.platform = platform.lower()
        self.monitoring = False
        self.performance_data = []
        self.monitor_thread = None
    
    def start_monitoring(self, interval: float = 1.0):
        """开始性能监控"""
        self.monitoring = True
        self.performance_data = []
        
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,)
        )
        self.monitor_thread.start()
        print(f"开始监控应用 {self.package_name} 的性能...")
    
    def stop_monitoring(self):
        """停止性能监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("性能监控已停止")
    
    def _monitor_loop(self, interval: float):
        """监控循环"""
        while self.monitoring:
            try:
                performance_snapshot = self.collect_performance_metrics()
                if performance_snapshot:
                    self.performance_data.append(performance_snapshot)
                time.sleep(interval)
            except Exception as e:
                print(f"监控过程中发生错误: {e}")
                time.sleep(interval)
    
    def collect_performance_metrics(self) -> Dict[str, Any]:
        """收集性能指标"""
        metrics = {
            'timestamp': time.time(),
            'cpu_usage': self.get_cpu_usage(),
            'memory_usage': self.get_memory_usage(),
            'network_stats': self.get_network_stats(),
            'battery_level': self.get_battery_level(),
            'temperature': self.get_device_temperature()
        }
        
        if self.platform == "android":
            metrics.update(self.get_android_specific_metrics())
        else:
            metrics.update(self.get_ios_specific_metrics())
        
        return metrics
    
    def get_cpu_usage(self) -> float:
        """获取CPU使用率"""
        if self.platform == "android":
            try:
                # 使用adb获取应用CPU使用率
                result = subprocess.run([
                    'adb', 'shell', 'top', '-n', '1', '|', 'grep', self.package_name
                ], capture_output=True, text=True, shell=True)
                
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if self.package_name in line:
                            parts = line.split()
                            if len(parts) >= 9:
                                return float(parts[8].replace('%', ''))
                return 0.0
            except:
                return 0.0
        else:
            # iOS CPU监控需要使用Instruments或者私有API
            return self._get_ios_cpu_usage()
    
    def get_memory_usage(self) -> Dict[str, float]:
        """获取内存使用情况"""
        if self.platform == "android":
            try:
                # 获取应用内存使用
                result = subprocess.run([
                    'adb', 'shell', 'dumpsys', 'meminfo', self.package_name
                ], capture_output=True, text=True)
                
                memory_info = self.parse_android_memory_info(result.stdout)
                return memory_info
            except:
                return {'total': 0, 'pss': 0, 'private': 0}
        else:
            return self._get_ios_memory_usage()
    
    def parse_android_memory_info(self, meminfo_output: str) -> Dict[str, float]:
        """解析Android内存信息"""
        memory_data = {'total': 0, 'pss': 0, 'private': 0}
        
        lines = meminfo_output.split('\n')
        for line in lines:
            if 'TOTAL' in line and 'PSS' in line:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        memory_data['pss'] = float(parts[1]) / 1024  # 转换为MB
                    except:
                        pass
            elif 'Private Dirty:' in line:
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        memory_data['private'] = float(parts[2]) / 1024
                    except:
                        pass
        
        return memory_data
    
    def get_network_stats(self) -> Dict[str, float]:
        """获取网络使用统计"""
        if self.platform == "android":
            try:
                # 获取应用网络使用统计
                result = subprocess.run([
                    'adb', 'shell', 'cat', '/proc/net/xt_qtaguid/stats'
                ], capture_output=True, text=True)
                
                return self.parse_android_network_stats(result.stdout)
            except:
                return {'rx_bytes': 0, 'tx_bytes': 0}
        else:
            return self._get_ios_network_stats()
    
    def parse_android_network_stats(self, stats_output: str) -> Dict[str, float]:
        """解析Android网络统计"""
        network_data = {'rx_bytes': 0, 'tx_bytes': 0}
        
        # 实现网络统计解析逻辑
        lines = stats_output.split('\n')
        for line in lines:
            if self.package_name in line:
                parts = line.split()
                if len(parts) >= 8:
                    try:
                        network_data['rx_bytes'] += float(parts[5])
                        network_data['tx_bytes'] += float(parts[7])
                    except:
                        pass
        
        return network_data
    
    def get_battery_level(self) -> float:
        """获取电池电量"""
        if self.platform == "android":
            try:
                result = subprocess.run([
                    'adb', 'shell', 'dumpsys', 'battery'
                ], capture_output=True, text=True)
                
                for line in result.stdout.split('\n'):
                    if 'level:' in line:
                        return float(line.split(':')[1].strip())
                return 0.0
            except:
                return 0.0
        else:
            return self._get_ios_battery_level()
    
    def get_device_temperature(self) -> float:
        """获取设备温度"""
        if self.platform == "android":
            try:
                result = subprocess.run([
                    'adb', 'shell', 'cat', '/sys/class/thermal/thermal_zone0/temp'
                ], capture_output=True, text=True)
                
                if result.stdout.strip():
                    # 温度通常以毫度为单位
                    temp_millidegrees = float(result.stdout.strip())
                    return temp_millidegrees / 1000.0
                return 0.0
            except:
                return 0.0
        else:
            return self._get_ios_temperature()
    
    def get_android_specific_metrics(self) -> Dict[str, Any]:
        """获取Android特有指标"""
        metrics = {}
        
        # GPU使用率
        metrics['gpu_usage'] = self.get_gpu_usage()
        
        # 应用启动时间
        metrics['app_startup_time'] = self.measure_app_startup_time()
        
        # 帧率
        metrics['fps'] = self.get_frame_rate()
        
        return metrics
    
    def get_gpu_usage(self) -> float:
        """获取GPU使用率"""
        try:
            result = subprocess.run([
                'adb', 'shell', 'cat', '/sys/class/kgsl/kgsl-3d0/gpubusy'
            ], capture_output=True, text=True)
            
            if result.stdout.strip():
                return float(result.stdout.strip())
            return 0.0
        except:
            return 0.0
    
    def measure_app_startup_time(self) -> float:
        """测量应用启动时间"""
        try:
            # 先杀死应用
            subprocess.run(['adb', 'shell', 'am', 'force-stop', self.package_name])
            time.sleep(1)
            
            # 记录启动时间
            start_time = time.time()
            
            # 启动应用
            result = subprocess.run([
                'adb', 'shell', 'am', 'start-activity', '-W',
                f'{self.package_name}/.MainActivity'
            ], capture_output=True, text=True)
            
            # 解析启动时间
            for line in result.stdout.split('\n'):
                if 'TotalTime:' in line:
                    return float(line.split(':')[1].strip())
            
            return 0.0
        except:
            return 0.0
    
    def get_frame_rate(self) -> float:
        """获取帧率"""
        try:
            # 使用dumpsys gfxinfo获取帧率信息
            result = subprocess.run([
                'adb', 'shell', 'dumpsys', 'gfxinfo', self.package_name, 'framestats'
            ], capture_output=True, text=True)
            
            return self.parse_frame_stats(result.stdout)
        except:
            return 0.0
    
    def parse_frame_stats(self, framestats_output: str) -> float:
        """解析帧统计信息"""
        lines = framestats_output.split('\n')
        frame_times = []
        
        for line in lines:
            if line.startswith('0,'):  # 帧数据行
                parts = line.split(',')
                if len(parts) >= 3:
                    try:
                        # 计算帧时间（纳秒转换为毫秒）
                        frame_time = (float(parts[1]) - float(parts[0])) / 1000000
                        frame_times.append(frame_time)
                    except:
                        continue
        
        if frame_times:
            avg_frame_time = sum(frame_times) / len(frame_times)
            # 计算FPS
            return 1000.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
        return 0.0
    
    def get_ios_specific_metrics(self) -> Dict[str, Any]:
        """获取iOS特有指标"""
        # iOS性能监控需要使用Instruments或其他工具
        return {
            'memory_warnings': 0,
            'thermal_state': 'nominal',
            'app_launch_time': 0.0
        }
    
    def _get_ios_cpu_usage(self) -> float:
        """获取iOS CPU使用率"""
        # iOS CPU监控实现
        return 0.0
    
    def _get_ios_memory_usage(self) -> Dict[str, float]:
        """获取iOS内存使用情况"""
        return {'total': 0, 'used': 0}
    
    def _get_ios_network_stats(self) -> Dict[str, float]:
        """获取iOS网络统计"""
        return {'rx_bytes': 0, 'tx_bytes': 0}
    
    def _get_ios_battery_level(self) -> float:
        """获取iOS电池电量"""
        return 0.0
    
    def _get_ios_temperature(self) -> float:
        """获取iOS设备温度"""
        return 0.0
    
    def generate_performance_report(self) -> str:
        """生成性能报告"""
        if not self.performance_data:
            return "没有性能数据"
        
        df = pd.DataFrame(self.performance_data)
        
        # 计算统计信息
        cpu_avg = df['cpu_usage'].mean()
        cpu_max = df['cpu_usage'].max()
        
        memory_avg = df['memory_usage'].apply(lambda x: x.get('pss', 0)).mean()
        memory_max = df['memory_usage'].apply(lambda x: x.get('pss', 0)).max()
        
        report = f"""
# 移动端性能测试报告

## 应用信息
- 应用包名: {self.package_name}
- 测试平台: {self.platform}
- 监控时长: {len(self.performance_data)} 秒
- 数据点数: {len(df)}

## CPU性能
- 平均CPU使用率: {cpu_avg:.2f}%
- 最大CPU使用率: {cpu_max:.2f}%

## 内存性能
- 平均内存使用: {memory_avg:.2f} MB
- 最大内存使用: {memory_max:.2f} MB

## 网络性能
- 总接收字节: {df['network_stats'].apply(lambda x: x.get('rx_bytes', 0)).sum():.0f}
- 总发送字节: {df['network_stats'].apply(lambda x: x.get('tx_bytes', 0)).sum():.0f}

## 电池和温度
- 平均电池电量: {df['battery_level'].mean():.1f}%
- 平均设备温度: {df['temperature'].mean():.1f}°C
"""
        
        if self.platform == "android":
            fps_avg = df['fps'].mean()
            report += f"""
## Android特有指标
- 平均FPS: {fps_avg:.1f}
- 应用启动时间: {df['app_startup_time'].iloc[0]:.0f} ms
"""
        
        return report
    
    def create_performance_charts(self, output_dir: str = "performance_charts"):
        """创建性能图表"""
        if not self.performance_data:
            print("没有性能数据用于生成图表")
            return
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        df = pd.DataFrame(self.performance_data)
        df['time'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # CPU使用率图表
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.plot(df['time'], df['cpu_usage'])
        plt.title('CPU使用率')
        plt.ylabel('CPU %')
        plt.xticks(rotation=45)
        
        # 内存使用图表
        plt.subplot(2, 2, 2)
        memory_usage = df['memory_usage'].apply(lambda x: x.get('pss', 0))
        plt.plot(df['time'], memory_usage)
        plt.title('内存使用')
        plt.ylabel('内存 (MB)')
        plt.xticks(rotation=45)
        
        # 电池电量图表
        plt.subplot(2, 2, 3)
        plt.plot(df['time'], df['battery_level'])
        plt.title('电池电量')
        plt.ylabel('电量 %')
        plt.xticks(rotation=45)
        
        # 设备温度图表
        plt.subplot(2, 2, 4)
        plt.plot(df['time'], df['temperature'])
        plt.title('设备温度')
        plt.ylabel('温度 °C')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/performance_overview.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 如果是Android，生成FPS图表
        if self.platform == "android" and 'fps' in df.columns:
            plt.figure(figsize=(10, 6))
            plt.plot(df['time'], df['fps'])
            plt.title('帧率 (FPS)')
            plt.ylabel('FPS')
            plt.xlabel('时间')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.savefig(f"{output_dir}/fps_chart.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"性能图表已保存到 {output_dir} 目录")

# 使用示例
class TestMobilePerformance:
    def setup_method(self):
        self.performance_monitor = MobilePerformanceMonitor(
            package_name="com.example.myapp",
            platform="android"
        )
    
    def test_app_performance_during_usage(self):
        """测试应用使用过程中的性能"""
        # 开始性能监控
        self.performance_monitor.start_monitoring(interval=1.0)
        
        try:
            # 执行各种应用操作
            self.perform_app_operations()
            
            # 监控30秒
            time.sleep(30)
            
        finally:
            # 停止监控
            self.performance_monitor.stop_monitoring()
            
            # 生成报告和图表
            report = self.performance_monitor.generate_performance_report()
            print(report)
            
            self.performance_monitor.create_performance_charts()
    
    def perform_app_operations(self):
        """执行应用操作"""
        # 实现具体的应用操作逻辑
        pass
    
    def test_memory_leak_detection(self):
        """内存泄漏检测测试"""
        monitor = MobilePerformanceMonitor("com.example.myapp")
        
        # 记录初始内存
        initial_memory = monitor.get_memory_usage()
        print(f"初始内存使用: {initial_memory}")
        
        # 执行重复操作
        for i in range(100):
            self.perform_memory_intensive_operation()
            
            if i % 10 == 0:
                current_memory = monitor.get_memory_usage()
                memory_increase = current_memory['pss'] - initial_memory['pss']
                print(f"第{i}次操作后内存增长: {memory_increase:.2f} MB")
                
                # 检查内存泄漏
                if memory_increase > 50:  # 50MB阈值
                    print("⚠️ 检测到可能的内存泄漏")
                    break
    
    def perform_memory_intensive_operation(self):
        """执行内存密集型操作"""
        # 实现内存密集型操作逻辑
        pass
```

---

## 专题总结

移动端自动化测试是现代应用开发的重要组成部分，需要掌握：

1. **框架技术**：熟练掌握Appium等移动端自动化测试框架
2. **平台特性**：深入理解Android和iOS平台的测试特点和差异
3. **特殊场景**：能够处理移动端特有的测试场景和挑战
4. **性能测试**：掌握移动端性能测试方法和工具
5. **设备管理**：了解真机测试和云测试平台的使用

**面试回答要点**：
- 展示对移动端测试技术栈的全面掌握
- 结合实际项目说明移动端测试实施经验
- 强调跨平台兼容性和设备覆盖策略
- 体现对移动端用户体验和性能的关注