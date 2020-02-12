# TSC 标签打印机 Python 实现

Fork from: [https://github.com/RayforLoy/TSC-Printer.git](https://github.com/RayforLoy/TSC-Printer.git)

## 安装依赖

脚本依赖 `numpy` 和 `pillow` 两个包，请使用 pip 包管理工具安装两个依赖库

```
pip install numpy
pip install pillow
```

## 运行流程

`tsc_manager.py` 会读取当前目录下的 `command_line.json` 文件，根据 JSON 数据实现初步的设置和打印功能，请注意修改 `port` 参数以指定你打印机的名称

 - send_command 命令可以执行原生指令
 - windows_font 和 windows_font_unicode 可以打印中文内容
 - print_image 会将图片进行转换缩放并调用 BITMAP 指令打印图片

## JSON 文件示例

```
{
  "pageHeight" : 30,
  "pageWidth" : 40,
  "port" : "Gprinter  GP-1324D",
  "set" : 1
  "copy" : 1,
  "data" : [{
    "type" : "command",
    "data" : "DIRECTION 1"
  }, {
    "type" : "command",
    "data" : "GAP 10mm, 10mm"
  }, {
    "type" : "command",
    "data" : "QRCODE 10,10,H,4,A,0,\"ABCabc123\""
  }, {
    "type" : "text",
    "content" : "中文测试",
    "fontHeight" : 80,
    "fontName" : "Arial",
    "fontStyle" : 0,
    "fontUnderline" : 0,
    "rotation" : 0,
    "x" : 10,
    "y" : 10
  }, {
    "type" : "image",
    "imageFile" : "E:\\cachedFiles\\logo.png",
    "mode" : 1,
    "x" : 100,
    "y" : 100
  }]
}
```

