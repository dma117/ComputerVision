import os
import cv2
import csv


# фунцкия для получения данных из файла "description.csv"
# возвращает массив трех элементов: индекс, цвет, путь до изображения
def get_imgs_data(input_dir):
    file_name = 'description.csv'
    imgs_data_dir = os.path.join(input_dir , file_name)
    imgs_data = []
    names = []
    with open(imgs_data_dir) as file_obj:
        heading = next(file_obj)
        reader_obj = csv.reader(file_obj)
        for row in list(reader_obj):
            name = row[2]
            name_idx = name.index('_')
            name = name[:name_idx]
            names.append(name)
            row[2] = os.path.join('./input/data' , row[2])
            imgs_data.append(row)
    return imgs_data, names

# функция считывает и возвращает количество изображений из файла "image_counter.txt"
def read_imgs_count(input_dir):
    file_name = 'image_counter.txt'
    count_imgs_dir = os.path.join(input_dir , file_name)
    with open(count_imgs_dir) as f:
        return int(f.read())

# функция для соединения r, g, b изображений в одно
def merge_channels(input_dir, output_dir):
    imgs_data, names = get_imgs_data(input_dir)
    count_imgs = read_imgs_count(input_dir)
    ext = '.jpg'
    imgs = []
    count = 3 * count_imgs # количество всех изображений в data
    for i in range(count):
        color_letter = imgs_data[i][1]
        path = imgs_data[i][2]
        img = cv2.imread(os.path.join(path))
        b,g,r = cv2.split(img)
        if color_letter == 'r':
            imgs.append(r)
        if color_letter == 'g':
            imgs.append(g)
        if color_letter == 'b':
            imgs.append(b)
        if len(imgs) == 3:
            merged = cv2.merge(imgs)
            cv2.imwrite(os.path.join(output_dir , f'{names[i]}{ext}' ),merged)
            imgs = []

input_dir = './input'
output_dir = './output'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

merge_channels(input_dir, output_dir)

