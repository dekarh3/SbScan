# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import sys
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_config
import openpyxl
from openpyxl import Workbook
from openpyxl.writer.write_only import WriteOnlyCell
import NormalizeFields as norm
import datetime
from datetime import datetime
import time
import string

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

B = {
    'menuIII'   : {'t': 'i', 's': 'compact-mode-btn'},
    'login'     : {'t': 'x', 's': '//INPUT[@class="controls-TextBox__field js-controls-TextBox__field  "]'},
    'password'  : {'t': 'x', 's': '//INPUT[@class="js-controls-TextBox__field controls-TextBox__field"]'},
    'a-button'  : {'t': 'x', 's': '//DIV[@class="loginForm__sendButton"]'},
    'menu>>'    : {'t': 'x', 's': '//SPAN[@class="navigation-LeftNavigation__event icon-View"]'
                                                    '[@data-go-event="onClickContragentIcon"]'},
    'menuCats'  : {'t': 'x', 's': '(//SPAN[@class="controls-DropdownList__text"])[2]'},
    'firms_x'   : {'t': 'x', 's': '//DIV[@class="Contragents-CommonRenders__InnCorner '
                                                    'Contragents-CommonRenders__Inn ws-ellipsis"]'},
    'firms_tr'  : {'t': 'x', 's': '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                                                    'js-controls-ListView__item"]'},
    'firms_trA' : {'t': 'x', 's': '//SPAN[@class="Contragents-CommonRenders__Name"]/../../../../..', 'a': 'data-id'},
    'data_id'   : {'t': 'x', 's': '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                                          'js-controls-ListView__item"][@data-id="'},
    'data_idA'  : {'t': 'x', 's': '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                    'js-controls-ListView__item"][@data-id="', 'a' : 'data-id'},
    'close'     : {'t': 'x', 's': '//DIV[@class="sbisname-window-title-close ws-button-classic ws-component '
                        'ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select"]'},
    'first'     : {'t': 'x', 's': '(//I[@sbisname="PagingBegin"])[1]'},
    'next'      : {'t': 'x', 's': '(//I[@sbisname="PagingNext"])[1]'},
    'prev'      : {'t': 'x', 's': '(//I[@sbisname="PagingPrev"])[1]'},
    'innA'      : {'t': 'x', 's': '//INPUT[@name="СтрокаИНН"]', 'a' : 'value'},
    'kppA'      : {'t': 'x', 's': '//INPUT[@name="СтрокаКПП"]', 'a': 'value'},
    'familyA'   : {'t': 'x', 's': '//INPUT[@name="СтрокаФамилия"]', 'a': 'value'},
    'nameA'     : {'t': 'x', 's': '//INPUT[@name="СтрокаИмя"]', 'a': 'value'},
    'surnameA'  : {'t': 'x', 's': '//INPUT[@name="СтрокаОтчество"]', 'a': 'value'},
'firm_full_nameA':{'t': 'x', 's': '//INPUT[@name="СтрокаПолноеНазвание"]', 'a': 'value'},
   'act_num1000': {'t': 'x', 's': '//DIV[@class="custom-select-option"][@value="1000"]'},
    'about'     : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="О компании"]'},
    'contacts'  : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="Контактные данные"]'},
    'rekv'      : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="Реквизиты"]'},
    'owners'    : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="Владельцы"]'},
    'summA'     : {'t': 'x', 's': '//SPAN[@class="Contragents-ContragentCardRatingBanner__title-Revenue  '
                                  'ctrg-subseparator"][text()="Выручка: "]/SPAN', 'a': 'text'},
    'costA'     : {'t': 'x', 's': '//SPAN[@class="Contragents-ContragentCardRatingBanner__title-Cost  '
                                  'ctrg-subseparator"][text()="Стоимость бизнеса: "]/SPAN', 'a': 'text'},
    'rat_sumA'  : {'t': 'x', 's': '//DIV[@class="ctrg-half-left"]//DIV[@class="Contragents-'
                                  'ContragentCardRatingBanner__positions"]/DIV/SPAN', 'a': 'title'},
    'rat_costA' : {'t': 'x', 's': '//DIV[@class="ctrg-half-right"]//DIV[@class="Contragents-'
                                  'ContragentCardRatingBanner__positions"]/DIV/SPAN', 'a': 'title'},
    'phonesA'   : {'t': 'x', 's': '//DIV[@sbisname="Таблица телефонов"]//DIV[@class="crm-phone-number crm-noicon '
                                  'ContragentCardPhones-Ellipsis"]', 'a': 'text'},
   'phones_typA': {'t': 'x', 's': '//DIV[@sbisname="Таблица телефонов"]//SPAN[@class="crm-phone-comment '
                                  'ContragentCardPhones-Ellipsis"]', 'a': 'text'},
         'warnA': {'t': 'x', 's': '//DIV[@sbisname="Реестры"]//DIV[@class="Contragents-ContragentCardIndicators'
                                  '__itemTitle "]//SPAN[@data-component="SBIS3.CONTROLS.Link"]', 'a': 'text'},
    'warn_dataA': {'t': 'x', 's': '//DIV[@sbisname="Реестры"]//DIV[@class="Contragents-ContragentCardIndicators_'
                                  '_listItemFooter"]//SPAN[@data-component="SBIS3.CONTROLS.Link"]', 'a': 'text'},
    'filialsA'  : {'t': 'x', 's': '//DIV[@sbisname="Таблица филиалов"]//DIV[@title]', 'a': 'text'},
    'ogrnA'     : {'t': 'x', 's': '//DIV[@sbisname="СтрокаОГРН"]//SPAN[@title]', 'a': 'text'},
    'okpoA'     : {'t': 'x', 's': '//DIV[@sbisname="СтрокаОКПО"]//SPAN[@title]', 'a': 'text'},
    'oktmoA'    : {'t': 'x', 's': '//DIV[@sbisname="СтрокаОКТМО"]//SPAN[@title]', 'a': 'text'},
    'reg_N_pfrA': {'t': 'x', 's': '//DIV[@sbisname="СтрокаРегНомерПФ"]//SPAN[@title]', 'a': 'text'},
    'reg_comp'  : {'t': 'x', 's': '//DIV[@class="ContragentCardRegistration-Data"]', 'a': 'text'},
    'reg_org'   : {'t': 'x', 's': '//DIV[@class="ContragentCardRegistrationGosOrg-Data"]', 'a': 'text'},
    'uchred'    : {'t': 'x', 's': '//DIV[@sbisname="brwУчредители"]//DIV[@class="ws-browser-cell-paddings"]'
                                  '/DIV[@title]', 'a': 'title'},
    'dochki'    : {'t': 'x', 's': '//DIV[@sbisname="brwДочерниеКомпании"]//DIV[@class="ws-browser-cell-paddings"]'
                                  '/DIV[@title]', 'a': 'title'},
    'cats-link' : {'t': 'x', 's': '//DIV[@sbisname="DropdownList_buttonHasMore"]/SPAN'},
    'cats'      : {'t': 'c', 's': 'controls-DropdownList__item-text'},
    'firms_c'   : {'t': 'c', 's': 'controls-DataGridView__tr'},
   'ch_surnameA': {'t': 'c', 's': 'Contragents-ContragentCard__Chief__surname', 'a': 'text'},
    'ch_nameA'  : {'t': 'c', 's': 'Contragents-ContragentCard__Chief__name', 'a': 'text'},
    'ch_titleA' : {'t': 'c', 's': 'Contragents-ContragentCard__Chief__title', 'a': 'text'},
    'gen_infoA' : {'t': 'c', 's': 'Contragents-ContragentCardGeneralInfo__State', 'a': 'text'},
    'act_link'  : {'t': 'c', 's': 'Contragents-ContragentCardGeneralInfo__ActivityTypes__title'},
  'act_by_count': {'t': 'c', 's': 'custom-select-text'},
    'acts'      : {'t': 'c', 's': 'ws-browser-table-row'},
    'act_numA'  : {'t': 'c', 's': 'Contragents-ContragentCardGeneralInfo__ActivityTypes__counter', 'a': 'text'},
    'emp_qtyA'  : {'t': 'c', 's': 'Contragents-ContragentCard__EmployeesQuantity__qty', 'a': 'text'},
    'addressA'  : {'t': 'c', 's': 'ContragentCardAddresses-blackLink', 'a': 'text'},
    'predstavA' : {'t': 'c', 's': 'user-info-cell', 'a': 'text'},

}

def wj(driver):  # Ждем, пока динамическая ява завершит все свои процессы
    WebDriverWait(driver, 50).until(lambda driver: driver.execute_script("return jQuery.active == 0"))
    """
    Еще варианты фреймворков/библиотек:
    "return Ajax.activeRequestCount == 0"
    "return dojo.io.XMLHTTPTransport.inFlight.length == 0"
    Ожидание пока все набранные буквы отработют явой:
    element = WebDriverWait(ff, 10).until(EC.presence_of_element_located((By.ID, "keywordSuggestion")))
    """
    return

def wa(driver): # Типа ловит анимацию. Здесь не ловит :(
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.ID, 'new - element') and
                                                   driver.find_elements(By.ID, 'spinner') == 0)
    return
"""
Прокрутка
driver.execute_script("return arguments[0].scrollIntoView();", elem) # Здесь не точно
driver.execute_script("window.scrollTo(0, 911)") # Здесь вообще не прокручивает

"""
def chk(d, t, s, f = '', a = '', data_id = ''): # Проверка наличия элемента, не вызывающая исключения
    wj(d)
    if data_id != '':
        data_id += '"]'
    try:
        if   t == 'i':
            d.find_element(By.ID, s)
        elif t == 'c':
            d.find_element(By.CLASS_NAME, s)
        elif t == 'x':
            d.find_element(By.XPATH, s)
    except NoSuchElementException:
        return False
    return True
"""
^^^
|||
Потому что EC.presence_of_element_located((By.XPATH, "xpath"))) возвращает объект, не нашел где там результат
try:
    assert EC.presence_of_element_located((By.XPATH, '//*[@id="Waldo"]')) is not True
except AssertionError, e:
    self.verificationErrors.append('presence_of_element_located returned True for Waldo')
"""

def p(d, t, f, s, a = '', data_id = ''):
    wj(d)
    if data_id != '':
        data_id += '"]'
    if t == 'i':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.ID, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.ID, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'vs':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.ID, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return [atr.text for atr in foo]
                else:
                    return [atr.get_attribute(a) for atr in foo]
        elif f == 'vv':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.ID, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo if atr.is_displayed()]
                    else:
                        return [atr.get_attribute(a) for atr in foo if atr.is_displayed()]
            else:
                if a == '':
                    return []
                else:
                    return ['']

        elif f == 'p':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.ID, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return foo.text
                    else:
                        return foo.get_attribute(a)
            else:
                if a == '':
                    return
                else:
                    return ''
        elif f == 'ps':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.ID, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo]
                    else:
                        return [atr.get_attribute(a) for atr in foo]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        else:
            return
    elif t == 'x':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, s+data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.XPATH, s+data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'vs':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.XPATH, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return [atr.text for atr in foo]
                else:
                    return [atr.get_attribute(a) for atr in foo]
        elif f == 'vv':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.XPATH, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo if atr.is_displayed()]
                    else:
                        return [atr.get_attribute(a) for atr in foo if atr.is_displayed()]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        elif f == 'p':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.XPATH, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return foo.text
                    else:
                        return foo.get_attribute(a)
            else:
                if a == '':
                    return
                else:
                    return ''
        elif f == 'ps':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.XPATH, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo]
                    else:
                        return [atr.get_attribute(a) for atr in foo]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        else:
            return
    elif t == 'c':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, s + data_id)))
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, B[s]+data_id)))
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'vs':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return [atr.text for atr in foo]
                else:
                    return [atr.get_attribute(a) for atr in foo]
        elif f == 'vv':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo if atr.is_displayed()]
                    else:
                        return [atr.get_attribute(a) for atr in foo if atr.is_displayed()]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        elif f == 'p':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.CLASS_NAME, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return foo.text
                    else:
                        return foo.get_attribute(a)
            else:
                if a == '':
                    return
                else:
                    return ''
        elif f == 'ps':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo]
                    else:
                        return [atr.get_attribute(a) for atr in foo]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        else:
            return

def authorize(driver, login, password, authorize_page=''):
    time.sleep(1)
    if authorize_page != '':
        driver.get(authorize_page)
    # Ввод логина
    log = p(d = driver, f = 'c', **B['login'])
    time.sleep(1)
    log.send_keys(login)
    # Ввод пароля
    passwd = p(d = driver, f = 'c', **B['password'])
    time.sleep(1)
    passwd.send_keys(password)
    # Отправка формы нажатием кнопки
    cl = p(d = driver, f = 'c', **B['a-button'])
    cl.click()
    return

def to_spisok(driver):
    g = 0
    while g < 1000:
        try:
            menu = p(d = driver, f = 'c', **B['menuIII']) # Три палочки
            wj(driver)
            company = p(d = driver, f = 'p', **B['menu>>'])  # >>
            wj(driver)
            menu.click()
            wj(driver)
            if not company.is_displayed():
                wj(driver)
                continue
            company.click()
            wj(driver)
            if chk(d = driver, **B['menuCats']):
                wj(driver)
                if p(d = driver, f = 'p', **B['menuCats']).is_displayed():
                    return
            continue
        except Exception as ee:
            print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Ошибка в to_spisok', ee)
            continue

def set_filter(driver, category = ''):
    g = 0
    while g < 1000:
        try:
            elem = p(d = driver, f = 'v', **B['menuCats']) # Открываем дроплист
            wj(driver)
            elem.click()
            wj(driver)
            cats = p(d = driver, f = 'vs', **B['cats'])  # Выбираем категорию
            wj(driver)
            for i, cat in enumerate(cats):
                wj(driver)
                if cat.text == category and cat.is_displayed():
                    wj(driver)
                    cat.click()
                    break
            wj(driver)
            if chk(d = driver, **B['menuCats']):
                wj(driver)
                if p(d = driver, f = 'p', **B['menuCats']).text == category:
                    wj(driver)
                    return
                wj(driver)
            continue
        except  Exception as ee:
            print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Ошибка в to_spisok', ee)
            continue


# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')
scanconfig = read_config(section='scan')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(1) # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

try:
    authorize(driver, **webconfig)  # Авторизация
    #driver.get(**fillconfig)  # Открытие страницы где надо заполнять
    wj(driver)
    to_spisok(driver)
    wj(driver)
    set_filter(driver, **scanconfig)
    wj(driver)

    g = 0
    height = driver.get_window_size()['height'] # Высота окна
    while g < 1000:
        firms = p(d = driver, f = 'vv', **B['firms_trA'])
        read_cursor.execute('SELECT data_id, inn, kpp FROM main WHERE data_id >-1;')
        rows = read_cursor.fetchall()
        for i, firm in enumerate(firms):
            pass_string = False
            wj(driver)
            for row in rows:
                if row[0] == int(firm):
                    pass_string = True
            if pass_string:
                continue
            firmu = p(d=driver, f='p', **B['data_id'], data_id=firm)
            if firmu.location['y'] < 105:
                wj(driver)
                f = p(d = driver, f = 'c', **B['prev'])
                wj(driver)
                time.sleep(2)
                f.click()
                wj(driver)
                print(datetime.strftime(datetime.now(), "%H:%M:%S"),'prev')
                time.sleep(2)
                break
            if firmu.location['y'] > (height - 79):
                f = p(d = driver, f = 'c', **B['next'])
                wj(driver)
                time.sleep(2)
                f.click()
                wj(driver)
                print(datetime.strftime(datetime.now(), "%H:%M:%S"),'next вверху')
                time.sleep(2)
                break
            wj(driver)
            if firmu.is_displayed():
                wj(driver)                                      # Если DOM изменилось доступ через data-id (он не меняется)
                firma = p(d = driver, f = 'c', **B['data_id'], data_id = firm)
    #            xc_dataid(driver,'data_id',str(firm.get_attribute('data-id')))
                wj(driver)
                data_id = firma.get_attribute('data-id')
                firma.click()
                wj(driver)
                time.sleep(4)
                inn = p(d = driver, f = 'p', **B['innA'])
                kpp = p(d = driver, f = 'p', **B['kppA'])
                firm_full_name = p(d = driver, f = 'p', **B['firm_full_nameA'])
                if firm_full_name == '':
                    firm_full_name = p(d = driver, f = 'p', **B['familyA']) + ' ' + p(d = driver, f = 'p', **B['nameA'])\
                                     + ' ' + p(d = driver, f = 'p', **B['surnameA'])
                gen_info = p(d = driver, f = 'p', **B['gen_infoA'])
                act_num = p(d = driver, f = 'p', **B['act_numA'])
                act_link = p(d = driver, f = 'c', **B['act_link']) # Страница видов деятельности
                wj(driver)
                act_link.click()
                wj(driver)
                time.sleep(4)
                act_by_count = p(d = driver, f = 'c', **B['act_by_count']) # Список по сколько на страницу
                wj(driver)
                act_by_count.click()
                act_num1000 = p(d = driver, f = 'c', **B['act_num1000']) # Выбираем по 1000 на страницу
                act_num1000.click()
                acts =  p(d = driver, f = 'ps', **B['acts'])
                act_list = ''
                for j, act in enumerate(acts):
                    wj(driver)
                    if act.is_displayed() and act.get_attribute('rowkey').find('.') > -1:
                        wj(driver)
                        act_list += act.get_attribute('rowkey') + ' '
                wj(driver)
                act_link.click()
                wj(driver)
                time.sleep(4)
                ch_title = p(d = driver, f = 'p', **B['ch_titleA'])
                ch_name = p(d = driver, f = 'p', **B['ch_nameA'])
                ch_surname = p(d = driver, f = 'p', **B['ch_surnameA'])
                if ch_name == '' and ch_surname == '':
                    ch_fio = gen_info
                    ch_title = 'Индивидуальный предприниматель'
                else:
                    ch_fio = ch_surname + ' ' + ch_name
                summ = p(d = driver, f = 'p', **B['summA'])
                cost = p(d = driver, f = 'p', **B['costA'])
                s_rats = p(d = driver, f = 'ps', **B['rat_sumA'])
                c_rats = p(d = driver, f = 'ps', **B['rat_costA'])
                while len(s_rats) < 2:
                    s_rats.append('')
                while len(c_rats) < 2:
                    c_rats.append('')
                havnt_in_about = []  # Что не нашли на странице "О компании"
                ph = p(d = driver, f = 'ps', **B['phonesA'])
                if ph[0] == '':
                    havnt_in_about.append('phones')
                ph_t = p(d = driver, f = 'ps', **B['phones_typA'])
                while len(ph) < 5:
                    ph.append(None)
                ph_n = []
                for j, tel in enumerate(ph):
                    tel = str(tel).strip()
                    if tel == '' or tel == None:
                        ph_n.append(None)
                    else:
                        tel = ''.join([char for char in tel if char in string.digits])
                        if len(tel) == 11:
                            if tel[0] in ['8', '9']:
                                ph_n.append(int('7' + tel[1:]))
                        elif len(tel) == 10:
                            ph_n.append(int('7' + tel))
                        else:
                            ph_n.append(None)
                while len(ph_t) < 5:
                    ph_t.append(None)
                warns = p(d = driver, f = 'ps', **B['warnA'])
                if warns[0] == '':
                    havnt_in_about.append('warnings')
                warn_datas = p(d = driver, f = 'ps', **B['warn_dataA'])
                warn = ''
                for j, w in enumerate(warns):
                    if j < len(warn_datas):
                        if warn_datas[j] != '':
                            warn += w + ' (' + warn_datas[j] + ') '
                        else:
                            warn += w + ' '
                    else:
                        warn += w + ' '
                emp_qty = p(d = driver, f = 'p', **B['emp_qtyA'])
                address = p(d = driver, f = 'p', **B['addressA'])
                region = address.split(',')[0]
                if address == '':
                    havnt_in_about.append('address')
                predstavs = p(d = driver, f = 'ps', **B['predstavA'])
                if predstavs[0] == '':
                    havnt_in_about.append('predstavs')
                predstav = ''
                for w in predstavs:
                    predstav += w.replace('\n',' - ') + ' '
                filials = p(d = driver, f = 'ps', **B['filialsA'])
                fils = ''
                if filials[0] != '':
                    for j, w in enumerate(filials):
                        if j % 2 == 0:
                            fils += w
                        else:
                            fils += ' (' + w + ') '
                else:
                    havnt_in_about.append('filials')

                if chk(d = driver, **B['contacts']):
                    contacts_page = p(d = driver, f = 'c', **B['contacts'])
                    wj(driver)
                    contacts_page.click()
                    for havnt in havnt_in_about:
                        if havnt == 'phones':
                            ph = p(d=driver, f='ps', **B['phonesA'])
                            ph_t = p(d=driver, f='ps', **B['phones_typA'])
                            while len(ph) < 5:
                                ph.append(None)
                            ph_n = []
                            for j, tel in enumerate(ph):
                                tel = str(tel).strip()
                                if tel == '' or tel == None:
                                    ph_n.append(None)
                                else:
                                    tel = ''.join([char for char in tel if char in string.digits])
                                    if len(tel) == 11:
                                        if tel[0] in ['8', '9']:
                                            ph_n.append(int('7' + tel[1:]))
                                    elif len(tel) == 10:
                                        ph_n.append(int('7' + tel))
                                    else:
                                        ph_n.append(None)
                            while len(ph_t) < 5:
                                ph_t.append(None)
                        elif havnt == 'warnings':
                            warns = p(d=driver, f='ps', **B['warnA'])
                            warn_datas = p(d=driver, f='ps', **B['warn_dataA'])
                            warn = ''
                            for j, w in enumerate(warns):
                                if j < len(warn_datas):
                                    if warn_datas[j] != '':
                                        warn += w + ' (' + warn_datas[j] + ') '
                                    else:
                                        warn += w + ' '
                                else:
                                    warn += w + ' '
                        elif havnt == 'address':
                            address = p(d=driver, f='p', **B['addressA'])
                            region = address.split(',')[0]
                        elif havnt == 'predstavs':
                            predstavs = p(d=driver, f='ps', **B['predstavA'])
                            predstav = ''
                            for w in predstavs:
                                predstav += w.replace('\n', ' - ') + ' '
                        elif havnt == 'filials':
                            filials = p(d=driver, f='ps', **B['filialsA'])
                            if filials[0] != '':
                                for j, w in enumerate(filials):
                                    if j % 2 == 0:
                                        fils += w
                                    else:
                                        fils += ' (' + w + ') '

                if chk(d = driver, **B['rekv']):
                    rekv_page = p(d = driver, f = 'c', **B['rekv'])
                    wj(driver)
                    rekv_page.click()
                ogrn = p(d=driver, f='p', **B['ogrnA'])
                okpo = p(d=driver, f='p', **B['okpoA'])
                oktmo = p(d=driver, f='p', **B['oktmoA'])
                reg_N_pfr = p(d=driver, f='p', **B['reg_N_pfrA'])
                reg_comp =  p(d=driver, f='p', **B['reg_comp']).replace('\n',' ')
                reg_gos =  p(d=driver, f='p', **B['reg_org']).replace('\n',' ')

                if chk(d = driver, **B['owners']):
                    own_page = p(d = driver, f = 'c', **B['owners'])
                    wj(driver)
                    own_page.click()
                u = []
                uchreds = p(d=driver, f='ps', **B['uchred'])
                for j in range(int(len(uchreds)/3)):
                    u.append('(' + uchreds[j*3 + 2] + '% / ' + uchreds[j*3 + 1] + ' руб.) '+ uchreds[j*3])
                while len(u) < 5:
                    u.append(None)
                d = []
                dochki = p(d=driver, f='ps', **B['dochki'])
                for j in range(int(len(dochki)/2)):
                    d.append('(ИНН ' + dochki[j*2 + 1] + ') '+ dochki[j*2])
                while len(d) < 5:
                    d.append(None)

                sql = 'INSERT INTO main(data_id, inn, kpp, firm_full_name, gen_info, act_num, act_list, ch_title, ' \
                      'ch_fio, summ, cost, sum_rat1, sum_rat2, cost_rat1, cost_rat2, t_phone_1, phone_1, t_phone_2,' \
                      ' phone_2, t_phone_3, phone_3, t_phone_4, phone_4, t_phone_5, phone_5, warn, emp_qty, address,' \
                      ' region, predstav, fils, ogrn, okpo, oktmo, reg_N_pfr, reg_comp, reg_gos, u1, u2, u3, u4, u5,' \
                      'd1, d2, d3, d4, d5) ' \
                      'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' \
                      ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                write_cursor.execute(sql, (data_id, inn, kpp, firm_full_name, gen_info, act_num, act_list, ch_title,
                                           ch_fio, summ, cost, s_rats[0], s_rats[1], c_rats[0], c_rats[1], ph_t[0],
                                           ph_n[0], ph_t[1], ph_n[1], ph_t[2], ph_n[2], ph_t[3], ph_n[3], ph_t[4], ph_n[4],
                                           warn, emp_qty, address, region, predstav, fils, ogrn, okpo, oktmo, reg_N_pfr,
                                           reg_comp, reg_gos, u[0], u[1], u[2], u[3], u[4], d[0], d[1], d[2], d[3], d[4]))
                dbconn.commit()
                read_cursor.execute('SELECT count(*) FROM main WHERE data_id >-1;')
                rows = read_cursor.fetchall()
                if int(rows[0][0]) % 100 == 0:
                    print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Спарсено', int(rows[0][0]))
                wj(driver)
                close = p(d = driver, f = 'c', **B['close'])
                wj(driver)
                close.click()
                wj(driver)
                time.sleep(4)
        if i == len(firms)-1:
            f = p(d=driver, f='c', **B['next'])
            wj(driver)
            time.sleep(2)
            f.click()
            wj(driver)
            print(datetime.strftime(datetime.now(), "%H:%M:%S"),'next внизу')
            time.sleep(2)

    dbconn.close()
    driver.close()

except Exception as ee:
    print(datetime.strftime(datetime.now(), "%H:%M:%S"),'Ошибка: ', ee, '\n перезагружаю')
    dbconn.close()
    driver.close()
    driver = webdriver.Chrome()  # Инициализация драйвера
    driver.implicitly_wait(1)  # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
    dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
    read_cursor = dbconn.cursor()
    write_cursor = dbconn.cursor()



