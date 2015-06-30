#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium import webdriver
from settings import *
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.service as service
import os, time, unicodedata


class RobotStop(Exception):
    pass

class RobotStopAll(Exception):
    pass


class BaseSelenium(object):
    """
    Base Selenium class to start WebDriver and make try_again actions on Web Browser.
    """

    def __init__(self,
                donwload_dir=r'/Users/user/Documents/robo_screenshot/',
                screenshot_dir=r'/Users/user/Documents/robo_screenshot/',
                never_ask_savetodisk= 'application/pdf,text/plain,application/octet-stream,text/csv,application/csv,application/vnd.ms-excel,application/ms-excel,application/xml,application/vnd.csv,application/excel,text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml',
                screenshot_mask='{0}/screenshot_{1}.png',
                screenshot_date_mask='%Y-%m-%d__%H:%M:%S'):
        """
        Selenium (urllib2) doesn't work without no_proxy setted
        os.environ['no_proxy'] = '10.137.5.62:4444,127.0.0.1:4444' # vm ip and localhost
        """
        self.donwload_dir = donwload_dir
        self.screenshot_dir = screenshot_dir
        self.never_ask_savetodisk = never_ask_savetodisk
        self.screenshot_mask = screenshot_mask
        self.screenshot_date_mask = screenshot_date_mask

        os.environ['LANG'] = 'en_US.UTF-8'
        os.environ['no_proxy'] = '*'

        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")
        self.profile.set_preference("browser.download.dir", self.donwload_dir)
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.helperApps.neverAsk.openFile", self.never_ask_savetodisk)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", self.never_ask_savetodisk)
        # self.profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
        # self.profile.set_preference("browser.download.manager.focusWhenStarting", False)
        self.profile.set_preference("browser.download.manager.useWindow", False)
        self.profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        self.profile.set_preference("browser.download.manager.closeWhenDone", False)
        self.profile.set_preference("plugin.default.state", 2)
        self.profile.set_preference("plugin.state.java", 2)
        self.profile.set_preference("security.enable_java", True)
        # You can enable Navigation toolbar by adding the following to user.js:
        self.profile.set_preference("extensions.rkiosk.navbar", True)
        # You might want to remove the print dialog by adding following lines to your user.js:
        self.profile.set_preference("print.always_print_silent", True)
        self.profile.set_preference("print.show_print_progress", False)
        # self.profile.set_preference("browser.download.useDownloadDir", False)
        self.profile.update_preferences()

        self.driver = self.initiate_driver()
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(60)
        self.driver.maximize_window()

    def initiate_driver(self):
        raise NotImplementedError('Please use a implementation class')

    def run(self, **kwargs):
        raise NotImplementedError('Please use a implementation class')

    def take_screenshot(self):
        file_name = self.screenshot_mask.format(self.screenshot_dir,
                                                datetime.strftime(datetime.today(), self.screenshot_date_mask))
        self.driver.save_screenshot(file_name)

    def try_again(self, action, error_index=0, sleep_time=2, **kwargs):
        time.sleep(sleep_time)
        error_index += 1
        function = getattr(self, action)
        try:
            return function(**kwargs)
        except: # Exception, e:
            if error_index >= 3:
                # get print screen
                date_string = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')

                if hasattr(settings, 'SCREENSHOT_PATH'):
                    screenshot_dir = settings.SCREENSHOT_PATH
                else:
                    screenshot_dir = ''

                png_filename = '%s_%s_%s.png' % (action, error_index, date_string)
                screenshot_name = os.path.join(screenshot_dir, png_filename)

                self.driver.get_screenshot_as_file(screenshot_name)
                self.driver.quit()
                # raise e
            self.try_again(action, error_index, **kwargs)

    def remove_accentuation(self, string):
        if isinstance(string, unicode):
            return_string = unicodedata.normalize("NFKD", string).encode('ascii', 'ignore')
        else:
            return_string = unicodedata.normalize("NFKD", string.decode('utf-8')).encode('ascii', 'ignore')

        return_string = return_string.replace('\\t', '')
        return_string = return_string.replace('\\n', '')
        return_string = return_string.replace("\'", '')

        return return_string

    def retry_if_fail(self, action, error_index=0, retry_times=3, **kwargs):
        error_index += 1
        function = getattr(self, action)
        try:
            return function(**kwargs)
        except (RobotStop, e):
            raise e
        except (RobotStopAll, e):
            raise e
        except (Exception, e):
            if error_index >= retry_times:
                self.take_screenshot()
                raise RobotStop(e)
            self.retry_if_fail(action, error_index, **kwargs)

    def wait_by_element_id(self, element_id):
        self.wait.until(lambda driver: driver.find_element_by_id(element_id))

    def wait_by_css_selector(self, css_selector):
        self.wait.until(lambda driver: driver.css_selector(css_selector))

    def wait_by_element_by_xpath(self, xpath):
        self.wait.until(lambda driver: driver.find_element_by_xpath(xpath))

    def wait_by_element_class_name(self, class_name):
        self.wait.until(lambda driver: driver.find_element_by_class_name(class_name))

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass


class RobotWebdriver(BaseSelenium):

    def initiate_driver(self):
        return webdriver.Firefox(firefox_profile=self.profile)


class RobotRemoteFirefox(BaseSelenium):

    def __init__(self, donwload_dir=r'/Users/user/Documents/robo_screenshot/',
                 screenshot_dir=r'/Users/user/Documents/robo_screenshot/',
                 never_ask_savetodisk='application/pdf,text/plain,application/octet-stream',
                 screenshot_mask='{0}/screenshot_{1}.png', screenshot_date_mask='%Y-%m-%d__%H:%M:%S',
                 command_executor_ip='localhost', command_executor_mask='http://{0}:4444/wd/hub'):

        if not command_executor_ip:
            raise RobotStopAll('Ip cant be null')

        #looking for pref.js
        # caps = webdriver.DesiredCapabilities.FIREFOX
        # caps.update({
        #                 'profile': 'rootair',
        #                 'version': '2',
        #                 'browserName': 'firefox',
        #                 'javascriptEnabled': True
        #             })
        #
        # self.driver = webdriver.Remote(command_executor=command_executor,
        #                                desired_capabilities=caps)
        #
        # if settings.DEBUG:
        #     print('DEBUG ', command_executor)
        self.command_executor = command_executor_mask.format(command_executor_ip)
        # os.environ['no_proxy'] = '{0},127.0.0.1:4444'.format(command_executor_ip)
        super(RobotRemoteFirefox, self).__init__(donwload_dir, screenshot_dir, never_ask_savetodisk,
                                          screenshot_mask, screenshot_date_mask)

    def initiate_driver(self):
        """
        :return:
        """
        return webdriver.Remote(
            command_executor=self.command_executor,
            desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
            browser_profile=self.profile)

    def goto_order_details(self):
        """
        :return: Go to HTML order detail
        """
        try:
            order_details_url = '?action=modifyOrderDetails&workPackageId=%s' % self.work_package.ipm_id
            self.driver.get(settings.IPM_DO_URL+order_details_url)
        except:
            self.driver.find_element_by_css_selector("#wpForm > table > tbody > tr > td > a").click()
        time.sleep(1)

    def test_css_selector(self):
        """
        :return: click para caixa dialogo
        """
        onclick="javascript:ExibeTeclado(); return false;"
        time.sleep(1)
        self.driver.find_element_by_css_selector("input[type=\"image\"]").click()
        self.driver.find_element_by_name("PASSWORD").clear()
        self.driver.find_element_by_name("PASSWORD").send_keys(password)
        self.wait_by_element_class_name('prtlHeaderNotchImgWidth')
        self.html_content = self.driver.page_source

    def get_cpo_status_from_page_source(self):
        """
        :return:
        """
        result = []
        soup = BeautifulSoup(self.driver.page_source)
        table = soup.findAll('table', {'class': 'urSAPTable'})[0]

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 9:
                status = cells[4].text
                cpo_number = cells[8].text
                result.append((cpo_number, status))
        return result


class RobotRemoteChrome( object ):

    def __init__(self, debug=False, proxy=False, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('--kiosk')
        # options.add_argument('--start-maximized')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        options.add_argument('--disk-cache-dir=/var/www/cake2.2.4/app/tmp/cache/selenium-chrome-cache')
        options.add_argument('--no-referrers')
        options.add_argument('--test-type')
        options.add_argument('--window-size=1003,719')
        options.add_argument('--disable-extensions')
        # options.add_argument('--proxy-server=localhost:8118')
        options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")

        prefs = {"download.default_directory" : directory.get('DIR_LOCAL_SCREENSHOT')}
        options.add_experimental_option("prefs",prefs)
        # chromium_path = "/Users/user/Applications/Chromium"
        # options.binary_location = chromium_path
        self.driver = webdriver.Chrome(executable_path=directory.get('DIR_CHROME_DRIVER'), chrome_options=options)

        self.wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(10)