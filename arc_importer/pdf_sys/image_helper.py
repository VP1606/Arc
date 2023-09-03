from PIL import Image

# X Lines: 0-550, 550-1100, 1100-END ::: WIDTH=550
# y Lines: 215-515, 515-815, 815-1115, 1115-1415, 1415-1715, 1715-2015, 2015-END ::: HEIGHT=300

x_lines = [[0, 550], [550, 1100], [1100, -1]]
y_lines = [[215, 515], [515, 815], [815, 1115], [1115, 1415], [1415, 1715], [1715, 2015], [2015, -1]]

def cut_items(image: Image):
    book_images = list()

    for y_bound in y_lines:
        for x_bound in x_lines:

            right = x_bound[1]
            if right == -1:
                right = image.width
            
            bottom = y_bound[1]
            if bottom == -1:
                bottom = image.height

            cropped = image.crop((x_bound[0], y_bound[0], right, bottom))
            book_images.append(cropped)
    
    return book_images

def check_if_occupied(image: Image):
    target_colour = (0, 0, 0)
    color_found = False

    image_rgb = image.convert('RGB')

    for x in range(image.width):
        for y in range(image.height):
            pixel_color = image_rgb.getpixel((x, y))
            if pixel_color == target_colour:
                color_found = True
                break
        if color_found:
            break

    return color_found
