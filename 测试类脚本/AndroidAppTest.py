import os
import time
import unittest
# from selenium import webdriver
from appium import webdriver
from appium.webdriver.common.touch_action import *
from appium.webdriver.webdriver import WebDriver

from appium.webdriver.webdriver import WebDriver as learn
from appium import webdriver as learn1

from lib2to3.pgen2.driver import Driver
from lib2to3.tests.support import driver

PATH = lambda p: os.path.abspath(
	os.path.join(os.path.dirname(__file__), p)
)


class SmallloanAndroidTests(unittest.TestCase):

	def setUp(self):
		desired_caps = {}
		desired_caps['device'] = 'PBV7N16630002955'
		desired_caps['platformName'] = 'Android'
		desired_caps['browserName'] = ''
		desired_caps['version'] = '7.1.1'
		desired_caps['deviceName'] = 'PBV7N16630002955'  # 这是测试机的型号，可以查看手机的关于本机选项获得
		desired_caps['automationName']='uiautomator2'# desired_caps['app'] = PATH('D:\\Bo\\loan_android_1.0_0303_test.apk')#被测试的App在电脑上的位置
		# 如果知道被测试对象的apppage，appActivity可以加上下面这两个参数，如果不知道，可以注释掉，不影响用例执行
		desired_caps['appPackage']='com.sohu.newsclient'
		desired_caps['appActivity']=r'com.sohu.newsclient.boot.activity.SplashActivity'
		self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

	def tearDown(self):
		self.driver.quit()

	def check_1stElement(self,id):
		try:
			if self.driver.find_element_by_id(id).is_displayed()==True:
				return True
		except:
			return False
	def test_function(self):
		time.sleep(2)
		x=0
		while x<3 and self.check_1stElement('com.sohu.newsclient:id/news_more')==False:

			try:

				els = self.driver.find_elements_by_class_name('android.widget.Button')
				for el in els:
					if el.text == u'允许':
						self.driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
						x += 1
					elif el.text == u'始终允许':
						self.driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
						x += 1
					elif el.text == u'确定':
						self.driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
						x += 1
			except:
				pass
		# self.driver.switch_to.alert.accept()
		time.sleep(2)
		# temp=self.driver.find_element_by_id('com.sohu.newsclient:id/news_moree').is_displayed()
		# print(temp)
		self.driver.find_element_by_id('com.sohu.newsclient:id/news_more').click()
		time.sleep(5)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(SmallloanAndroidTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
	# print(dir(learn1))
