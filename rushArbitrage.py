import json
import pandas as pd
import functools
import os
from functools import lru_cache
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import sys
import pandas as pd
import requests
import json 
from time import sleep
from dotenv import load_dotenv, dotenv_values 

# loading variables from .env file
load_dotenv() 

# Changing my current working directory so my taskScheduler app works well on my local machine
cwd = os.getcwd() 
os.chdir("I:\Personal\Personal_SUBFOLDER\Coding\SportyBet\SportyBet Rush Arbitrage") 
print("Current directory is-", os.getcwd()) 

# Smart waits implemented
def wait_and_find_element(by, value):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

def wait_and_find_elements(by, value):
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((by, value)))


options = Options()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver.maximize_window()


# Code to get the sporty bet website url 
driver.get("https://www.sportybet.com/ng/")

def login(): 

    username = wait_and_find_element(By.XPATH, "//*[@id='j_page_header']/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/input")
    username.send_keys(os.getenv("USERNAMESPORTY"))

    password = wait_and_find_element(By.XPATH, "//*[@id='j_page_header']/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/input")
    password.send_keys(os.getenv("PASSWORDSPORTY"))

    loginBtn = wait_and_find_element(By.XPATH, "//*[@id='j_page_header']/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/button")
    loginBtn.click()
 
# Function to navigate to the virtual bet url focused on rush
def navToRush(): 
    # Hard coding sleep time so the login script works well 
    time.sleep(5)
    driver.get("https://www.sportybet.com/ng/sportygames/rush")

    # Code to skip the tutorial lesson that automatically pops up
    skipTutorial = wait_and_find_element(By.CSS_SELECTOR, "#onboarding > div.nav-links-skip > span > span")
    skipTutorial.click()

    #Hard coding sleep time so element becomes interactable
    time.sleep(2)
    # Code to enable one tap
    enableOneTap = wait_and_find_element(By.XPATH,"//*[@id='__BVID__52___BV_modal_footer_']/button[2]")
    enableOneTap.click()

def placeBet():
    # Code to get staring balance
    startingBalance = int(
            wait_and_find_element(
                By.CSS_SELECTOR,"#app > div > div > div.game-header.px-3 > div.row.row-header.align-items-center.justify-content-between > div.align-items-center.back.d-flex.justify-content-center.pl-1.col-4 > div > div > span:nth-child(2)").text.split(".")[0].replace(",", "")
                )
    # Using try-exception because autoBet button changes after a successful round of betting
    try:
        # Code to click on autoBet Button
        autoBetButton = wait_and_find_element(By.CSS_SELECTOR, "#app > div > div > div.game-area > div.align-items-center.bet-board-bg.d-flex.flex-column > div.row.all-bet-btn-container.default-bet-container.no-gutters.align-items-center.justify-content-center > div > div.align-items-center.auto-bet-btn.d-flex.justify-content-center > div.auto-bet-text > span")
    except:
        time.sleep(3)
        autoBetButton = wait_and_find_element(By.CSS_SELECTOR, "#app > div > div > div.game-area > div.align-items-center.bet-board-bg.d-flex.flex-column > div.row.all-bet-btn-container.no-gutters.align-items-center.justify-content-center.show-auto-bet-container.auto-btn-container > div > div.align-items-center.auto-bet-btn.d-flex.justify-content-center > div.auto-bet-text > span")

    autoBetButton.click()
    
    shouldStopBet = False

    # Code to stop bet if profittable by 200 naira
    for x in range(0, 180):

        # Hardcoded sleep time to constantly check if the bet is profittable
        time.sleep(3)
        # print(f"Starting Balance is: {startingBalance} \n currentBalance is {currentBalance}")
        try: 
            currentBalance = int(
                wait_and_find_element(
                    By.XPATH,"//*[@id='app']/div/div/div[2]/div[2]/div[1]/div/div/span[2]").text.split(".")[0].replace(",", "")
                    )
            
            # Stop bet if 200 naira profit is realized
            if(currentBalance - startingBalance >= 200):
                # stop betting
                stopBetButton = wait_and_find_element(By.CSS_SELECTOR, "#app > div > div > div.game-area > div.align-items-center.bet-board-bg.d-flex.flex-column > div.row.all-bet-btn-container.no-gutters.align-items-center.justify-content-center.stop-btn-container > div > div.row.align-items-center.d-flex.flex-column.justify-content-center.py-1.stop-auto-bet-container.text-center.stop-auto-bet-btn.no-gutters")
                stopBetButton.click()
                print("Bet profittable starting again at your command.....")
                shouldStopBet = True
                x = 200
                break
            if(currentBalance - startingBalance <= -200):
                # stop betting
                stopBetButton = wait_and_find_element(By.CSS_SELECTOR, "#app > div > div > div.game-area > div.align-items-center.bet-board-bg.d-flex.flex-column > div.row.all-bet-btn-container.no-gutters.align-items-center.justify-content-center.stop-btn-container > div > div.row.align-items-center.d-flex.flex-column.justify-content-center.py-1.stop-auto-bet-container.text-center.stop-auto-bet-btn.no-gutters")
                stopBetButton.click()
                print("NO PROFIT starting again at your command.....")
                shouldStopBet = True
                x = 200
                break
            # Code to consatntly give you an update on your profit status 
            print(f" \n Profit Status: {currentBalance - startingBalance}")
        except:
            # There seems to be an exception when the script executes and the hover window showing a winning bet pops up
            print("Exception")

        if(shouldStopBet == True):
            break

login()
navToRush()

# Running a loop 5 times to place a bet
for x in range(1,6):
    placeBet()

# quit driver 
driver.quit()


