# ☀ 待优化说明
## ☞ url2pdf:
* 现方案时间一篇文章大概一分钟，需要优化时间。
* 需要适配windows环境，或者搭建linux虚拟机环境。
## ☞ get_gzh_essay:
* 现方案仅适配华为Mate9手机，需要适配备用机。
---

# ☀ 模块功能说明
## ☞ 微信公众号文章批量下载并转换为pdf
```
原理：
* 通过手机adb直接爬取
* 通过手机adb爬取微信公众号历史文章的 “ 日期_标题：链接 ” 。
* 通过网页打开并打印为pdf。

准备工作：
* 需要一部手机设置为1080*800分辨率，安装微信。
* 手机打开到要爬取的公众号的历史文章页。
```

---
# ☀ 开发贴士
* 不同手机的通用性：
```
    屏幕截图需要在pic_flg/下新建对应分辨率的文件夹，以存放不同分辨率的不同flg，以达到可移植、可配置性。
    对应的需要在py里设置config list、dict实现可配置性。
```

---
# ☀ 附录：
* [.md即markdown文件的基本常用编写语法](https://www.cnblogs.com/liugang-vip/p/6337580.html)