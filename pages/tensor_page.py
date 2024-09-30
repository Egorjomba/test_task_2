from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TensorPage:
    URL = "https://tensor.ru/"
    
    def __init__(self, driver):
        self.driver = driver

    def get_site(self):
        """Открывает сайт Tensor."""
        self.driver.get(self.URL)

    def check_sila_v_lyudyah(self):
        """Проверяет наличие блока 'Сила в людях'."""
        sila_block = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Сила в людях')]"))
        )
        return sila_block is not None

    def go_to_more_info(self):
        """Переходит на страницу 'Подробнее'."""
        more_info_buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.tensor_ru-link.tensor_ru-Index__link")
        
        for button in more_info_buttons:
            href = button.get_attribute("href")
            if "/about" in href:
                # Прокручиваем к элементу перед кликом
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                return

        raise Exception("Ссылка на страницу 'about' не найдена")

    def check_about_url(self):
        """Проверяет, что текущий URL содержит 'about'."""
        return "about" in self.driver.current_url

    def check_timeline_images_size(self):
        """Проверяет, что все изображения на странице имеют одинаковые размеры."""
        images = self.driver.find_elements(By.CSS_SELECTOR, "img.tensor_ru-About__block3-image")
        
        if not images:
            print("Изображения не найдены")
            return False  # Если изображения не найдены, возвращаем False

        # Получаем размер первого изображения для сравнения
        width = images[0].get_attribute('naturalWidth')
        height = images[0].get_attribute('naturalHeight')

        # Проверяем размеры всех изображений
        for img in images:
            if img.get_attribute('naturalWidth') != width or img.get_attribute('naturalHeight') != height:
                print("Разные размеры изображений")
                return False
        
        return True
