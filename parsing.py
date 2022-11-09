import threading
import re
import requests
from bs4 import BeautifulSoup
import os


def get_html(url,bynary=False):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76"
        }
    try:
        result = requests.get(url,headers=headers)
        result.raise_for_status()
        return result.text if not bynary else result
    except(requests.RequestException,ValueError):
        print('Сетевая ошибка')
        return False


def create_folder(name_folder, set_exceptions=set()):
    if name_folder in set_exceptions:
        return
    folder_path = os.path.join('C:\images_for_Alex',name_folder)
    os.mkdir(folder_path)
    return folder_path


def save_image(path_dir, name_img, price, num, value):
    image = get_html(value['href'],bynary=True)
    price = price.split('\n')[1] if len(price.split('\n'))>1 else price
    name_img = name_img[:224-len(f'.({price})_{num}.jpg')].replace('/','!')
    path_image = os.path.join(path_dir,f"{name_img}.({price})_{num}.jpg")
    try:
        with open(path_image,'bw') as new_img:
            new_img.write(image.content)
    except FileNotFoundError:
        print(f'Ошибка в имени: {name_img}')
        save_error.append(True)


def save_description(path_folder,name_folder,name_image,price,description):
    path_description = os.path.join(path_folder,f"{name_folder}.txt")
    with open(path_description,'a') as data:
        data.write(f'{name_image}{description}{price}\n\n')

def parsing(url, start, stop, exceptions=set()):
    path_folder = 'C:\images_for_Alex\Финансовые и исторические документы'
    name_folder = 'Финансовые и исторические документы'
    num_source = ''
    for i in range(start,stop):
        url = re.sub('/\d+/\?',f'/{i}/?',url)
        html = get_html(url)
        if html:
            print(f'Скачивается страница {i}')
            source_count = 0
            source_save_counte = 0
            soup = BeautifulSoup(html, 'html.parser')
            list_row = soup.findAll('tr')
            for row in list_row:
                new_name_folder = row.find('div', class_="text-center display-4")
                if new_name_folder and new_name_folder.text != name_folder:
                    name_folder = new_name_folder.text
                    path_folder = create_folder(name_folder, exceptions)
                elif path_folder and row.find('td', class_="d-flex flex-column pb-0 col-5"):   
                    new_num_source = row.find('td', class_="num align-middle col-2 pb-0 display-4").text
                    print(new_num_source)
                    if new_num_source == num_source:
                        continue
                    num_source = new_num_source
                    save_error = []                                                         
                    source_count += 1
                    name_image = row.find('h3', class_="el text-left").text.strip()
                    #print(name_image)
                    description = row.find('div', class_='flex-fill').text
                    #print(description)
                    new_url = 'https://www.znak-auction.ru' + row.find('a', class_="etooltip")['href']
                    new_html = get_html(new_url)
                    if new_html:
                        new_soup = BeautifulSoup(new_html,'html.parser')
                        try:
                            price = new_soup.find('div', class_="row justify-content-between align-items-center").text.strip()
                        except AttributeError:
                            price = new_soup.find('div', class_="text-primary font-weight-bold text-right py-4").text.strip()
                            print(f'Цена в блоке except: {price}')
                        links = new_soup.findAll('a', class_="mz-thumb mx-1 p-1 border border-dark")
                        for num,link in enumerate(links,1):
                            th = threading.Thread(target=save_image, args=(path_folder,name_image,price,num,link))
                            th.start()
                        source_save_counte += 1 if not save_error else 0
                        if description:
                            save_description(path_folder,name_folder,name_image,price,description)
                    else: 
                        print(f'Не сохранен лот с именем: {name_image}')
            print(f'Лотов к скачиванию: {source_count}\nИтого скаченно: {source_save_counte}\n')        
           

if __name__ == "__main__":
    parsing("https://www.znak-auction.ru/online/126/0/1/?view=table&count=10", 38, 40)



           