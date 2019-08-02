import matplotlib.pyplot as plt

colormap = plt.get_cmap("viridis")

gray = (128, 128, 128, 255)


def mapValueToRange(old_min, old_max, new_min, new_max, value):
    old_range = old_max - old_min
    new_range = new_max - new_min
    scaled_value = float(value - old_min) / float(old_range)
    return new_min + (scaled_value * new_range)


def map2DArray(func, arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] = func(arr[i][j])
    return arr
