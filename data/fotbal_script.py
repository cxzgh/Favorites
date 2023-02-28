from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .models import Bookmakers, Fotbal
from collections import Counter
import time


def get_fotbal_data():
    s = Service('D:\chrome driv\chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    url = 'https://www.flashscore.ro'
    driver.get(url)

    actions = ActionChains(driver)

    wait = WebDriverWait(driver, 10)

    cookie = driver.find_element(By.CSS_SELECTOR, 'button[id^=onetrust-accept-btn-handler]')
    if cookie.is_displayed():
        cookie.click()

    fotbal = driver.find_element(By.CSS_SELECTOR, 'a[data-sport-id="1"]')
    fotbal.click()

    ligi = ["ANGLIA: Premier League", "ROMÂNIA: Liga 1 - SuperLiga", "FRANŢA: Ligue 1", "GERMANIA: Bundesliga", "ITALIA: Serie A", "SPANIA: LaLiga"]

    for liga in ligi:

        alege_liga = driver.find_element(By.CSS_SELECTOR, f'div[title="{liga}"]')
        alege_liga.click()
        tara = driver.find_element(By.XPATH, '//*[@id="mc"]/div[4]/div[1]/h2/a[2]').text
        rezultate = driver.find_element(By.CSS_SELECTOR, 'a[id="li1"]')
        rezultate.click()
        while True:

            try:
                time.sleep(0.5)
                afiseaza_mai_mult = driver.find_element(By.CSS_SELECTOR, "a.event__more.event__more--static")
                driver.execute_script("arguments[0].scrollIntoView();", afiseaza_mai_mult)
                driver.execute_script("window.scrollBy(0, -100);")
                actions.move_to_element(afiseaza_mai_mult).click().perform()
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.event__more.event__more--static")))
            except Exception:
                break

        for game in driver.find_elements(By.CSS_SELECTOR, '[id^="g_1_"]'):

            def game_exists(participant1, participant2, data):
                return Fotbal.objects.filter(participant1=participant1, participant2=participant2, data=data).exists()

            driver.execute_script("arguments[0].scrollIntoView();", game)
            driver.execute_script("window.scrollBy(0, -100);")
            actions.move_to_element(game).click().perform()
            driver.switch_to.window(driver.window_handles[1])

            try:
                if driver.find_element(By.CSS_SELECTOR, '.infoBox__wrapper.infoBoxModule').is_displayed():
                    driver.execute_script("arguments[0].remove();", driver.find_element(By.CSS_SELECTOR, '.infoBox__wrapper.infoBoxModule'))
            except NoSuchElementException:
                pass

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

            if game_exists(participant1, participant2, data):
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                break
                # continue
            else:

                if score1 == score2:
                    print(f"Egal {participant1}-{participant2}")
                    rezultat = "Egal"
                    scor = f"{score1}-{score2}"
                else:
                    rezultat = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text
                    print(f"{participant1} {score1}-{score2} {participant2} {rezultat}")
                    scor = f"{score1}-{score2}"

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

                        bookmaker_odd_egal_path = driver.find_element(By.XPATH, f'//*[@id="detail"]/div[7]/div[3]/div/div[2]/div[{i}]/a[3]')
                        bookmaker_odd_egal = bookmaker_odd_egal_path.get_attribute("title")

                    except NoSuchElementException:
                        bookmaker_odd_p1 = "NaN"
                        bookmaker_odd_p2 = "NaN"
                        bookmaker_odd_egal = "Nan"

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
                        cotaX=bookmaker_odd_egal,
                    )
                    bookmakerz.save()
                    bookmakers_list.append(bookmakerz)

                fav_list = Counter(favorite)
                favorita = fav_list.most_common()

                new_game = Fotbal(
                    tara=tara,
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
