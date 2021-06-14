import time
import json
import grequests
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'
}

def async_links(list):
    response = (grequests.get(url, headers=headers) for url in list)
    resp = grequests.map(response)
    return resp

def extraer_contenido(resp):
    soup = BeautifulSoup(resp.text, 'html.parser')

    titulo = soup.find_all("h1", "ui-pdp-title")[0].text.strip()
    precio = soup.find_all("span", "price-tag-fraction")[0].text
    precio = precio.replace(".", "")
    galeria = soup.find_all("figure", "ui-pdp-gallery__figure")
    try:
        descripcion = soup.find_all("p", "ui-pdp-description__content")[0]

        lista_descripcion = []
        for text in descripcion:
            if text.name == 'br':
                lista_descripcion.append('\n')
            else:
                lista_descripcion.append(text)

        separador = ''
        descripcion = separador.join(lista_descripcion)

    except:
        descripcion = ''


    imagenes = []

    for imagen in galeria:
        imagenUrl = imagen.find('img')
        if imagenUrl != None:
            imagenes.append(imagenUrl['src'])
        else:
            continue

    json_data = {
        'imagenes': imagenes,
        'titulo': titulo,
        'precio': precio,
        'descripcion': descripcion,
    }

    return json_data

def paginas(links):
    response = requests.get(links, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    lista = soup.find_all('div', 'ui-search-item__group ui-search-item__group--title')

    links = []
    for link in lista:
        links.append(link.find('a')['href'])

    return links

def save_file(responses):
    base_datos = []
    for link in responses:
        base_datos.append(extraer_contenido(link))

    with open('data.json', 'w') as f:
        json.dump(base_datos, f)

if __name__ == '__main__':
    start_time = time.time()
    links = paginas('https://listado.mercadolibre.com.ar/celulares#D[A:celulares]')
    responses = async_links(links)
    save_file(responses)
    print("--- %s seconds ---" % (time.time() - start_time))