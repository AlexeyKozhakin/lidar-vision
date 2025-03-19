import os
import laspy
import numpy as np
from scipy.interpolate import griddata


def average_grid(las_data, N):
    xk = las_data.x
    yk = las_data.y
    zk = las_data.z

    x_min, x_max = np.min(xk), np.max(xk)
    y_min, y_max = np.min(yk), np.max(yk)
    R = np.sqrt((x_max - x_min) ** 2 + (y_max - y_min) ** 2) / N

    xn = np.linspace(x_min, x_max, N)
    yn = np.linspace(y_min, y_max, N)
    Xn, Yn = np.meshgrid(xn, yn)
    Zn = np.zeros(Xn.shape)

    for i in range(N):
        for j in range(N):
            mask = (np.sqrt((xk - Xn[i, j]) ** 2 + (yk - Yn[i, j]) ** 2) <= R)
            if np.any(mask):
                Zn[i, j] = np.mean(zk[mask])

    return Xn, Yn, Zn


def interpolate_data(las_data, grid_data):
    xk = las_data.x
    yk = las_data.y
    Xn, Yn, Zn = grid_data

    points = np.column_stack((Xn.ravel(), Yn.ravel()))
    values = Zn.ravel()
    fk = griddata(points, values, (xk, yk), method='linear')
    return fk


def filtered_dataset(las_data, fk):
    xk, yk, zk = las_data.x, las_data.y, las_data.z
    filtered_zk = zk - fk

    filtered_las = las_data #laspy.create(point_format=las_data.header.point_format)
    filtered_las.header = las_data.header
    filtered_las.x = xk
    filtered_las.y = yk
    filtered_las.z = filtered_zk


    return filtered_las


def process_las_filter_relief(input_directory, output_directory, N=10):
    for filename in os.listdir(input_directory):
        if filename.endswith(".las"):
            filepath = os.path.join(input_directory, filename)
            print(f"Обработка файла: {filepath}")
            las_data = laspy.read(filepath)

            grid_data = average_grid(las_data, N)
            fk = interpolate_data(las_data, grid_data)
            filtered_las = filtered_dataset(las_data, fk)

            output_path = os.path.join(output_directory, filename)
            filtered_las.write(output_path)
            print(f"Файл сохранен: {output_path}")

# Пример использования
if __name__ == "__main__":
    import config_preprocessing as cp
    import time
    input_directory = cp.path_las_with_rv  # Указать путь к каталогу с LAS-файлами
    output_directory = cp.path_las_no_rv  # Указать путь к каталогу с LAS-файлами
    # Создаем выходную директорию, если она не существует
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    start = time.time()
    process_las_filter_relief(input_directory, output_directory, N=10)
    end = time.time()
    print(round((end-start)/60,1))