from typing import List, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import allure


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver: WebDriver = driver
        self.timeout: int = timeout
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)
        self.page_url: str = ''

    @allure.step('Найти элемент {value}')
    def find_element(self, by: Union[By, str], value: str) -> WebElement:
        return self.wait.until(
            expected_conditions.visibility_of_element_located((by, value)),
            message=f'Элемент {value} не найден'
        )

    @allure.step('Найти элементы {value}')
    def find_elements(self, by: Union[By, str], value: str) -> List[WebElement]:
        return self.wait.until(
            expected_conditions.visibility_of_all_elements_located((by, value)),
            message=f'Элементы {value} не найдены'
        )

    @allure.step('Получить текущий URL')
    def get_current_url(self) -> str:
        return self.driver.current_url


class LoginPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver, timeout=60)
        self.login = (By.ID, 'user-name')
        self.password = (By.ID, 'password')
        self.login_btn = (By.NAME, 'login-button')

    @allure.step('Ввести логин {login}')
    def input_login(self, login: str) -> None:
        self.find_element(*self.login).send_keys(login)

    @allure.step('Ввести пароль')
    def input_password(self, password: str) -> None:
        self.find_element(*self.password).send_keys(password)

    @allure.step('Нажать кнопку "LOGIN"')
    def login_button_click(self) -> None:
        self.find_element(*self.login_btn).click()

    @allure.step('Авторизоваться с логином {login} и паролем')
    def auth(self, login: str, password: str) -> None:
        self.input_login(login)
        self.input_password(password)
        self.login_button_click()


class InventoryPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver, timeout=60)
        self.page_url = 'https://www.saucedemo.com/inventory.html'
        self.item = (By.ID, 'item_0_title_link')
        self.add_jacket_to_cart_btn = (By.XPATH, '//*[@id="add-to-cart-sauce-labs-fleece-jacket"]')
        self.cart_btn = (By.XPATH, '//*[@id="shopping_cart_container"]/a')

    @allure.step('Проверить, что открыта страница "https://www.saucedemo.com/inventory.html"')
    def check_inventory_page_open(self) -> None:
        current_url = self.get_current_url()
        with allure.step('Проверить соответствие URL'):
            assert current_url == self.page_url, f"Ожидалось: {self.page_url}, Получено: {current_url}"

    @allure.step('Выбрать товар')
    def choose_item(self) -> None:
        self.find_element(*self.item).click()

    @allure.step('Добавить куртку в корзину')
    def add_jacket_to_cart_btn_click(self) -> None:
        self.find_element(*self.add_jacket_to_cart_btn).click()

    @allure.step('Открыть корзину')
    def cart_btn_click(self) -> None:
        self.find_element(*self.cart_btn).click()


class ItemPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver, timeout=60)
        self.add_to_cart_btn = (By.XPATH, '//*[@id="add-to-cart"]')
        self.back_to_products_btn = (By.XPATH, '//*[@id="back-to-products"]')

    @allure.step('Добавить товар в корзину')
    def add_to_cart_btn_click(self) -> None:
        self.find_element(*self.add_to_cart_btn).click()

    @allure.step('Вернуться к каталогу товаров')
    def back_to_products(self) -> None:
        self.find_element(*self.back_to_products_btn).click()


class CartPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver, timeout=60)
        self.item_list = (By.XPATH, "//*[@data-test='inventory-item']")

    @allure.step('Проверить количество продуктов в корзине')
    def check_count_products(self) -> None:
        items = self.find_elements(*self.item_list)
        count = len(items)
        with allure.step(f'Проверить количество элементов в корзине: {count}'):
            assert count >= 0, "Количество продуктов в корзине не может быть отрицательным"
