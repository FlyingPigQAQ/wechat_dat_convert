# 微信.dat图片文件还原
## 1. 原理
微信采用的是伪加密的方式处理图片,即将每一字节进行异或操作。
## 2. 图片类型支持
- [x] png
- [x] gif
- [x] jpg
### 2.1 支持拓展图片
添加图片的start marker到 ImgType枚举类
## 3. 使用方法
```python
from datToimage import WechatConvert

if __name__ == '__main__':
    WechatConvert().convert("/Users/tobbyquinn/Downloads/2019-11/a997b7d544722c521ff14b83677f3fb0.dat",output_path=".")
```