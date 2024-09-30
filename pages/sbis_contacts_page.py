import os
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class SbisContactsPage:
    URL = "https://sbis.ru/"
    download_dir = os.path.join(os.getcwd(), "downloads")

    def __init__(self, driver):
        self.driver = driver

    def get_site(self):
        """Открывает сайт СБИС."""
        self.driver.get(self.URL)

    def go_to_contacts(self):
        """Переходит на страницу контактов."""
        contacts_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.sbisru-Footer__link[href='/contacts']"))
        )
        contacts_link.click()

    def click_tensor_banner(self):
        """Кликает по баннеру Tensor."""
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element((By.CSS_SELECTOR, "перекрывающий_элемент"))
        )
        tensor_banner = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.sbisru-Contacts__logo-tensor[href='https://tensor.ru/']"))
        )
        tensor_banner.click()

    def check_region(self, region_name):
        """Проверяет, что выбранный регион соответствует ожидаемому."""
        region_text = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sbis_ru-Region-Chooser__text"))
        )
        return region_name in region_text.text

    def change_region(self, new_region_name):
        """Изменяет выбранный регион."""
        region_dropdown = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sbis_ru-Region-Chooser__text"))
        )
        region_dropdown.click()

        new_region_xpath = f"//li[contains(@class, 'sbis_ru-Region-Panel__item')]//span[@title='{new_region_name}']"
        new_region = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, new_region_xpath))
        )
        
        assert new_region.is_displayed(), f"New region {new_region_name} is not displayed"
        new_region.click()

        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "sbis_ru-Region-Chooser__text"), new_region_name)
        )

    def go_to_downloads(self):
        """Переходит на страницу загрузок."""
        downloads_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.sbisru-Footer__link[href='/download']"))
        )
        downloads_link.click()

    def choose_downloads_plugin(self):
        """Выбирает загрузку плагина СБИС."""
        choose_plugin_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'СБИС Плагин')]"))
        )
        choose_plugin_button.click()

    def choose_downloads_windows(self):
        """Выбирает версию для Windows."""
        choose_windows_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Windows')]"))
        )
        choose_windows_button.click()

    def get_file_size(self):
        """Получает размер файла для загрузки."""
        download_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sbis_ru-DownloadNew-loadLink__link"))
        )
        
        for element in download_elements:
            link = element.get_attribute("href")
            if "exe" in link:
                download_text = element.text
                match = re.search(r'(\d+(\.\d+)?)\s*МБ', download_text)
                if match:
                    file_size = match.group(1)  # Извлекаем размер файла
                    return float(file_size)
        
        raise ValueError("Не удалось найти ссылку на файл с расширением 'exe' или размер файла")

    def download_file(self):
        """Скачивает файл."""
        download_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sbis_ru-DownloadNew-loadLink__link"))
        )
        
        for element in download_elements:
            link = element.get_attribute("href")
            if "exe" in link:
                element.click()
                return self.wait_for_download()
        
        raise ValueError("Не удалось найти ссылку на файл с расширением 'exe'")

    def wait_for_download(self, timeout=30):
        """Ожидает завершения загрузки файла."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            files = os.listdir(self.download_dir)
            if files:
                for file_name in files:
                    if not file_name.endswith('.crdownload'):  # Проверяем, что файл загрузился полностью
                        return os.path.join(self.download_dir, file_name)
            time.sleep(1)
        raise TimeoutError("Загрузка файла не завершена в течение отведенного времени")