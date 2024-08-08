#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *

def apply_filter(image, drawable, rust_color1, rust_color2, error, quality):
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)
    
    layer_to_process = pdb.gimp_layer_copy(drawable, False)
    proc_width = int(layer_to_process.width * quality / 100)
    proc_height = int(layer_to_process.height * quality / 100)
    image.add_layer(layer_to_process, 0)
    pdb.gimp_layer_scale(layer_to_process, proc_width, proc_height, False)
    
    bg = pdb.gimp_context_get_background()
    pdb.gimp_context_set_background((0, 0, 0))
    mask_layer = gimp.Layer(image, "Rust Mask Layer", proc_width, proc_height, RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_drawable_fill(mask_layer, 1)
    
    color_range = [abs(rust_color1[0] - rust_color2[0]), abs(rust_color1[1] - rust_color2[1]), abs(rust_color1[2] - rust_color2[2])]
    color_average = [(rust_color1[0] + rust_color2[0]) / 2, (rust_color1[1] + rust_color2[1]) / 2, (rust_color1[2] + rust_color2[2]) / 2]
    
    for y in range(proc_height):
        for x in range(proc_width):
            pixel_color = layer_to_process.get_pixel(x, y)
            if all(abs(pixel_color[i] - color_average[i]) <= (color_range[i] / 2 + color_range[i] / 2 * error) for i in range(3)):
                mask_layer.set_pixel(x, y, (255, 255, 255))
    
    pdb.gimp_image_remove_layer(image, layer_to_process)
    
    image.add_layer(mask_layer, 0)
    pdb.gimp_layer_scale(mask_layer, image.width, image.height, False)
    mask_layer.update(0, 0, mask_layer.width, mask_layer.height)
    
    pdb.gimp_context_set_background(bg)
    
    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_context_pop()

# Регистрация скрипта в GIMP
register(
            "python-fu_rust_finder",
            "Rust Finder",
            "Finds rust and covers it with white color",
            "Romanov Andrei B21-503",
            "Romanov Andrei B21-503",
            "2023",
            "Rust Finder",
            "*",  # Image type - all types
            [
                (PF_IMAGE, "image", "Input image", None),
                (PF_DRAWABLE, "drawable", "Input drawable", None),
                (PF_COLOR, "rust_color1", "Цвет ржавчины 1", (183, 65, 14)),
                (PF_COLOR, "rust_color2", "Цвет ржавчины 2", (183, 65, 14)),
                (PF_FLOAT, "error", "Погрешность", 0.5),
                (PF_SLIDER, "quality", "Качество", 50, (1, 100, 1))
            ],
            [],
            apply_filter,
            menu="<Image>/Filters/"
        )

main()
