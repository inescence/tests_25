import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def driverChrome():
    pytest.driver = webdriver.Chrome('/Users/inescence/tests_25/chromedriver')
    pytest.driver.implicitly_wait(10)
    pytest.driver.maximize_window()
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield driverChrome
    pytest.driver.quit()


# логинимся и открываем страницу "мои питомцы"
@pytest.fixture()
def logging_in_and_go_to_my_pets():
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    pytest.driver.find_element(By.ID, 'email').send_keys('inescence@ya.ru')
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button['
                                                                                           'type="submit"]')))
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()


# получаем информацию о питомцах
@pytest.fixture()
def get_pets():
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.table.table-hover tbody tr')))
    pet_list = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    returned_list = []
    for pets in pet_list:
        pet = pets.text.split()
        if type(pet) != None:
            if len(pet) > 3:
                returned_list.append({'name': pet[0], 'breed': pet[1], 'age': pet[2]})
            else:
                returned_list.append({'name': 1, 'breed': 1, 'age': 1})

    yield returned_list


# получаем фотографии питомцев
@pytest.fixture()
def get_pets_photos():
    count = 0
    photo = pytest.driver.find_elements(By.XPATH, "//tbody/tr/th/img")
    for i in range(len(photo)):
        if 'data' in photo[i].get_dom_attribute('src'):
            count += 1

    yield count

