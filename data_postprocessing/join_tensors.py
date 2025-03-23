import os
import numpy as np
from tqdm import tqdm

def parse_coordinates(filename):
    """
    Извлекает координаты из имени файла, например: '453000_3974000.npy'.
    """
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    parts = name.split('_')
    #print('parts', parts)
    y, x = map(int, parts[-2:])
    return y, x

def stitch_arrays(input_folder, output_file):
    """
    Склеивает массивы из папки на основе их нумерации.
    """
    files = [f for f in os.listdir(input_folder) if f.endswith('.npy')]
    coordinates = {}

    for file in files:
        x, y = parse_coordinates(file)
        coordinates[(x, y)] = file

    if not coordinates:
        raise ValueError("В папке нет массивов для склейки")

    x_coords = sorted({x for x, y in coordinates.keys()})
    y_coords = sorted({y for x, y in coordinates.keys()})

    if len(x_coords) < 1 or len(y_coords) < 1:
        raise ValueError("Недостаточно координат для определения сетки")

    step_x = x_coords[1] - x_coords[0] if len(x_coords) > 1 else 0
    step_y = y_coords[1] - y_coords[0] if len(y_coords) > 1 else 0

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    num_x = ((max_x - min_x) // step_x) + 1 if step_x != 0 else 1
    num_y = ((max_y - min_y) // step_y) + 1 if step_y != 0 else 1

    first_array = np.load(os.path.join(input_folder, coordinates[(min_x, min_y)]))
    tile_shape = first_array.shape

    final_height = num_y * tile_shape[0]
    final_width = num_x * tile_shape[1]

    final_array = np.zeros((final_height, final_width, tile_shape[2]), dtype=first_array.dtype)
    default_array = np.zeros(tile_shape, dtype=first_array.dtype)

    for y in tqdm(range(num_y), desc="Склеивание строк"):
        for x in range(num_x):
            coord_x = min_x + x * step_x
            coord_y = min_y + y * step_y

            start_x = x * tile_shape[1]
            start_y = y * tile_shape[0]

            if (coord_x, coord_y) in coordinates:
                tile = np.load(os.path.join(input_folder, coordinates[(coord_x, coord_y)]))
            else:
                tile = default_array

            final_array[start_y:start_y + tile_shape[0],
                        start_x:start_x + tile_shape[1],
                        :] = tile
    joined_file = os.path.join(output_file, 'joined.npy')
    np.save(joined_file, final_array)
    print(f"Склеенный массив сохранен как '{joined_file}'")



if __name__ == "__main__":
    import config_postprocessing as cp
    input_folder = cp.path_tensors_to_join
    output_file = cp.path_joined_tensors
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    stitch_arrays(input_folder, output_file)
