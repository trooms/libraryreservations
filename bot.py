from selenium import webdriver
import os
import time

class Bot():
    def __init__(self):
        print(print(os.getcwd()))
        self.driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver')
        self.driver.get('https://libcal.usc.edu/reserve/lvl2')
        self.driver.find_element_by_xpath("//*[contains(text(), '202B')]").click();
        # self.driver.find_element_by_xpath('//*[@id="eq-time-grid"]/div[1]/div[1]/button[2]').click();

def main():
    my_bot = Bot()

if __name__ == '__main__':
    main()
