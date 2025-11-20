from pages.cadastro_estudante_page import CadastroEstudantePage
from pages.tabela_page import TabelaPage

def test_cadastro_e_validacao(driver):
    cadastro = CadastroEstudantePage(driver)
    cadastro.abrir_pagina()

    payload = {
        "name": "João da Silva",
        "email": "joao@email.com",
        "gender": "Male",
        "phone": "9999999999",
        "date_of_birth": "10 October 1990",
        "favorite_subject": "Maths",
        "hobbies": ["Sports"],
        "file_upload": "src/files/imagem.png",
        "current_address": "Rua dos Testes, 123",
        "state": "NCR",
        "city": "Delhi",
    }

    first, rest = payload["name"].split(" ", 1)
    cadastro.preencher_nome(first)
    cadastro.preencher_sobrenome(rest)
    cadastro.preencher_email(payload["email"])
    cadastro.selecionar_genero(payload["gender"])
    cadastro.preencher_telefone(payload["phone"])
    cadastro.preencher_data_nascimento(payload["date_of_birth"])  
    cadastro.preencher_materias(payload["favorite_subject"])
    for hobby in payload["hobbies"]:
        cadastro.selecionar_hobbies(hobby)
    cadastro.fazer_upload_foto(payload["file_upload"])
    cadastro.preencher_endereco(payload["current_address"])
    cadastro.selecionar_estado(payload["state"])
    cadastro.selecionar_cidade(payload["city"])
    cadastro.clicar_botao_enviar()

    tabela = TabelaPage(driver)
    data = tabela.get_submission_table()

    def value_for_label(keywords):
        for label, val in data.items():
            low = label.lower()
            for k in keywords:
                if k.lower() in low:
                    return val
        return ""
        
    def formatar_data(data_str):
        dia, mes, ano = data_str.split()
        return f"{dia} {mes},{ano}"

    assert payload["name"] in value_for_label(["student name", "name"])
    assert payload["email"] == value_for_label(["student email", "email"])
    assert payload["gender"] == value_for_label(["gender"])
    assert payload["phone"] == value_for_label(["mobile", "phone"])
    dob_val = value_for_label(["date of birth", "date"])
    assert formatar_data(payload["date_of_birth"]) == dob_val
    assert payload["favorite_subject"] in value_for_label(["subject", "subjects"])
    for h in payload["hobbies"]:
        assert h in value_for_label(["hobbies", "hobby"])
    assert payload["current_address"] in value_for_label(["address", "current address"])
    sc = value_for_label(["state and city", "state"])
    assert payload["state"] in sc and payload["city"] in sc
