import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse as urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
import time
from time import sleep
import requests

email_payload = {
    'subject': 'Sharing your experience!',
    'message': """Hello, please do not report this message. If you are not interested, please answer 'Not interested'. We are writing a paper about how different methodologies affect the quality of the game development process to make the game development process better. I need to focus on visual novel developers. Can you please participate in the questionnaire and share your experience? You have to have at least one game made.

You can do this by participating in an interview in the zoom or by fulfilling the questionnaire in the google form. I guess the first option is easier because I can guide you through the whole process, explain things and probably make everything faster. It will take about 10-20 minutes.

The google form is here: https://forms.gle/VHtUsYxJ78NCaPby8. If you prefer to have an oral interview you can contact me in various ways:

Mail: d.vaskovskaya2@gmail.com
Telegram: @BananaAndBread
Instagram: _banana_and_bread_""",
}


def send_mail(developerName, developerId):
    print(f'sending to developer name {developerName}')
    sleep(1)
    driver.get(f'https://lemmasoft.renai.us/forums/memberlist.php?mode=email&u={developerId}')
    permitted =  'You are not permitted to send email to this user' not in driver.page_source
    if permitted:
        subject_input = driver.find_element_by_name("subject")
        message_input = driver.find_element_by_name("message")
        subject_input.send_keys(email_payload['subject'])
        message_input.send_keys(email_payload['message'])
        sleep(1)
        driver.find_element_by_name('submit').click()
    email_is_sent = "The email has been sent" in driver.page_source
    if email_is_sent or not permitted:
        f.write(f'{developerId}\n')
    "This user does not exist"
    invalid = 'You cannot send another email at this time' in driver.page_source or "FORM_INVALID" in driver.page_source
    print('invalid', invalid)
    print("email_is_sent", email_is_sent)
    return (not invalid and email_is_sent) or not permitted

index = 0
step = 60
developers = {}
f = open("receivers_usernames.txt", "r")
previous_user_ids = list(map(lambda x: x.rstrip(), f.readlines()))
f = open("receivers_usernames.txt", "a")
is_next = True
while len(list(developers.items())) < 500 and is_next:
    URL = f'https://lemmasoft.renai.us/forums/viewforum.php?f=11&start={index*step}'
    URL = f'https://lemmasoft.renai.us/forums/viewforum.php?f=11&start={index*step}'
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_='username')
    is_next = (soup.find_all(class_='pagination')[0].find_all('li')[-1].text == 'Next')
    print(is_next)
    for result in results:
        if result.get('href'):
            user_id = parse_qs(urlparse.urlparse(result['href']).query)['u'][0]
            user_name = result.text
            if user_id not in previous_user_ids:
                developers[user_name] = user_id
    index+=1


print(list(developers.items()))

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://lemmasoft.renai.us/forums/ucp.php?mode=login')
login_input = driver.find_element_by_name("username")
login_input.send_keys("BananaAndBread")
password_input = driver.find_element_by_name("password")
password_input.send_keys("P55L3LJND")
driver.find_element_by_name('login').click()


for developerName, developerId in list(developers.items()):
    f = open("receivers_usernames.txt", "a")
    invalid = True
    while invalid:
        try:
            invalid = not send_mail(developerName, developerId)
            print(invalid)
        except:
            invalid = True
    f.close()
