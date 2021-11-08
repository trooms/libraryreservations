import os
import time
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class RSFBot:
    def __init__(self, args):
        self.initURL = 'https://libcal.usc.edu/space/18367'
        self.usernames = args['usernames']
        self.passwords = args['passwords']
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.service = Service(f'{os.getcwd()}/chromedriver')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.userIndex = 0
        self.driver.implicitly_wait(6)

    def init_browser(self):
        self.driver.get(self.initURL)
        while self.driver.current_url != self.initURL:
            time.sleep(0.5)


    def select_closest_timeslot(self):
        nextAvailable = self.driver.find_element(By.XPATH, '//*[@id="eq-time-grid"]/div[1]/div[1]/button[2]')
        try:
            nextAvailable.click()
        except:
            time.sleep(1)
            try:
                self.driver.find_element(By.XPATH, '//*[@id="eq-time-grid"]/div[1]/div[1]/button[2]').click()
            except:
                pass
            pass
        time.sleep(1)
        i = 1
        while self.driver.current_url == self.initURL:
            try:
                slot = self.driver.find_element(By.XPATH, f'//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/table/tbody/tr/td/div/div[2]/div[{i}]')
            except:
                break
            try:
                slot.click()
            except:
                pass
            time.sleep(0.1)
            i += 1
        time.sleep(1)
        submitButton = self.driver.find_element(By.XPATH, f'//*[@id="submit_times"]')
        try:
            submitButton.click()
            return True
        except:
            return False

    def auth_uscid(self):
        while self.driver.current_url == self.initURL:
            time.sleep(0.5)
        time.sleep(1)
        try:
            username_field = self.driver.find_element(By.ID, 'username')
        except:
            time.sleep(3)
            username_field = self.driver.find_element(By.ID, 'username')
        try:
            username_field.send_keys(self.usernames[self.userIndex])
        except:
            time.sleep(2)
            self.driver.find_element(By.ID, 'username').send_keys(self.usernames[self.userIndex])

        password_field = self.driver.find_element(By.ID, 'password')
        password_field.send_keys(self.passwords[self.userIndex])
        time.sleep(0.25)
        self.driver.find_element(By.XPATH, '//*[@id="loginform"]/div/button').click()

    def reserve(self):
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH, '//*[@id="terms_accept"]').click()
        except:
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="terms_accept"]').click()

        self.driver.find_element(By.XPATH, '//*[@id="s-lc-eq-bform-submit"]').click()
        time.sleep(1)
        if 'Sorry, this exceeds the limit per day in this location' in self.driver.page_source:
            self.driver.find_element(By.XPATH, '//*[@id="eid_18367"]/td[6]/button').click()
        time.sleep(2)
        self.reset()

    def reset(self):
        self.driver.quit()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.userIndex += 1
        if self.userIndex >= len(self.usernames):
            self.userIndex = 0
        self.run()

    def run(self):
        time.sleep(1)
        self.init_browser()
        if not self.select_closest_timeslot():
            print("SUCCESSFULLY BOOKED ALL SLOTS")
            self.driver.quit()
            return
        self.auth_uscid()
        self.reserve()

if __name__ == '__main__':
    colnames = ['name', 'username', 'password']
    data = pandas.read_csv('logins.csv', names=colnames)

    usernames = data.username.tolist()
    passwords = data.password.tolist()

    logins = {'usernames': usernames, 'passwords': passwords}
    bot = RSFBot(logins)
    try:
        bot.run()
    except:
        time.sleep(1)
        bot.reset()

