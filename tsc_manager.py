import ctypes
import json
import os
from PIL import Image
import numpy as np


DPI = 200  # DPI of printer
DOT = DPI // 100 * 4  # Dots per mm

tsclibrary = ctypes.WinDLL("TSCLIB.dll");


def open_port(port):
    tsclibrary.openport(port)


def close_port():
    tsclibrary.closeport()


def clear_buffer():
    tsclibrary.clearbuffer()


def print_label(set, copy):
    tsclibrary.printlabel(set, copy)


def send_command(command_line):
    tsclibrary.sendcommand(command_line)


def windows_font(x, y, font_height, rotation, font_style, font_underline, font_name, content):
    tsclibrary.windowsfont(x, y, font_height, rotation, font_style, font_underline, font_name, content)


def windows_font_unicode(x, y, font_height, rotation, font_style, font_underline, font_name, content):
    tsclibrary.windowsfontUnicode(x, y, font_height, rotation, font_style, font_underline, font_name, content)


def print_image(image_file, x, y, mode, page_width = 40, page_height = 30):
    print("PRINTING ", image_file)
    im = Image.open(image_file)
    im.thumbnail((page_width * DOT, page_height * DOT), Image.ANTIALIAS)
    width, height = im.size

    if width < 248:  # report err for now, edit later
        print("FAILURE: IMAGE IS TOO SMALL\n")
        return -1

    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data)
    data = data.tolist()[0]

    im1 = [1 for i in range(width * height)]
    for i in range(width * height):
        if data[i] < 128:
            im1[i] = 0
    bitmap = [0 for i in range(width * height // 8)]  # sending 0 may cause some err
    offset = [255 for i in range(width * height // 8)]  # so use offset to make it work
    for i in range(width * height // 8):
        bitmap[i] = eval(
            "0b" + str(im1[i * 8:(i + 1) * 8]).replace(" ", "").replace(",", '').replace("[", '').replace("]",
                                                                                                          ''))
        if bitmap[i] == 0:
            bitmap[i] = 1
            offset[i] = 254
    # seeBitmap(bitmap)
    ini = "BITMAP " + str(x) + "," + str(y) + "," + str(width // 8) + "," + str(height) + "," + str(mode) + ","
    ini = ini.encode()
    bm = bytes(bitmap)
    ofs = bytes(offset)
    end = "\0".encode()
    tsclibrary.sendcommand(ini + bm + end);
    tsclibrary.sendcommand(ini + ofs + end);
    return


def main():
    with open("command_line.json", 'r', encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    print(load_dict)

    open_port(load_dict["port"])
    send_command('SIZE ' + str(load_dict["pageWidth"]) + ' mm, ' + str(load_dict["pageHeight"]) + ' mm')

    for command in load_dict["data"]:
        if command["type"] == 'text':
            windows_font(command["x"],
                         command["y"],
                         command["fontHeight"],
                         command["rotation"],
                         command["fontStyle"],
                         command["fontUnderline"],
                         command["fontName"],
                         command["content"])
        elif command["type"] == 'command':
            send_command(command["data"])
        elif command["type"] == 'image':
            print_image(command["imageFile"],
                        command["x"],
                        command["y"],
                        command["mode"],
                        load_dict["pageWidth"],
                        load_dict["pageHeight"])

    print_label(str(load_dict["set"]), str(load_dict["copy"]))
    close_port()

if __name__ == "__main__":
    main()
