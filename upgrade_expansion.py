import os
import time

import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def load_saved_game(driver, filename):
    """Load a saved game."""
    with open(f"saves/{filename}") as fo:
        pyperclip.copy(fo.read())

    driver.get("https://www.swarmsim.com/#/options")
    text_field = driver.find_element(By.ID, "export")
    text_field.clear()
    text_field.send_keys()
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").perform()


def upgrade_expansion(driver, times=1):

    text = ".ng-scope:nth-child(2) > div > .ng-isolate-scope > " \
           ".ng-scope > .ng-scope > .ng-scope > .ng-binding"
    button = ".ng-scope:nth-child(2) > div > .ng-isolate-scope .btn:nth-child(1)"

    n = 0
    while True:
        driver.get("https://www.swarmsim.com/#/tab/larva/unit/larva")
        WebDriverWait(driver, 1805).until(
            expected_conditions.text_to_be_present_in_element(
                (By.CSS_SELECTOR, text),
                "Your next expansion will award 500 crystals."
            )
        )
        driver.find_element(By.CSS_SELECTOR, button).click()

        n+=1
        if n >= times:
            break

        for m in range(29, -1, -1):
            for s in range(59, -1, -1):
                print(
                    f"\rClicked {n} of {times} times."
                    f" {m:02d}:{s:02d}s until the next click.",
                    end='',
                )
                time.sleep(1)


def save_game(driver, filename):
    # Saved a game
    driver.get("https://www.swarmsim.com/#/options")

    text_field = driver.find_element(By.ID, "export")
    text_field.click()
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("c").perform()

    with open(f"saves/{filename}", 'w') as fo:
        fo.write(pyperclip.paste())


def main():
    # Set up
    driver = webdriver.Firefox()
    driver.set_window_size(1078, 901)
    driver.get("https://www.swarmsim.com")

    latest_save = sorted(entry.name for entry in os.scandir("saves"))[-1]
    load_saved_game(driver, latest_save)

    upgrade_expansion(driver, times=20) # minimum 10 hours

    new_save_filename = f"{time.strftime('%Y-%m-%d_%H.%M.%S%z')}.txt"
    save_game(driver, new_save_filename)

    #driver.quit()

if __name__ == "__main__":
    main()
