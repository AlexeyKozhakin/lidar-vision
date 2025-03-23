# config_preporocessing.py

# ===== training preprocessing =======
# ===== 1. INFO ======================

path_las = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points"

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
path_las_many_points = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb"
path_las_reduced_points = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points"
number_of_points = 3_000_000
#number_of_points = 1048576

# ===== 2.3 - Relief variation Filter
path_las_with_rv = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points"
path_las_no_rv = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_rv"
W_filter = 10
sigma = 100.0
cutoff1=0.001
cutoff2=0.01

# ===== 3. Cut LAS - slicing.py
# ===== 3.1
path_las_before_cut = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_rv"
path_las_after_cut = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_cut"
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

# ===== Filtering post slising
path_las_sliced = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_cut"
true_amount_of_files = 16
 
# ===== 4. TRANSFORMATION 2D
path_input_las_for_2d = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_cut"
path_out_tensors = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_transform"
#path_input_las_for_2d = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_cut"
#path_out_tensors = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_transform"
K_nn = 4
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
                "n_z": 2,
                "r": 3,
                "g": 4,
                "b": 5,
                "class": 6,
                "dist_mean": 7
                }


# ===== 5. Join tensors
path_tensors_to_join = ""
path_joined_tensor = ""
# ===== 6. Visualisation - image_generator.py
path_tensor_to_visual = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_transform"
path_image = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_rgb"
#path_tensor_to_visual = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_3M_points_transform"
#path_image = r"C:\Users\alexe\Downloads\UM\work\GFG\profs\Marfa_images_rgb"
# channels_visualisation = {
#     "r":0,
#     "g":1,
#     "b":2,
# }

# channels_visualisation = {
#     "class":0,
#     "class":1,
#     "class":2,
# }

# channels_visualisation = {
#     "z_mean":0,
#     "z_std":1,
#     "dist_mean":2,
# }

channels_visualisation = {
    "z_mean":0,
    "z_std":1,
    "n_z":2,
}

# ===== 7. Filtering dist_mean
path_tensors_dist_mean_filter = r"D:\data\las_org\data_las_stpls3d\all_org_las_rgb_reduce_points_transform"
#===== prediction preprocessing
