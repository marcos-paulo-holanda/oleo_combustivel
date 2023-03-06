from IPython.display import HTML

class HtmlPage:
    '''Recebe uma dataframe, converte para html e formata o mesmo'''
    def html_file(self,df, file_name):
        # converte a df para html
        html_file = df.to_html()
        index_file = open(file_name + '.html', 'w')
        index_file.write(html_file)
        index_file.close()
        # Formata o arquivo com código css
        file = open(file_name + '.html', 'a')
        text = '<link rel="stylesheet" href="css/styles.css">'
        file.write(text)
        file.close()
