from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os

from pages.base_page import BasePage

class CadastroEstudantePage(BasePage):
    URL = "https://demoqa.com/automation-practice-form"

    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "userEmail")
    GENDER_RADIO = (By.XPATH, "//label[contains(text(), '{}')]")
    MOBILE_INPUT = (By.ID, "userNumber")
    DATE_OF_BIRTH_INPUT = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    HOBBIES_CHECKBOX = (By.XPATH, "//label[contains(text(), '{}')]")
    UPLOAD_PICTURE_INPUT = (By.ID, "uploadPicture")
    CURRENT_ADDRESS_TEXTAREA = (By.ID, "currentAddress")
    STATE_DROPDOWN = (By.XPATH, "//div[text()='Select State']/following::input[1]")
    CITY_DROPDOWN = (By.XPATH, "//div[text()='Select City']/following::input[1]")
    SUBMIT_BUTTON = (By.ID, "submit")

    def __init__(self, driver):
        super().__init__(driver)
    
    def abrir_pagina(self):
        self.driver.get(self.URL)

    def preencher_nome(self, nome):
        self._find(self.FIRST_NAME_INPUT).send_keys(nome)

    def preencher_sobrenome(self, sobrenome):
        self._find(self.LAST_NAME_INPUT).send_keys(sobrenome)

    def preencher_email(self, email):
        self._find(self.EMAIL_INPUT).send_keys(email)

    def selecionar_genero(self, genero):
        genero = genero.strip().capitalize()

        xpath = f"//label[@class='custom-control-label' and normalize-space()='{genero}']"

        label = self._wait(5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        try:
            label.click()  # tentativa padrão
        except:
            # fallback
            ActionChains(self.driver).move_to_element(label).click().perform()

    def preencher_telefone(self, telefone):
        self._find(self.MOBILE_INPUT).send_keys(telefone)
 
    def preencher_data_nascimento(self, data_str):
        dia_str, mes_str, ano_str = data_str.split() 
        dia = int(dia_str)
        meses = {
            "january": "0", "february": "1", "march": "2", "april": "3",
            "may": "4", "june": "5", "july": "6", "august": "7",
            "september": "8", "october": "9", "november": "10", "december": "11"
        }

        mes_valor = meses[mes_str.lower()]
        self._safe_click(self.DATE_OF_BIRTH_INPUT)
        
        select_mes = Select(self._find((By.CSS_SELECTOR, ".react-datepicker__month-select")))
        select_mes.select_by_value(mes_valor)

        select_ano = Select(self._find((By.CSS_SELECTOR, ".react-datepicker__year-select")))
        select_ano.select_by_value(ano_str)

        dias = self.driver.find_elements(By.CSS_SELECTOR, ".react-datepicker__day")
        for d in dias:
            # Evita dias de outro mês (classe outside-month)
            if d.text == str(dia) and "outside-month" not in d.get_attribute("class"):
                d.click()
                break  

    def preencher_materias(self, materias):
        elem = self._find(self.SUBJECTS_INPUT)
        elem.clear()
        elem.send_keys(materias)
        elem.send_keys(Keys.ENTER)
        # espera para o autocomplete desaparecer
        try:
            self._wait(5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".subjects-auto-complete__option")
                )
            )
        except TimeoutException:
            pass

    def selecionar_hobbies(self, hobby):
        locator = (
            By.XPATH, 
            f"//label[contains(text(), '{hobby}')]/preceding-sibling::input[1]"
        )

        self._hide_common_ads()

        checkbox = self._wait(10).until(
            EC.presence_of_element_located(locator)
        )
        self._scroll_into_view(checkbox)

        try:
            self.driver.execute_script("arguments[0].click();", checkbox)
            return
        except:
            pass

        try:
            checkbox.click()
            return
        except:
            pass
        try:
            ActionChains(self.driver).move_to_element(checkbox).click().perform()
        except:
            raise

    def fazer_upload_foto(self, caminho_foto):
        file_path = os.path.abspath(caminho_foto)
        self._find(self.UPLOAD_PICTURE_INPUT).send_keys(file_path)

    def preencher_endereco(self, endereco):
        self._find(self.CURRENT_ADDRESS_TEXTAREA).send_keys(endereco)

    def selecionar_estado(self, estado):
        elem_locator = self.STATE_DROPDOWN
        self._safe_click(elem_locator)
        elem = self._find(elem_locator)
        elem.send_keys(estado)
        elem.send_keys(Keys.ENTER)
        try:
            self._wait(5).until(EC.element_to_be_clickable(self.CITY_DROPDOWN))
        except TimeoutException:
            pass

    def selecionar_cidade(self, cidade):
        elem = self._find(self.CITY_DROPDOWN)
        try:
            elem.click()
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", elem)
            except Exception:
                pass
        try:
            elem.send_keys(cidade)
            elem.send_keys(Keys.ENTER)
        except Exception:
            try:
                self.driver.execute_script(
                    "arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                    elem,
                    cidade,
                )
            except Exception:
                pass

    def clicar_botao_enviar(self):
        self._safe_click(self.SUBMIT_BUTTON)