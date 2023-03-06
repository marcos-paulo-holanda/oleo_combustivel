import requests, os
class Pdf:
    """Classe para baixar e salvar localmente o arquivo pdf"""
    def __init__(self, link, file_name):
        self.link = link
        self.file_name = file_name

    def baixa_pdf(self):
        # Baixa arquivo pdf das tabelas converte para csv
        response = requests.get(self.link)
        pdf = open(self.file_name + ".pdf", 'wb')
        pdf.write(response.content)
        pdf.close()
