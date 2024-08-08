#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def bayer_dither(image, drawable, bayer_matrix_size):
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)
    
    # Получаем размер изображения
    width = image.width
    height = image.height
    # Создаем матрицу Байера заданного размера
    bayer_matrix = generate_bayer_matrix(bayer_matrix_size)
    
    # Применяем дизеринг к каждому пикселю изображения
    for y in range(height):
        for x in range(width):
            pixel = drawable.get_pixel(x, y)
            new_values = []
            for i in range(3):  # Итерируем по каналам RGB
                grayscale_value = pixel[i]
                threshold = bayer_matrix[x % bayer_matrix_size][y % bayer_matrix_size]
                new_value = 255 if grayscale_value > threshold else 0
                new_values.append(new_value)

            new_pixel = (new_values[0], new_values[1], new_values[2])
            drawable.set_pixel(x, y, new_pixel)

    # Обновляем изображение
    drawable.update(0, 0, width, height)
    
    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_context_pop()

def generate_bayer_matrix(size):
    if size == 2:
        bayer_matrix = [[0, 128],
                        [192, 64]]
    elif size == 4:
        bayer_matrix = [[0, 192, 48, 240],
                        [128, 64, 176, 112],
                        [32, 224, 16, 208],
                        [160, 96, 144, 80]]
    elif size == 8:
        bayer_matrix = [[0, 128, 32, 160, 8, 136, 40, 168],
                        [192, 64, 224, 96, 200, 72, 232, 104],
                        [48, 176, 16, 144, 56, 184, 24, 152],
                        [240, 112, 208, 80, 248, 120, 216, 88],
                        [12, 140, 44, 172, 4, 132, 36, 164],
                        [204, 76, 236, 108, 196, 68, 228, 100],
                        [60, 188, 28, 156, 52, 180, 20, 148],
                        [252, 124, 220, 92, 244, 116, 212, 84]]
        
    elif size == 16:
        bayer_matrix = [[0, 192, 48, 240, 12, 204, 60, 252, 3, 195, 51, 243, 15, 207, 63, 255],
                        [128, 64, 176, 112, 140, 76, 188, 124, 131, 67, 179, 115, 143, 79, 191, 127],
                        [32, 224, 16, 208, 44, 236, 28, 220, 35, 227, 19, 211, 47, 239, 31, 223],
                        [160, 96, 144, 80, 172, 108, 156, 92, 163, 99, 147, 83, 179, 115, 151, 87],
                        [8, 200, 56, 248, 4, 196, 52, 244, 11, 203, 59, 251, 7, 199, 55, 247],
                        [136, 72, 184, 120, 140, 76, 188, 124, 139, 75, 187, 123, 143, 79, 191, 127],
                        [40, 232, 24, 216, 36, 228, 20, 212, 43, 235, 27, 219, 39, 231, 23, 215],
                        [168, 104, 152, 88, 164, 100, 148, 84, 171, 107, 155, 91, 147, 83, 179, 115],
                        [2, 194, 50, 242, 14, 206, 62, 254, 1, 193, 49, 241, 13, 205, 61, 253],
                        [130, 66, 178, 114, 142, 78, 190, 126, 129, 65, 177, 113, 141, 77, 189, 125],
                        [34, 226, 18, 210, 46, 238, 30, 222, 33, 225, 17, 209, 45, 237, 29, 221],
                        [162, 98, 146, 82, 178, 114, 150, 86, 161, 97, 145, 81, 177, 113, 149, 85],
                        [10, 202, 58, 250, 6, 198, 54, 246, 9, 201, 57, 249, 5, 197, 53, 245],
                        [138, 74, 186, 122, 140, 76, 188, 124, 137, 73, 185, 121, 141, 77, 189, 125],
                        [42, 234, 26, 218, 38, 230, 22, 214, 41, 233, 25, 217, 37, 229, 21, 213],
                        [170, 106, 154, 90, 166, 102, 150, 86, 169, 105, 153, 89, 165, 101, 149, 85]]
    else:
        raise ValueError("Unsupported Bayer matrix size")

    return bayer_matrix

# Регистрация скрипта в GIMP
register(
            "python-fu_bayer_dither",
            "Bayer Dither",
            "",
            "DP",
            "DP",
            "2023",
            "Bayer Dither",
            "*",  # Image type - all types
            [
                (PF_IMAGE, "image", "Input image", None),
                (PF_DRAWABLE, "drawable", "Input drawable", None),
                (PF_INT, "bayer_matrix_size", "Bayer Matrix Size", 2, ["2x2", "4x4", "8x8", "16x16"])
            ],
            [],
            bayer_dither,
            menu="<Image>/Filters/"
        )

main()
