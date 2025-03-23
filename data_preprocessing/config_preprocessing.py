# config_preporocessing.py

# ===== training preprocessing =======
# ===== 1. INFO ======================
path_las = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim"
#path_las = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_clean"
#path_las = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_rv"
#path_las = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_rv"
#path_las = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points"
#path_las = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Sliema"
#path_las = r"C:\Users\alexe\Downloads\UM\work\Data\2012-20240803T112213Z-001\2018-20240913T181437Z-001\city_san_gwann\san_gwan_256_256_1"
#path_las = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org"
#path_las = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_large"
# ===== 2. FILTERING
# ===== 2.1 - Noises Filter
path_las_noise = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points"
path_las_clean = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_clean"

# Параметры фильтрации
filter_params = {
    'global_filter': {
        'z_sigma_threshold': 3,  # Количество сигм для глобальной фильтрации
    },
    'local_filter': {
        'grid_size': 100,  # Размер ячеек сетки для локальной фильтрации (в метрах)
        'z_sigma_threshold': 3,  # Количество сигм для локальной фильтрации
    },
}


# ===== 2.2 - Reduce points Filter
path_las_many_points = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_large"
path_las_reduced_points = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points"
number_of_points = 3_000_000
#number_of_points = 1048576

# ===== 2.3 - Relief variation Filter
path_las_with_rv = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_cut"
path_las_no_rv = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_cut_rv"
W_filter = 10
sigma = 100.0
cutoff1=0.001
cutoff2=0.01

# ===== 3. Cut LAS - slicing.py
# ===== 3.1
# path_las_before_cut = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_rv"
# path_las_after_cut = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_cut"

path_las_before_cut = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim"
path_las_after_cut = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_cut"
las_cut_size = 250

# ===== 3.2 Cuted LAS Filter
# Good filter to remove files which you know to remove 
# (after cut slices after cut or after distance anomalies)
path_las_cut_las_to_filter = ""
files_to_remove = [
                   "", 
                   "", 
                   ""
                   ]

# ===== Filtering post slising - post_slicing_filtering.py
path_las_sliced = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_cut"
true_amount_of_files = 3
 
# ===== 4. TRANSFORMATION 2D - transformation.py
path_input_las_for_2d = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_cut_rv"
path_out_tensors = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_transform"
K_nn = 10
M_tensor_size = 512
num_points_lim = 100_000
feature_input_tensor = {
    "x": 0,
    "y": 1,
    "z": 2,
    "r": 3,
    "g": 4,
    "b": 5,
    "class": 6,
}
feature_output_tensor = {
                "z_mean": 0,
                "z_std": 1,
                "dist_mean": 2,
                "r": 3,
                "g": 4,
                "b": 5,
                "class": 6
                }


# ===== 5. Join tensors
path_tensors_to_join = ""
path_joined_tensor = ""
# ===== 6. Visualisation - image_generator.py
path_tensor_to_visual = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_transform"
path_image = r"C:\Users\alexe\Downloads\UM\work\Data\Hessigheim_Benchmark\Epoch_March2016\LiDAR\org\Hessigheim_img_rgb_rv"

channels_visualisation = {
    "r":0,
    "g":1,
    "b":2,
}

# channels_visualisation = {
#     "class":0,
#     "class":1,
#     "class":2,
# }

# channels_visualisation = {
#     "z_mean":0,
#     "z_std":1,
#     "n_z":2,
# }

#===== prediction preprocessing
