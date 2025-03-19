import os
import glob
import laspy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#======================================= Interpolation Profiles ====================
from scipy.interpolate import griddata

def interpolate_profile(x, y, z, x_start, y_start, x_end, y_end, num_points=100):
    # Генерация точек на прямой между (x_start, y_start) и (x_end, y_end)
    x_vals = np.linspace(x_start, x_end, num_points)
    y_vals = np.linspace(y_start, y_end, num_points)
    
    # Интерполяция с использованием griddata (метод 'linear' наиболее быстрый и точный)
    points = np.column_stack((x, y))  # Объединяем x и y в массив точек
    grid_points = np.column_stack((x_vals, y_vals))  # Точки на сетке для интерполяции
    
    # Интерполяция по сетке
    z_vals = griddata(points, z, grid_points, method='nearest')  # Можно заменить 'linear' на 'nearest', если требуется еще больше ускорить

    return x_vals, y_vals, z_vals


def calculate_profiles(x, y, z, num_points=100):
    # Находим граничные точки
    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)

    # Первая диагональ: [x_min, y_min; x_max, y_max]
    x1, y1, z1 = interpolate_profile(x, y, z, x_min, y_min, x_max, y_max, num_points)

    # Вторая диагональ: [x_min, y_max; x_max, y_min]
    x2, y2, z2 = interpolate_profile(x, y, z, x_min, y_max, x_max, y_min, num_points)

    # Горизонтальный профиль: [(x_max+x_min)/2, y_min; (x_max+x_min)/2, y_max]
    x_mid = (x_min + x_max) / 2
    x3, y3, z3 = interpolate_profile(x, y, z, x_mid, y_min, x_mid, y_max, num_points)

    # Вертикальный профиль: [x_min, (y_max+y_min)/2; x_max, (y_max+y_min)/2]
    y_mid = (y_min + y_max) / 2
    x4, y4, z4 = interpolate_profile(x, y, z, x_min, y_mid, x_max, y_mid, num_points)

    return (x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4)
#=======================================


def create_new_info_folder(base_dir="data_info"):
    """Создает новый каталог info_{i}, увеличивая индекс на 1, если каталоги уже существуют."""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    existing_folders = sorted(glob.glob(os.path.join(base_dir, "info_*")), key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else 0)
    
    if existing_folders:
        last_index = int(existing_folders[-1].split('_')[-1])
        new_index = last_index + 1
    else:
        new_index = 0
    
    new_folder = os.path.join(base_dir, f"info_{new_index}")
    os.makedirs(new_folder)
    return new_folder

def analyze_las_file(las_path):
    """Анализирует LAS-файл и возвращает статистику."""
    las = laspy.read(las_path)
    z_values = las.z
    num_points = len(z_values)
    mu_z = np.mean(z_values)
    sigma_z = np.std(z_values)
    max_z = np.max(z_values)
    min_z = np.min(z_values)
    
    return {
        "file_name": os.path.basename(las_path),
        "num_points": num_points,
        "mu_z": mu_z,
        "sigma_z": sigma_z,
        "max_z": max_z,
        "min_z": min_z,
        "dz_max": max_z-min_z
    }

def save_csv_profile(z_values, output_csv):
    # Check if z_values is iterable, if it's not, make it a list
    if isinstance(z_values, (list, np.ndarray)):
        df = pd.DataFrame({"z": z_values})
    else:
        # If z_values is a scalar, put it in a list or array
        df = pd.DataFrame({"z": [z_values]})
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)


def save_png_profile(z_values, output_png):
    # Ensure z_values is an iterable (list, numpy array, etc.)
    if isinstance(z_values, np.ndarray) and z_values.ndim == 1:
        plt.plot(range(len(z_values)), z_values, label="Elevation Profile", color='b')
        plt.xlabel('Index')
        plt.ylabel('Elevation (z)')
        plt.title('Elevation Profile')
        plt.legend()
        plt.savefig(output_png)
        plt.close()
    else:
        print("Error: z_values must be an iterable (like a numpy array or list).")

def generate_las_report(input_dir, save_csv=True, save_png=True):
    """Генерирует отчет о всех LAS-файлах в указанной директории."""
    output_folder = create_new_info_folder()
    report_file = os.path.join(output_folder, "report.txt")
    
    las_files = glob.glob(os.path.join(input_dir, "*.las"))
    report_data = []
    
    with open(report_file, "w") as f:
        f.write(f"Report generated on: {datetime.now()}\n")
        f.write(f"Source directory: {input_dir}\n")
        f.write(f"Processed files: {len(las_files)}\n\n")
        
        for las_path in las_files:
            stats = analyze_las_file(las_path)
            report_data.append(stats)
            
            f.write(f"File: {stats['file_name']}\n")
            f.write(f"  Points: {stats['num_points']}\n")
            f.write(f"  Mean Z: {stats['mu_z']:.2f}\n")
            f.write(f"  Std Z: {stats['sigma_z']:.2f}\n")
            f.write(f"  Max Z: {stats['max_z']:.2f}\n")
            f.write(f"  Min Z: {stats['min_z']:.2f}\n\n")

            las = laspy.read(las_path)
            x = las.x
            y = las.y
            z = las.z
            (x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4) = calculate_profiles(x, y, z, num_points=50)
            #print(z1)
            n=0
            for zi in [z1, z2, z3, z4]:
                n+=1
                if save_csv:
                    output_csv = os.path.join(output_folder, stats['file_name'].replace(".las", f"_{n}.csv"))
                    save_csv_profile(zi-np.min(zi), output_csv)
                if save_png:
                    output_png = os.path.join(output_folder, stats['file_name'].replace(".las", f"_{n}.png"))
                    save_png_profile(zi-np.min(zi), output_png)
    
    print(f"Report saved in {report_file}")
    return report_data

# Пример использования
if __name__ == "__main__":
    import config_preprocessing as cp
    import time
    input_directory = cp.path_las  # Указать путь к каталогу с LAS-файлами
    start = time.time()
    generate_las_report(input_directory, save_csv=True, save_png=True)
    end = time.time()
    print(round((end-start)/60,1))
