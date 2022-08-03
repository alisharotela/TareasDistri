import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

import time
# usamos la libreria de expresiones regulares para sacar el numero del texto
import re

# Tema 1.1
def obtener_apariciones():
    page = False
    url="https://www.tiobe.com/tiobe-index/"

    while True:
        page = requests.get(url, timeout=(2,2))
        if page.ok:
            break
        else:
            time.sleep(1)
            print('x', end="")

    #print (page.content)
    soup = BeautifulSoup(page.content, 'html.parser')

    #para que imprima el contenido de la pagina con tabulador y espacios
    #print(soup.prettify())

    table = soup.find(id='top20')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    lenguajes = [tr.find_all('td')[4].text for tr in trs]

    # print("Lenguages obtenidos", lenguajes)
    print('Obteniendo datos: ')
    topic_urls = [(lang,'https://github.com/topics/'+lang)for lang in lenguajes]
    apariciones = []
    for lenguaje, url in topic_urls:
        if lenguaje=='C++':
            url = 'https://github.com/topics/Cpp'
        if lenguaje=='C#':
            url = 'https://github.com/topics/Csharp'
        if lenguaje == 'Delphi/Object Pascal':
            url = 'https://github.com/topics/Delphi'
        if lenguaje == 'Classic Visual Basic':
            url = 'https://github.com/topics/VisualBasic'

        page = False
        while True:
            page = requests.get(url)
            if page.ok:
                print('.', end=" ", flush=True)
                break
            else:
                time.sleep(1)
                print('x', end=" ", flush=True)

        soup = BeautifulSoup(page.content, 'html.parser')
        h3 = soup.find('h2', class_='h3')
        # "Here are 44,090 public repositories matching this topic..."
        # "Here are 44090 public repositories matching this topic..."
        nro = re.findall('\d+',h3.text.replace(',',''))
        # agregar el lenguaje y el numero de apariciones 
        apariciones.append((lenguaje,int(nro[0])))

    #print(apariciones)

    return apariciones 

# Tema 1.2
def guardar_archivo(datos):
    # datos = [(lang, nro), (lang, nro), (lang, nro)] => ["lang,nro\n","lang,nro\n"]
    lista_cadena = [key+","+str(value)+"\n" for key, value in datos]
    archivo = open("Resultados.txt", "w")
    archivo.writelines(lista_cadena)
    archivo.close()
    return True

# Tema 1.3
def obtener_valores():
    archivo = open("Resultados.txt", "r")
    valores = []
    while(linea := archivo.readline()):
        lang = linea.split(",")[0]
        nro = int(linea.split(",")[1].split('\n')[0])
        valores.append((lang,nro))
    return valores

def gen_rating(valores):
    # valores = [(lang, nro), (lang, nro), (lang, nro)]
    # valores = [nro,nro,nro]
    v_min = min([nro for lang, nro in valores])
    v_max = max([nro for lang, nro in valores])
    return [(lang, ((v_max-nro)/(v_max-v_min))*100) for lang, nro in valores]

# Tema 1.4
def imprimir_rating():
    valores = obtener_valores()
    # valores = [(python, nro), (lang, nro), (lang, nro)]
    rating = gen_rating(valores)
    # rating = [(python, rating), (lang, rating), (lang, rating)]
    
    # lista = [(lang, nro, rating[i][1]) for i, (lang, nro) in enumerate(valores)]
    lista = [] 
    for i, (lenguaje, nro) in enumerate(valores):
        puntuacion = rating[i][1]
        lista.append((lenguaje, nro, puntuacion))
    
    lista_ordenada = sorted(lista, key=lambda x: x[2], reverse=True)
    print("\nLenguaje - Rating - Nro de apariciones")
    for (lenguaje, nro, puntuacion) in lista_ordenada:
        print(lenguaje, " - ", round(puntuacion, 2), " - ", nro)

# Tema 1.5
def imprimir_grafico():
    valores = obtener_valores()[:10]
    # valores = [(lang, nro), (lang, nro), (lang, nro)]
    valores = sorted(valores, key=lambda x: x[1], reverse=True)
    
    fig, ax = plt.subplots()

    lenguajes = [lang for lang, nro in valores]
    y_pos = list(range(len(lenguajes))) # [0,1,2,3,4,5,6,7,8,9]
    x_pos = [v[1] for v in valores]
    error = [0 for v in valores]

    ax.bar(y_pos, x_pos, xerr=error, align='center')
    ax.set_xticks(y_pos, labels=lenguajes, rotation=90)
    ax.set_title('Numero de apariciones de lenguajes de programacion(python)')
    plt.subplots_adjust(bottom=0.35)
    plt.show()

def main():
    apariciones = obtener_apariciones()
    guardar_archivo(apariciones)
    #tema 1.3 tema 1.4
    imprimir_rating()
    imprimir_grafico()


if __name__ == "__main__":
    main()
