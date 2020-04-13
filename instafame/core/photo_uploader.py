'''
This code is based on shriar's and ozkc's previous work.
Check it out here:
    @shriar: https://github.com/shriar/Insta-post
    @ozkc: https://github.com/ozkc/selenium-instagram-uploader
'''
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PhotoUploader():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        mobile_emulation = {"deviceName": "Nexus 5"}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation",
                                               mobile_emulation)
        chrome_options.add_experimental_option('prefs', {"geolocation": True})
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    # TODO: login should be decopled in at least three functions:
    #   login itself.
    #   save your info login.
    #   add to home screen
    def login(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(1)

        # Set username, password and submit.
        username_input = self.browser.find_element_by_xpath(
            "//input[@name='username']")
        username_input.send_keys(self.email)
        password_input = self.browser.find_element_by_xpath(
            "//input[@name='password']")
        password_input.send_keys(self.password)
        password_input.submit()

        time.sleep(3)

        # save your info pop-up.
        not_now = self.browser.find_element_by_xpath(
            '//button[text()="Not Now"]')
        not_now.click()

        time.sleep(3)

        # add to home screen pop-up.
        # TODO: sometimes it fails with:
        #       selenium.common.exceptions.WebDriverException: Message: chrome not reachable
        # check it out.
        not_now = self.browser.find_element_by_xpath(
            '//button[text()="Cancel"]')
        not_now.click()

    def upload_pic(self, caption):
        '''
            After clicking + button to upload a picture a system window will
            appear to choose it, autokey manages this.
            Learn more from here: https://github.com/autokey/autokey
        '''
        new_post_btn = self.browser.find_element_by_xpath(
            "//div[@role='menuitem']")
        new_post_btn.click()

        os.system('/usr/bin/autokey-run -s image_select')
        time.sleep(6)

        button = self.browser.find_elements_by_xpath(
            "//*[contains(text(), 'Expand')]")
        if len(button) > 0:
            button[0].click()
        next_btn = self.browser.find_element_by_xpath(
            "//button[contains(text(),'Next')]").click()
        time.sleep(2)

        caption_field = self.browser.find_element_by_xpath(
            "//textarea[@aria-label='Write a caption…']")
        caption_field.send_keys(caption)
        share_btn = self.browser.find_element_by_xpath(
            "//button[contains(text(),'Share')]").click()
