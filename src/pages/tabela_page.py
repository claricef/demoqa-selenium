from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class TabelaPage(BasePage):
    MODAL_TBODY = (By.CSS_SELECTOR, "body > div.fade.modal.show > div > div > div.modal-body > div > table > tbody")

    def __init__(self, driver):
        super().__init__(driver)

    def get_submission_table(self, timeout: int = 10) -> dict:
        try:
            tbody = self._wait(timeout).until(lambda d: d.find_element(*self.MODAL_TBODY))
        except TimeoutException:
            return {}

        result = {}
        for row in tbody.find_elements(By.TAG_NAME, "tr"):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                label = cells[0].text.strip()
                value = cells[1].text.strip()
                result[label] = value
        return result

