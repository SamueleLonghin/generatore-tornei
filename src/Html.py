def generate_html_table(header_general, headers, data):
    """
    Genera una tabella HTML con stile Bootstrap.

    Args:
    - header_general (str): Intestazione generale della tabella.
    - headers (list of str): Lista delle intestazioni di colonna.
    - data (list of list of str): I dati della tabella.

    Returns:
    - str: Una stringa contenente il codice HTML della tabella.
    """
    # Inizio della tabella + classe Bootstrap
    html = '<table class="table table-bordered table-hover">\n'

    # Intestazione generale
    html += f'<thead><tr><th colspan="{len(headers)}">{header_general}</th></tr></thead>\n'

    # Intestazioni specifiche
    html += '<thead class="thead-light"><tr>' + ''.join(f'<th>{header}</th>' for header in headers) + '</tr></thead>\n'

    # Righe di dati
    html += '<tbody>\n'


    for row in data:
        html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>\n'
    html += '</tbody>\n'

    # Fine della tabella
    html += '</table>'

    return html


# Esempio di utilizzo
header_general = 'Intestazione Generale'
headers = ['Nome', 'Età', 'Città']
data = [
    ['Alice', '24', 'New York'],
    ['Bob', '30', 'Chicago'],
    ['Charlie', '28', 'San Francisco']
]

html_table = generate_html_table(header_general, headers, data)
print(html_table)
