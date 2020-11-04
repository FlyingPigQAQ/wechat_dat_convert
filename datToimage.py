import sys
from enum import Enum


class ImgType(Enum):
    gif = 0x4749
    jpg = 0xFFD8
    png = 0x8950


class WechatConvert(object):

    @staticmethod
    def find_img_type(file_path):
        with open(file_path, 'rb+') as f:
            byte1 = int.from_bytes(f.read(1), byteorder=sys.byteorder)
            byte2 = int.from_bytes(f.read(1), byteorder=sys.byteorder)
        for img_enum in ImgType:
            png_tuple = WechatConvert.hex_to_tuple(img_enum.value)
            if png_tuple[0] ^ byte1 == png_tuple[1] ^ byte2:
                return img_enum.name, png_tuple[0] ^ byte1
        raise Exception("不支持的图片类型")

    @staticmethod
    def hex_to_tuple(img_type):
        return img_type >> 8, img_type & 0b11111111

    def convert(self, file_path, output_path="."):
        file_name = file_path.split("/")[-1]
        # 获取图片类型
        img_type,img_xor = WechatConvert.find_img_type(file_path)
        with open(file_path, 'rb+') as fd:
            # 读取2 byte
            with open(output_path + "/" + file_name + "." + img_type, 'wb+') as w:
                while True:
                    b = fd.read(1)
                    if not b:
                        break
                    real = int.from_bytes(b, byteorder=sys.byteorder) ^ img_xor
                    real_bytes = int.to_bytes(real, 1, sys.byteorder)
                    w.write(real_bytes)