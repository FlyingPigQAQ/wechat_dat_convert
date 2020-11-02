import sys
from enum import Enum


class ImgType(Enum):
    gif = 0x4749
    jpg = 0xFFD8
    png = 0x8950


class WechatConvert(object):

    def __init__(self, absolute_file_path):
        self.file_path = absolute_file_path
        self.file_name = self.file_path.split("/")[-1]

    def _find_and_set_img_type(self):
        with open(self.file_path, 'rb+') as f:
            byte1 = int.from_bytes(f.read(1), byteorder=sys.byteorder)
            byte2 = int.from_bytes(f.read(1), byteorder=sys.byteorder)
        for img_enum in ImgType:
            if self._set_img(img_enum, byte1, byte2):
                return
        raise Exception("不支持的图片类型")

    def _set_img(self, img: ImgType, b1, b2):
        png_tuple = self._hex2tuple(img.value)
        if png_tuple[0] ^ b1 == png_tuple[1] ^ b2:
            self._img_type = img.name
            self._img_xor = png_tuple[0] ^ b1
            return True
        return False

    def _hex2tuple(self, img_type):
        return img_type >> 8, img_type & 0b11111111

    def convert(self, output_path="."):
        # 获取图片类型
        self._find_and_set_img_type()
        with open(self.file_path, 'rb+') as fd:
            # 读取2 byte
            with open(output_path + "/" + self.file_name + "." + self._img_type, 'wb+') as w:
                while True:
                    b = fd.read(1)
                    if not b:
                        break
                    real = int.from_bytes(b, byteorder=sys.byteorder) ^ self._img_xor
                    real_bytes = int.to_bytes(real, 1, sys.byteorder)
                    w.write(real_bytes)




