from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .models import Bookmakers, Tennis
from collections import Counter
import time


def get_tennis_data():
    s = Service('D:\chrome driv\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    url = 'https://www.flashscore.ro'
    driver.get(url)

    actions = ActionChains(driver)

    wait = WebDriverWait(driver, 10)

    cookie = driver.find_element(By.CSS_SELECTOR, 'button[id^=onetrust-accept-btn-handler]')
    if cookie.is_displayed():
        cookie.click()

    tennis = driver.find_element(By.CSS_SELECTOR, 'a[data-sport-id="2"]')
    tennis.click()

    ligi = ["ATP - SIMPLU: Wimbledon", "ATP - SIMPLU: French Open",  "ATP - SIMPLU: Australian Open", "ATP - SIMPLU: US Open"]

    for liga in ligi:
        alege_liga = driver.find_element(By.CSS_SELECTOR, f'div[title="{liga}"]')
        alege_liga.click()
        rezultate = driver.find_element(By.CSS_SELECTOR, 'a[id="li1"]')
        rezultate.click()

        while True:
            try:
                time.sleep(0.5)
                afiseaza_mai_mult = driver.find_element(By.CSS_SELECTOR, "a.event__more.event__more--static")
                driver.execute_script("arguments[0].scrollIntoView();", afiseaza_mai_mult)
                driver.execute_script("window.scrollBy(0, -100);")
                actions.move_to_element(afiseaza_mai_mult).click().perform()
                wait = WebDriverWait(driver, 5)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.event__more.event__more--static")))
            except Exception:
                break

        for game in driver.find_elements(By.CSS_SELECTOR, '[id^="g_2_"]'):

            def game_exists(participant1, participant2, data):
                return Tennis.objects.filter(participant1=participant1, participant2=participant2, data=data).exists()

            driver.execute_script("arguments[0].scrollIntoView();", game)
            driver.execute_script("window.scrollBy(0, -100);")
            actions.move_to_element(game).click().perform()
            driver.switch_to.window(driver.window_handles[1])

            try:
                if driver.find_element(By.CSS_SELECTOR, '.infoBox__wrapper.infoBoxModule').is_displayed():
                    driver.execute_script("arguments[0].remove();", driver.find_element(By.CSS_SELECTOR, '.infoBox__wrapper.infoBoxModule'))
            except NoSuchElementException:
                pass

            neprezentare = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[2]/span').text

            if neprezentare == "NEPREZENTARE":
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue
            else:
                tournament = driver.find_element(By.CLASS_NAME, 'tournamentHeader__country')
                liga_si_runda_driver = tournament.find_element(By.CSS_SELECTOR, 'a').text
                liga_si_runda = liga_si_runda_driver.rsplit("-", 1)
                liga = liga_si_runda[0]
                runda = liga_si_runda[1]
                data_si_ora = driver.find_element(By.CLASS_NAME, "duelParticipant__startTime").text
                data = data_si_ora.split(" ", 1)[0]
                participant1 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text
                participant2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text
                score1 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[1]/span[1]').text
                score2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[1]/span[3]').text

                print(liga_si_runda)

                if game_exists(participant1, participant2, data):
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    # break
                    continue
                else:
                    rezultat = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text
                    scor = f"{score1}-{score2}"
                    print(f"{participant1} {score1}-{score2} {participant2} {rezultat}")

                    try:
                        cote_tab = driver.find_element(By.CSS_SELECTOR, 'a.tabs__tab[href="#/comparare-cote"]')
                    except NoSuchElementException:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue

                    driver.execute_script("arguments[0].scrollIntoView();", cote_tab)
                    driver.execute_script("window.scrollBy(0, -100);")
                    actions.move_to_element(cote_tab).click().perform()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.oddsCell__bookmaker a.prematchLink')))
                    bookmakers = driver.find_elements(By.CSS_SELECTOR, '.oddsCell__bookmaker a.prematchLink')

                    i = 1

                    bookmakers_list = []
                    favorite = []

                    for bookmaker in bookmakers:

                        bookmaker_name = bookmaker.get_attribute("title")
                        bookmaker_obj, created = Bookmakers.objects.get_or_create(bookmaker=bookmaker_name)

                        try:
                            bookmaker_odd_p1_path = driver.find_element(By.XPATH, f'//*[@id="detail"]/div[7]/div[3]/div/div[2]/div[{i}]/a[1]')
                            bookmaker_odd_p1 = bookmaker_odd_p1_path.get_attribute("title")

                            bookmaker_odd_p2_path = driver.find_element(By.XPATH, f'//*[@id="detail"]/div[7]/div[3]/div/div[2]/div[{i}]/a[2]')
                            bookmaker_odd_p2 = bookmaker_odd_p2_path.get_attribute("title")
                        except NoSuchElementException:
                            bookmaker_odd_p1 = "NaN"
                            bookmaker_odd_p2 = "NaN"
                        i += 1

                        cota_p1 = bookmaker_odd_p1.rsplit("» ", 1)
                        cota_p2 = bookmaker_odd_p2.rsplit("» ", 1)

                        try:
                            if cota_p1[1] < cota_p2[1]:
                                favorita = participant1
                                favorite.append(favorita)
                            else:
                                favorita = participant2
                                favorite.append(favorita)
                        except IndexError:
                            favorita = "no data"
                            favorite.append(favorita)

                        bookmakerz = Bookmakers(
                            bookmaker=bookmaker_obj,
                            bookmaker_name=bookmaker_name,
                            cotaP1=bookmaker_odd_p1,
                            cotaP2=bookmaker_odd_p2,
                        )
                        bookmakerz.save()
                        bookmakers_list.append(bookmakerz)

                    fav_list = Counter(favorite)
                    favorita = fav_list.most_common()

                    new_game = Tennis(
                        liga=liga,
                        runda=runda,
                        data=data,
                        participant1=participant1,
                        participant2=participant2,
                        scor=scor,
                        rezultat=rezultat,
                        favorita=favorita[0][0],
                    )
                    new_game.save()
                    new_game.bookmaker_odds.set(bookmakers_list)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
