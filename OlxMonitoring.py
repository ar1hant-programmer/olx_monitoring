from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as Except
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.window import WindowTypes
from bs4 import BeautifulSoup as BS
from webdriver_manager.chrome import ChromeDriverManager
import requests
import telebot
import time
import os

# Token Bot
Bot = telebot.TeleBot("5584157050:AAEtaQkQ6ssxds0bvDUpqV75USdhUQQCG0Y")


# Get Chat ID
@Bot.message_handler(commands=['start'])
def start(message):
    global username
    username = message.chat.id
    Bot.send_message(username, text="<b>Бот успешно запущен!</b>\n\nОжидание данных от парсера...", parse_mode="HTML")


# Create Webdriver
options = webdriver.ChromeOptions()

# User-Agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Chrome/84.0")

# Options
options.add_argument("--window-size=960,1080")
options.add_argument("--disable-crash-reporter")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-in-process-stack-traces")
options.add_argument("--disable-logging")
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--log-level=3')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
options.set_capability("acceptInsecureCerts", True)

# Headless Mode
options.add_argument("--headless")

# Path To ChromeDriver.exe
executable_path = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=executable_path, options=options)
os.system("clear")

options_filters = ({"Type": "-",
                    "Price": "-",
                    "NumberOfRooms": "-",
                    "Furnishing": "-",
                    "Commission": "-",
                    "SquareOfRooms": "-",
                    "Floor": "-",
                    "Repair": "-",
                    "Ratio": "-"
                    },

                   {"Type": "-",
                    "Price": "-",
                    "Commission": "-",
                    "SquareOfRooms": "-",
                    "Ratio": "-"})

ratio_array = []
double_links = []


def action_with_program(function, value):
    os.system("clear")
    function(value)


# Parser Of Old Advertisements
def getting_publications():
    # Applying Parameters For First Links
    def parameters_for_first_links(value):

        user_choice = input(
            f"Настройки параметров для ссылки - {value}:\n\n"
            f"1. Тип жилья (Текущее значение: {options_filters[0]['Type']})\n"
            f"2. Цена (Текущее значение: {' '.join(options_filters[0]['Price'])})\n"
            f"3. Количество комнат (Текущее значение: {' '.join(options_filters[0]['NumberOfRooms'])})\n"
            f"4. Меблирование (Текущее значение: {options_filters[0]['Furnishing']})\n"
            f"5. Комиссионные (Текущее значение: {options_filters[0]['Commission']})\n"
            f"6. Площадь (Текущее значение: {' '.join(options_filters[0]['SquareOfRooms'])})\n"
            f"7. Этаж (Текущее значение: {' '.join(options_filters[0]['Floor'])})\n"
            f"8. Ремонт (Текущее значение: {' '.join(options_filters[0]['Repair'])})\n"
            f"9. Цена за кв. метр (Текущее значение: {options_filters[0]['Ratio']})\n"
            f"10. Продолжить\n\nВыбор (цифра): ")

        if user_choice == "1":
            os.system("clear")
            answer = input("Тип жилья:\n1. Новостройки\n2. Вторичный рынок\n3. Назад в меню\n\nВыбор: ")

            if answer != "3":
                if answer == "1":
                    options_filters[0]["Type"] = "Новостройки"
                    action_with_program(parameters_for_first_links, value)
                else:
                    options_filters[0]["Type"] = "Вторичный рынок"
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "2":
            os.system("clear")
            answer = input("Цена (Пример: 1000000 2500000):\n1. Назад в меню\n\nВыбор: ").split(" ")

            if answer[0] != "1":
                if len(answer) == 1:
                    options_filters[0]["Price"] = answer
                    action_with_program(parameters_for_first_links, value)
                else:
                    options_filters[0]["Price"] = answer[0], answer[1]
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "3":
            os.system("clear")
            answer = input("Количество комнат (Пример: 1* 3):\n1. Назад в меню\n\nВыбор: ").split(" ")

            if answer[0] != "1":
                if len(answer) == 1:
                    if answer == "1*":
                        options_filters[0]["NumberOfRooms"] = answer[:-1]
                        action_with_program(parameters_for_first_links, value)
                    else:
                        options_filters[0]["NumberOfRooms"] = answer
                        action_with_program(parameters_for_first_links, value)
                else:
                    if answer[0] == "1*":
                        answer[0] = answer[0][:-1]
                    options_filters[0]["NumberOfRooms"] = answer[0], answer[1]
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "4":
            os.system("clear")
            answer = input("Меблирование:\n1. Да\n2. Нет\n3. Назад в меню\n\nВыбор: ")

            if answer != "3":
                if answer == "1":
                    options_filters[0]["Furnishing"] = "Да"
                    action_with_program(parameters_for_first_links, value)
                else:
                    options_filters[0]["Furnishing"] = "Нет"
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "5":
            os.system("clear")
            answer = input("Комиссионные:\n1. Да\n2. Нет\n3. Назад в меню\n\nВыбор: ")

            if answer != "3":
                if answer == "1":
                    options_filters[0]["Commission"] = "Да"
                    action_with_program(parameters_for_first_links, value)
                else:
                    options_filters[0]["Commission"] = "Нет"
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "6":
            os.system("clear")
            answer = input("Площадь (Пример: 1* 31):\n1. Назад в меню\n\nВыбор: ").split(" ")

            if answer[0] != "1":
                if len(answer) == 1:
                    if answer == "1*":
                        options_filters[0]["SquareOfRooms"] = answer[:-1]
                        action_with_program(parameters_for_first_links, value)
                    else:
                        options_filters[0]["SquareOfRooms"] = answer
                        action_with_program(parameters_for_first_links, value)
                else:
                    if answer[0] == "1*":
                        answer[0] = answer[0][:-1]
                    options_filters[0]["SquareOfRooms"] = answer[0], answer[1]
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "7":
            os.system("clear")
            answer = input("Этаж (Пример: 1* 9):\n1. Назад в меню\n\nВыбор: ").split(" ")

            if answer[0] != "1":
                if len(answer) == 1:
                    if answer == "1*":
                        options_filters[0]["Floor"] = answer[:-1]
                        action_with_program(parameters_for_first_links, value)
                    else:
                        options_filters[0]["Floor"] = answer
                        action_with_program(parameters_for_first_links, value)
                else:
                    if answer[0] == "1*":
                        answer[0] = answer[0][:-1]
                    options_filters[0]["Floor"] = answer[0], answer[1]
                    action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "8":
            os.system("clear")
            answer = input(
                "Ремонт (Пример: 1 3 5):\n1. Авторский проект\n2. Евроремонт\n3. Средний\n4. Требует ремонта\n5. Черновая отделка\n6. Предчистовая отделка\n7. Назад в меню\nВыбор: ").split(
                " ")

            if answer[0] != "7":
                options_filters[0]["Repair"] = ""
                for count in range(len(answer)):
                    options_filters[0]["Repair"] = options_filters[0]["Repair"] + f" {answer[count]}"
                options_filters[0]["Repair"] = options_filters[0]["Repair"].split(" ")
                action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "9":
            os.system("clear")
            answer = input("Цена за кв. метр:\n1. Назад в меню\n\nВыбор: ").replace(",", ".")

            if answer != "1":
                options_filters[0]["Ratio"] = answer
                ratio_array.append(float(options_filters[0]['Ratio']))
                action_with_program(parameters_for_first_links, value)
            else:
                action_with_program(parameters_for_first_links, value)

        elif user_choice == "10":
            os.system("clear")

        else:
            print("Некорректные данные. Пожалуйста, попробуйте ещё раз.")
            time.sleep(2)
            action_with_program(parameters_for_first_links, value)

    # Applying Parameters For Second Links
    def parameters_for_second_links(value):

        user_choice = input(
            f"Настройки параметров для ссылки - {value}:\n\n"
            f"1. Тип недвижимости (Текущее значение: {' '.join(options_filters[1]['Type'])})\n"
            f"2. Цена (Текущее значение: {' '.join(options_filters[1]['Price'])})\n"
            f"3. Комиссионные (Текущее значение: {options_filters[1]['Commission']})\n"
            f"4. Площадь (Текущее значение: {' '.join(options_filters[1]['SquareOfRooms'])})\n"
            f"5. Цена за кв. метр (Текущее значение: {options_filters[1]['Ratio']})\n"
            f"6. Продолжить\n\nВыбор (цифра): ")

        if user_choice == "1":
            os.system("clear")
            user_answer = input(
                "Тип недвижимости (Пример: 1 3 5):\n"
                "1. Магазины/бутики\n"
                "2. Салоны\n"
                "3. Рестораны/кафе/бары\n"
                "4. Офисы\n"
                "5. Склады\n"
                "6. Отдельно стоящие здания\n"
                "7. Базы отдыха\n"
                "8. Помещения промышленного назначения\n"
                "9. Помещения свободного назначения\n"
                "10. МАФ\n"
                "11. Часть здания\n"
                "12. Другое\n"
                "13. Назад в меню\n\n"
                "Выбор: ").split(" ")

            if user_answer[0] != "13":
                options_filters[1]["Type"] = ""
                for count in range(len(user_answer)):
                    options_filters[1]["Type"] = options_filters[1]["Type"] + f" {user_answer[count]}"
                options_filters[1]["Type"] = options_filters[1]["Type"].split(" ")
                action_with_program(parameters_for_second_links, value)
            else:
                action_with_program(parameters_for_second_links, value)

        elif user_choice == "2":
            os.system("clear")
            answer = input("Цена (Пример: 1000000 2500000):\n1. Назад в меню\n\nВыбор: ").split(" ")

            if answer[0] != "1":
                if len(answer) == 1:
                    options_filters[1]["Price"] = answer
                    action_with_program(parameters_for_second_links, value)
                else:
                    options_filters[1]["Price"] = answer[0], answer[1]
                    action_with_program(parameters_for_second_links, value)
            else:
                action_with_program(parameters_for_second_links, value)

        elif user_choice == "3":

            os.system("clear")

            answer = input("Комиссионные:\n1. Да\n2. Нет\n3. Назад в меню\n\nВыбор: ")

            if answer != "3":
                if answer == "1":
                    options_filters[1]["Commission"] = "Да"
                    action_with_program(parameters_for_second_links, value)

                else:
                    options_filters[1]["Commission"] = "Нет"
                    action_with_program(parameters_for_second_links, value)
            else:
                action_with_program(parameters_for_second_links, value)

        elif user_choice == "4":
            os.system("clear")
            answer = input("Площадь (Пример: 1* 31):\n1. Назад в меню\n\nВыбор: ").split(" ")

            if answer[0] != "1":
                if len(answer) == 1:
                    if answer == "1*":
                        options_filters[1]["SquareOfRooms"] = answer[:-1]
                        action_with_program(parameters_for_second_links, value)
                    else:
                        options_filters[1]["SquareOfRooms"] = answer
                        action_with_program(parameters_for_second_links, value)
                else:
                    if answer[0] == "1*":
                        answer[0] = answer[0][:-1]
                    options_filters[1]["SquareOfRooms"] = answer[0], answer[1]
                    action_with_program(parameters_for_second_links, value)
            else:
                action_with_program(parameters_for_second_links, value)

        elif user_choice == "5":
            os.system("clear")
            answer = input("Цена за кв. метр:\n1. Назад в меню\n\nВыбор: ").replace(",", ".")

            if answer != "1":
                options_filters[1]["Ratio"] = answer
                ratio_array.append(float(options_filters[1]['Ratio']))

                action_with_program(parameters_for_second_links, value)
            else:
                action_with_program(parameters_for_second_links, value)

        elif user_choice == "6":
            os.system("clear")

        else:
            print("Некорректные данные. Пожалуйста, попробуйте ещё раз.")
            time.sleep(2)
            action_with_program(parameters_for_second_links, value)

    def parameters_execute(boolean):

        def execute_first_parameters():
            print("Выставление всех значений...")
            if options_filters[0]["Type"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[2]/div/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                type_ = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located(
                        (By.CSS_SELECTOR,
                         'div.css-7xjci5:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'))
                )
                type_.click()

                if options_filters[0]["Type"] == "Новостройки":
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[3]/div/div/div[2]/div/div[2]/label/p'))
                    )
                    input_type.click()

                    try:
                        check = WebDriverWait(driver, 2).until(
                            Except.visibility_of_element_located((By.CSS_SELECTOR,
                                                                  '#mainContent > div.css-1nvt13t > form > div:nth-child(3) > div.css-tx3aze > div > div:nth-child(3) > div > div > div.css-1wg12ds > div > div:nth-child(2) > label > div > svg.css-o9okd9'))
                        )
                    except:
                        time.sleep(1)

                        input_type.click()
                else:
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[3]/div/div/div[2]/div/div[3]/label/p'))
                    )
                    input_type.click()

                    try:
                        check = WebDriverWait(driver, 2).until(
                            Except.visibility_of_element_located((By.CSS_SELECTOR,
                                                                  '#mainContent > div.css-1nvt13t > form > div:nth-child(3) > div.css-tx3aze > div > div:nth-child(3) > div > div > div.css-1wg12ds > div > div:nth-child(3) > label > div > svg'))
                        )
                    except:
                        time.sleep(1)

                        input_type.click()

                time.sleep(1)

                close_type = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located((By.XPATH,
                                                          '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[3]/div/div/div[1]/div/span'))
                )
                close_type.click()

            if options_filters[0]["Price"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[3]/div/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                if len(options_filters[0]["Price"]) == 2:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["Price"][0])

                    time.sleep(1)

                    type_DO = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_DO.click()

                    time.sleep(1)

                    type_DO.send_keys(options_filters[0]["Price"][1])

                    time.sleep(1)

                    type_DO.send_keys(Keys.ENTER)
                else:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["Price"][0])

                    time.sleep(1)

                    type_OT.send_keys(Keys.ENTER)

            if options_filters[0]["Furnishing"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[4]/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                type_ = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located(
                        (By.XPATH,
                         '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[5]/div/div/div[1]/div/span'))
                )
                type_.click()

                if options_filters[0]["Furnishing"] == "Да":
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[5]/div/div/div[2]/div/div[2]/label/p'))
                    )
                    input_type.click()

                    time.sleep(1)
                else:
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[5]/div/div/div[2]/div/div[3]/label/p'))
                    )
                    input_type.click()

                    time.sleep(1)

                close_type = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located((By.XPATH,
                                                          '//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[5]/div/div/div[1]/div'))
                )
                close_type.click()

            if options_filters[0]["Commission"] != "-":

                type_ = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located(
                        (
                            By.XPATH,
                            '/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[6]/div/div/div[1]/div/span'))
                )
                type_.click()

                if options_filters[0]["Commission"] == "Да":
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              '/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[6]/div/div/div[2]/div/div[2]/label/p'))
                    )
                    input_type.click()

                    time.sleep(1)
                else:
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              '/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[6]/div/div/div[2]/div/div[3]/label/p'))
                    )
                    input_type.click()

                    time.sleep(1)

                close_type = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located((By.XPATH,
                                                          '/html/body/div[1]/div[2]/div[2]/form/div[3]/div[1]/div/div[6]/div/div/div[1]/div'))
                )
                close_type.click()

            if options_filters[0]["NumberOfRooms"] != "-":

                if len(options_filters[0]["NumberOfRooms"]) == 2:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(7) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["NumberOfRooms"][0])

                    time.sleep(1)

                    type_DO = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(7) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_DO.click()
                    type_DO.send_keys(options_filters[0]["NumberOfRooms"][1])

                    time.sleep(1)

                    type_DO.send_keys(Keys.ENTER)
                else:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(7) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["NumberOfRooms"][0])

                    time.sleep(1)

                    type_OT.send_keys(Keys.ENTER)

            if options_filters[0]["SquareOfRooms"] != "-":

                if len(options_filters[0]["SquareOfRooms"]) == 2:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(8) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["SquareOfRooms"][0])

                    time.sleep(1)

                    type_DO = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(8) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_DO.click()

                    time.sleep(1)

                    type_DO.send_keys(options_filters[0]["SquareOfRooms"][1])

                    time.sleep(1)

                    type_DO.send_keys(Keys.ENTER)
                else:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(8) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["SquareOfRooms"][0])

                    time.sleep(1)

                    type_OT.send_keys(Keys.ENTER)

            if options_filters[0]["Floor"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[7]/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                if len(options_filters[0]["Floor"]) == 2:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(9) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["Floor"][0])

                    time.sleep(1)

                    type_DO = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(9) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_DO.click()

                    time.sleep(1)

                    type_DO.send_keys(options_filters[0]["Floor"][1])

                    time.sleep(1)

                    type_DO.send_keys(Keys.ENTER)
                else:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(9) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[0]["Floor"][0])

                    time.sleep(1)

                    type_OT.send_keys(Keys.ENTER)

            if options_filters[0]["Repair"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[7]/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                type_ = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located(
                        (By.XPATH, '/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[10]/div/div/div/div/span'))
                )
                type_.click()

                for _index_ in range(1, len(options_filters[0]["Repair"])):
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              f'/html/body/div/div[2]/div[2]/form/div[3]/div[1]/div/div[10]/div/div/div[2]/div/div[{str(int(options_filters[0]["Repair"][_index_]) + 1)}]/label/p'))
                    )
                    time.sleep(2)

                    input_type.click()

                close_type = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located((By.CSS_SELECTOR,
                                                          '#mainContent > div.css-1nvt13t > form > div:nth-child(3) > div.css-tx3aze > div > div:nth-child(10) > div > div > div:nth-child(1) > div'))
                )
                close_type.click()

        def execute_second_parameters():
            print("Выставление всех значений...")
            if options_filters[1]["Type"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='/html/body/div[1]/div[2]/div[2]/form/div[3]/div[1]/div/div[2]/div/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                type_ = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located(
                        (
                            By.XPATH,
                            '/html/body/div[1]/div[2]/div[2]/form/div[3]/div[1]/div/div[3]/div/div/div/div/span'))
                )
                type_.click()

                for _index_ in range(1, len(options_filters[1]["Type"])):
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              f'//*[@id="mainContent"]/div[2]/form/div[3]/div[1]/div/div[3]/div/div/div[2]/div/div[{str(int(options_filters[1]["Type"][_index_]) + 1)}]/label'))
                    )
                    time.sleep(2)
                    input_type.click()

                close_type = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located((By.XPATH,
                                                          '/html/body/div[1]/div[2]/div[2]/form/div[3]/div[1]/div/div[3]/div/div/div/div'))
                )
                close_type.click()

            if options_filters[1]["Price"] != "-":

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='/html/body/div[1]/div[2]/div[2]/form/div[3]/div[1]/div/div[3]/div/p')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                if len(options_filters[1]["Price"]) == 2:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[1]["Price"][0])

                    time.sleep(1)

                    type_DO = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_DO.click()

                    time.sleep(1)

                    type_DO.send_keys(options_filters[1]["Price"][1])

                    time.sleep(1)

                    type_DO.send_keys(Keys.ENTER)
                else:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[1]["Price"][0])

                    time.sleep(1)

                    type_OT.send_keys(Keys.ENTER)

            if options_filters[1]["SquareOfRooms"] != "-":

                if len(options_filters[1]["SquareOfRooms"]) == 2:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[1]["SquareOfRooms"][0])

                    time.sleep(1)

                    type_DO = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_DO.click()

                    time.sleep(1)

                    type_DO.send_keys(options_filters[1]["SquareOfRooms"][1])

                    time.sleep(1)

                    type_DO.send_keys(Keys.ENTER)
                else:
                    type_OT = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located(
                            (By.CSS_SELECTOR,
                             'div.css-1y0lxug:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)'))
                    )
                    type_OT.click()

                    time.sleep(1)

                    type_OT.send_keys(options_filters[1]["SquareOfRooms"][0])

                    time.sleep(1)

                    type_OT.send_keys(Keys.ENTER)

            if options_filters[1]["Commission"] != "-":

                type_ = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located(
                        (By.XPATH,
                         '/html/body/div[1]/div[2]/div[2]/form/div[3]/div[1]/div/div[6]/div/div/div[1]/div/span'))
                )
                type_.click()

                if options_filters[1]["Commission"] == "Да":
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.CSS_SELECTOR,
                                                              'div.css-1rfy03l:nth-child(2) > label:nth-child(1) > p:nth-child(3)'))
                    )

                    time.sleep(2)

                    input_type.click()
                else:
                    input_type = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.CSS_SELECTOR,
                                                              'div.css-1rfy03l:nth-child(3) > label:nth-child(1) > p:nth-child(3)'))
                    )

                    time.sleep(2)

                    input_type.click()

                close_type = WebDriverWait(driver, 10).until(
                    Except.visibility_of_element_located((By.CSS_SELECTOR,
                                                          'div.css-7xjci5:nth-child(6) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)'))
                )
                close_type.click()

        if boolean:
            execute_first_parameters()
        else:
            execute_second_parameters()

    def options_filters_return(boolean):
        if boolean:
            options_filters[0]["Type"] = "-"
            options_filters[0]["Price"] = "-"
            options_filters[0]["NumberOfRooms"] = "-"
            options_filters[0]["Furnishing"] = "-"
            options_filters[0]["Commission"] = "-"
            options_filters[0]["SquareOfRooms"] = "-"
            options_filters[0]["Floor"] = "-"
            options_filters[0]["Repair"] = "-"
            options_filters[0]["Ratio"] = "-"
        else:
            options_filters[1]["Type"] = "-"
            options_filters[1]["Price"] = "-"
            options_filters[1]["Commission"] = "-"
            options_filters[1]["SquareOfRooms"] = "-"
            options_filters[1]["Ratio"] = "-"

    def check_of_true_title(name, html, cut):
        except_value = "не указано"
        for index in range(3, 10):
            value = html.select(f"li.css-1r0si1e:nth-child({index}) > p:nth-child(1)")
            try:
                if f"{name}" in value[0].text:
                    return value[0].text[cut:]
                elif index == 10:
                    return except_value
            except:
                pass

    def html_select_requests(href):
        global publication_title, square_of_rooms, floor_of_room, number_of_storeys, description_publication, price_publication, date_publication, id_publication
        response = requests.get(href)
        html_parser = BS(response.content, 'html.parser')
        publication_title = html_parser.select(".css-1juynto")[0].text
        square_of_rooms = check_of_true_title("Общая площадь:", html_parser, 15)
        floor_of_room = check_of_true_title("Этаж:", html_parser, 6)
        number_of_storeys = check_of_true_title("Этажность дома:", html_parser, 16)
        description_publication = html_parser.select(".css-1t507yq")[0].text
        price_publication = html_parser.select(".css-12vqlj3")[0].text
        date_publication = html_parser.select(".css-19yf5ek")[0].text
        id_publication = html_parser.select(".css-12hdxwj")[0].text[4:]

    def parser_function(number, flag):
        find = WebDriverWait(driver, 3).until(
            Except.visibility_of_element_located((By.XPATH,
                                                  f'//div[contains(@data-testid,"l-card")][{number}]/a'))
        )
        link_to_publication = find.get_attribute('href')

        if number == 2:
            double_links.append(link_to_publication)

        html_select_requests(link_to_publication)

        if not ratio_array:
            Bot.send_message(username, f'<b>Название:</b>\n{publication_title}\n\n'
                                       f'<b>Описание:</b>\n{description_publication}\n\n'
                                       f'<b>Общая площадь:</b> {square_of_rooms}\n\n'
                                       f'<b>Этаж:</b> {floor_of_room}\n\n'
                                       f'<b>Этажность:</b> {number_of_storeys}\n\n'
                                       f'<b>Цена:</b> {price_publication}\n\n'
                                       f'<b>Дата:</b> {date_publication}\n\n'
                                       f'<b>Ссылка (<code>{id_publication}</code>):</b>\n{link_to_publication}\n\n',
                             parse_mode="HTML")
        else:
            if (float(''.join(
                    check_digital if check_digital.isdigit() else '' for check_digital in price_publication).split()[
                          0]) / float(''.join(
                check_digital if check_digital.isdigit() else '' for check_digital in square_of_rooms).split()[
                                          0])) <= ratio_array[flag]:
                Bot.send_message(username, f'<b>Название:</b>\n{publication_title}\n\n'
                                           f'<b>Описание:</b>\n{description_publication}\n\n'
                                           f'<b>Общая площадь:</b> {square_of_rooms}\n\n'
                                           f'<b>Этаж:</b> {floor_of_room}\n\n'
                                           f'<b>Этажность:</b> {number_of_storeys}\n\n'
                                           f'<b>Цена:</b> {price_publication}\n\n'
                                           f'<b>Дата:</b> {date_publication}\n\n'
                                           f'<b>Ссылка (<code>{id_publication}</code>):</b>\n{link_to_publication}\n\n',
                                 parse_mode="HTML")

    def parser_function_for_new(number, flag):
        find = WebDriverWait(driver, 3).until(
            Except.visibility_of_element_located((By.XPATH,
                                                  f'//div[contains(@data-testid,"l-card")][{number}]/a'))
        )
        link_to_publication = find.get_attribute('href')

        print(double_links)

        if not(link_to_publication in set(double_links)):

            html_select_requests(link_to_publication)

            if not ratio_array:
                Bot.send_message(username, f'<b>Название:</b>\n{publication_title}\n\n'
                                           f'<b>Описание:</b>\n{description_publication}\n\n'
                                           f'<b>Общая площадь:</b> {square_of_rooms}\n\n'
                                           f'<b>Этаж:</b> {floor_of_room}\n\n'
                                           f'<b>Этажность:</b> {number_of_storeys}\n\n'
                                           f'<b>Цена:</b> {price_publication}\n\n'
                                           f'<b>Дата:</b> {date_publication}\n\n'
                                           f'<b>Ссылка (<code>{id_publication}</code>):</b>\n{link_to_publication}\n\n',
                                 parse_mode="HTML")
            else:
                if (float(''.join(
                        check_digital if check_digital.isdigit() else '' for check_digital in price_publication).split()[
                              0]) / float(''.join(
                    check_digital if check_digital.isdigit() else '' for check_digital in square_of_rooms).split()[
                                              0])) <= ratio_array[flag]:
                    Bot.send_message(username, f'<b>Название:</b>\n{publication_title}\n\n'
                                               f'<b>Описание:</b>\n{description_publication}\n\n'
                                               f'<b>Общая площадь:</b> {square_of_rooms}\n\n'
                                               f'<b>Этаж:</b> {floor_of_room}\n\n'
                                               f'<b>Этажность:</b> {number_of_storeys}\n\n'
                                               f'<b>Цена:</b> {price_publication}\n\n'
                                               f'<b>Дата:</b> {date_publication}\n\n'
                                               f'<b>Ссылка (<code>{id_publication}</code>):</b>\n{link_to_publication}\n\n',
                                     parse_mode="HTML")

    def getting_new_publications():
        time.sleep(2)
        os.system("clear")

        print("Парсер новых объявлений успешно запущен...")

        array_copy2 = driver.window_handles

        print(len(array_copy2))

        while True:

            index = 1

            while True:
                driver.refresh()

                element_wait = driver.find_element(by=By.XPATH,
                                                   value='//*[@id="mainContent"]/div[2]/form/div[3]/div[4]/div/div/div[1]/div/span')
                driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                time.sleep(1)

                parser_function_for_new(2, index - 1)

                if len(array_copy2) > index:
                    driver.switch_to.window(array_copy2[index])
                    index += 1
                else:
                    break

            driver.switch_to.window(array_copy2[0])
            time.sleep(6)

    def getting_old_publications():
        time.sleep(2)
        os.system("clear")

        print("Парсер старых объявлений успешно запущен...")

        array_for_parser = driver.window_handles

        index = 1

        while array_for_parser:

            number_publication = 2

            page = 2

            element_wait = driver.find_element(by=By.XPATH,
                                               value='//*[@id="mainContent"]/div[2]/form/div[3]/div[4]/div/div/div[1]/div/span')
            driver.execute_script("arguments[0].scrollIntoView();", element_wait)

            response = requests.get(f"{driver.current_url}")
            html_parser = BS(response.content, 'html.parser')
            find_count_publications = html_parser.select(".css-7ddzao > span:nth-child(1)")[0].text
            count_publications = int(''.join(
                check_digital if check_digital.isdigit() else '' for check_digital in find_count_publications).split()[
                                         0])

            while count_publications != 0:
                try:
                    parser_function(number_publication, index - 1)
                    element_wait = driver.find_element(by=By.XPATH,
                                                       value=f'//div[contains(@data-testid,"l-card")][{number_publication}]')
                    driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                    time.sleep(1)
                    count_publications -= 1
                    number_publication += 1

                except:
                    next_page = WebDriverWait(driver, 10).until(
                        Except.visibility_of_element_located((By.XPATH,
                                                              f'//*[@id="mainContent"]/div[2]/form/div[5]/div/section[1]/div/ul/li[{page}]'))
                    )
                    next_page.click()

                    time.sleep(1)

                    element_wait = driver.find_element(by=By.XPATH,
                                                       value='//*[@id="mainContent"]/div[2]/form/div[3]/div[4]/div/div/div[1]/div/span')
                    driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                    number_publication = 2

                    time.sleep(1)

                    page += 1
                    parser_function(number_publication, index - 1)
                    element_wait = driver.find_element(by=By.XPATH,
                                                       value=f'//div[contains(@data-testid,"l-card")][{number_publication}]')
                    driver.execute_script("arguments[0].scrollIntoView();", element_wait)

                    time.sleep(1)

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            first_page = WebDriverWait(driver, 10).until(
                Except.visibility_of_element_located((By.XPATH,
                                                      f'//*[@id="mainContent"]/div[2]/form/div[5]/div/section[1]/div/ul/li[1]'))
            )
            first_page.click()

            if len(array_for_parser) > index:
                driver.switch_to.window(array_for_parser[index])
                index += 1
            else:
                break

        print("Все старые объявления успешно спарсены! Перехожу в мониторинг новых объявлений...")
        driver.switch_to.window(array_for_parser[0])
        getting_new_publications()

    # Copy main array links
    array_copy = array_to_links.copy()

    number_link = 1

    while array_copy:
        os.system("clear")

        if "kvartiry" in array_copy[0]:
            parameters_for_first_links(number_link)
            parameters_execute(True)
            options_filters_return(True)
            array_copy.remove(array_copy[0])

        elif "kommercheskie-pomeshcheniya" in array_copy[0]:
            parameters_for_second_links(number_link)
            parameters_execute(False)
            options_filters_return(False)
            array_copy.remove(array_copy[0])

        number_link += 1

        if number_link <= len(array_to_links.copy()):
            driver.switch_to.window(driver.window_handles[number_link - 1])
        else:
            break

    driver.switch_to.window(driver.window_handles[0])
    getting_old_publications()


# Open All Links
def execute_links():
    global driver

    print("\nПрогрузка всех страниц, это может занять пару минут...")

    array_copy = array_to_links.copy()

    driver.get(f"{array_copy[0]}")
    array_copy.remove(array_copy[0])

    while array_copy:
        driver.switch_to.new_window(WindowTypes.TAB)
        driver.get(f"{array_copy[0]}")
        array_copy.remove(array_copy[0])

    driver.switch_to.window(driver.window_handles[0])

    os.system("clear")
    getting_publications()


# Get Links To Publications
def getting_links():
    global array_to_links

    count_links = int(input("Количество ссылок: "))

    print("\nВведите ссылки через Enter: ")
    array_to_links = [input(f"{index + 1}. ") for index in range(count_links)]

    execute_links()


if __name__ == "__main__":
    import threading

    main_thread = threading.Thread(target=getting_links)
    main_thread.start()
    Bot.polling(none_stop=True)
