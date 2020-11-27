#Урок 5
#Задание 1
#1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
#Логин тестового ящика: study.ai_172@mail.ru
#Пароль тестового ящика: NextPassword172

from pprint import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')

#Регистрируемся на сайте
elem = driver.find_element_by_id('mailbox:login-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)
elem = driver.find_element_by_id('mailbox:password-input')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

driver.get('https://e.mail.ru/inbox')
mail_links = set()
while True:
    links_num = len(mail_links)
    time.sleep(5)
    actions = ActionChains(driver)
    mails = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')

    for elem in mails:
        mail_links.add(elem.get_attribute('href'))
    links_num_new = len(mail_links)
    if links_num == links_num_new:
        break
    actions.move_to_element(mails[-1])
    actions.perform()

mails_data = []
for link in mail_links:
    mail = {}
    driver.get(link)

    From = driver.find_element_by_class_name('letter-contact').text
    Date = driver.find_element_by_class_name('letter__date').text
    Subject = driver.find_element_by_class_name('thread__subject').text
    Text = driver.find_element_by_xpath("//div[@class='letter__body']").text

    mail['From'] = From
    mail['Date'] = Date
    mail['Subject'] = Subject
    mail['Text'] = Text

    mails_data.append(mail)

pprint(mails_data)
driver.quit()

