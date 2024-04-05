import urllib.request 
import urllib.parse
import sys
import os
import re
from tqdm import tqdm

def read_file(file):
    with open(file, 'rb') as my_file:
        content = my_file.read()
        content = content.decode('utf-8')
    content = content.replace('\r\n', '\n')
    # with open(file, 'w', encoding='utf-8') as my_file:
    #     my_file.write(content)
    return content

def get_img(content, file_path, save_path='./img/'):
    p = r'!\[img\]\((http[s]?://.*\.(?:png|jpg|jpeg|svg|ico|gif|bmp|webp|gif))\)'

    img_list=re.findall(p, content)
    list_len = str(len(img_list))

    for img_url in img_list:
        print(img_url)
    print(list_len + 'items in total')

    save_path = file_path + save_path

    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print('create folder: ' + save_path)
        
    for each in tqdm(img_list):
        photo_name=each.split("/")[-3]+each.split("/")[-2]+each.split("/")[-1]
        encoded_url = urllib.parse.quote(each, safe=':/') 
        photo = urllib.request.urlopen(encoded_url)
        w = photo.read()
        f = open(save_path + photo_name, 'wb')
        f.write(w)
        f.close()
        content = content.replace(each, save_path + photo_name)
        
    with open(file, 'w', encoding='utf-8') as my_file:
        my_file.write(content)
    print('done.')

if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: python spider.py <file>")
        sys.exit()

    file = str(sys.argv[1])

    file_name = os.path.basename(file)
    file_path = os.path.dirname(file)
    # print('file_name: ' + file_name)
    # print('file_path: ' + file_path)

    content = read_file(file)
    get_img(content, file_path)
