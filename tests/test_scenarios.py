import os
import pytest
from selenium import webdriver
from pages.sbis_contacts_page import SbisContactsPage
from pages.tensor_page import TensorPage
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    prefs = {"download.default_directory": SbisContactsPage.download_dir}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_first_scenario(driver):
    sbis_contacts = SbisContactsPage(driver)
    tensor_page = TensorPage(driver)

    sbis_contacts.get_site()
    sbis_contacts.go_to_contacts()
    sbis_contacts.click_tensor_banner()

    driver.switch_to.window(driver.window_handles[1])
    assert "tensor.ru" in driver.current_url
    assert tensor_page.check_sila_v_lyudyah()

    tensor_page.go_to_more_info()
    assert tensor_page.check_about_url()
    assert tensor_page.check_timeline_images_size()

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def test_second_scenario(driver):
    sbis_contacts = SbisContactsPage(driver)
    sbis_contacts.get_site()
    sbis_contacts.go_to_contacts()

    assert sbis_contacts.check_region("Свердловская обл.")
    sbis_contacts.change_region("Камчатский край")
    assert sbis_contacts.check_region("Камчатский край")

def test_third_scenario(driver):
    sbis_contacts = SbisContactsPage(driver)
    sbis_contacts.get_site()
    sbis_contacts.go_to_downloads()
    sbis_contacts.choose_downloads_plugin()
    sbis_contacts.choose_downloads_windows()

    file_size = sbis_contacts.get_file_size()
    file_path = sbis_contacts.download_file()
    
    print(f"Файл скачан: {file_path}, размер файла: {file_size} МБ")
    assert os.path.exists(file_path), "Файл не был загружен."

    actual_size = os.path.getsize(file_path) / (1024 * 1024)  # Размер файла в МБ
    assert abs(actual_size - file_size) < 0.1, f"Размер файла не совпадает: ожидалось {file_size}, получено {actual_size}"
