from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def _wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout)

    def _find(self, locator):
        return self.driver.find_element(*locator)

    def _scroll_into_view(self, elem):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        except Exception:
            pass

    def _hide_common_ads(self):
        
        try:
            self.driver.execute_script(
                "Array.from(document.querySelectorAll('iframe')).forEach(i=>{ if(i.src && i.src.includes('googlesyndication')) i.style.display='none'; }); var e = document.getElementById('fixedban'); if(e) e.style.display='none'; var f = document.querySelector('footer'); if(f) f.style.display='none';"
            )
        except Exception:
            pass

    def _safe_click(self, locator, timeout=10):
        wait = self._wait(timeout)
        self._hide_common_ads()
        elem = wait.until(EC.presence_of_element_located(locator))
        self._scroll_into_view(elem)
        try:
            wait.until(EC.element_to_be_clickable(locator))
            elem.click()
            return
        except Exception:
            pass

        try:
            self.driver.execute_script("arguments[0].click();", elem)
            return
        except Exception:
            pass

        try:
            ActionChains(self.driver).move_to_element(elem).click(elem).perform()
            return
        except Exception:
            raise
