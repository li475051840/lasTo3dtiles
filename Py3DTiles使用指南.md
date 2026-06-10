# Py3DTiles 使用指南（LAS → 3D Tiles → Cesium）

## 项目简介

Py3DTiles 是一个将点云数据转换为 Cesium 3D Tiles 格式的 Python 工具。

项目地址：

https://gitlab.com/py3dtiles/py3dtiles

适用于：

```text
LAS/LAZ
    ↓
Py3DTiles
    ↓
3D Tiles
    ↓
Cesium
```

---

# 安装

## 克隆源码

```bash
git clone https://gitlab.com/py3dtiles/py3dtiles.git
```

## 安装项目

进入项目目录：

```bash
cd py3dtiles
```

执行：

```bash
pip install -e .
```

安装完成后会生成：

```text
py3dtiles.egg-info
```

说明安装成功。

---

# 注意事项

## Python 3.14

在 Python 3.14 环境中：

```bash
py3dtiles --help
```

可能无法运行。

报错：

```text
CommandNotFoundException
```

但实际上项目已经安装成功。

正确启动方式：

```bash
python -m py3dtiles.command_line
```

而不是：

```bash
py3dtiles
```

---

# 支持格式

convert 命令支持：

```text
.las
.laz
.xyz
.ply
```

官方说明：

```text
The file must use the
.las
.laz
.xyz
.ply
format.
```

---

# 输出格式

默认输出：

```text
tileset.json
*.pnts
```

Cesium 可直接加载。

---

# 常用命令

查看帮助：

```bash
python -m py3dtiles.command_line --help
```

查看 convert 帮助：

```bash
python -m py3dtiles.command_line convert --help
```

---

# convert 命令

基础格式：

```bash
python -m py3dtiles.command_line convert [输入文件] [参数]
```

例如：

```bash
python -m py3dtiles.command_line convert test.las
```

---

# convert 参数说明

## --out

输出目录

默认：

```text
./3dtiles
```

示例：

```bash
--out output
```

---

## --overwrite

覆盖已有目录

示例：

```bash
--overwrite
```

---

## --jobs

并行线程数

默认：

```text
CPU逻辑核心数
```

例如：

```bash
--jobs 16
```

---

## --cache_size

缓存大小（MB）

默认：

```text
可用内存 / 10
```

例如：

```bash
--cache_size 4096
```

---

## --srs_in

指定输入坐标系

示例：

```bash
--srs_in 4547
```

---

## --srs_out

转换输出坐标系

示例：

```bash
--srs_out 4326
```

---

## --benchmark

输出统计信息

示例：

```bash
--benchmark benchmark.txt
```

---

## --no-rgb

忽略颜色信息

示例：

```bash
--no-rgb
```

---

## --extra-fields

保留额外字段

示例：

```bash
--extra-fields intensity classification
```

---

## --color_scale

颜色缩放

示例：

```bash
--color_scale 256
```

---

## --force-srs-in

强制使用指定坐标系

示例：

```bash
--force-srs-in
```

---

## --disable-processpool

关闭多进程

示例：

```bash
--disable-processpool
```

---

## --pyproj-always-xy

强制使用 XY 顺序

示例：

```bash
--pyproj-always-xy
```

---

## --verbose

输出详细日志

示例：

```bash
--verbose
```

---

## --spec-version

支持：

```bash
--spec-version 1.0
```

或：

```bash
--spec-version 1.1
```

默认：

```text
1.0
```

推荐保持默认。

---

# 推荐命令（生产环境）

```bash
python -m py3dtiles.command_line convert ^
"input.las" ^
--out "output" ^
--overwrite ^
--jobs 16 ^
--verbose
```

PowerShell：

```powershell
python -m py3dtiles.command_line convert `
"input.las" `
--out "output" `
--overwrite `
--jobs 16 `
--verbose
```

---

# Cesium 加载

生成：

```text
output
│
├── tileset.json
└── *.pnts
```

加载：

```javascript
const tileset =
    await Cesium.Cesium3DTileset.fromUrl(
        "./tileset.json"
    );

viewer.scene.primitives.add(tileset);
```

---

# 常见问题

## support not found for files

例如：

```text
ERROR: support not found for files
```

可能原因：

1. 文件不是标准 LAS
2. LAS 文件损坏
3. 依赖未正确安装
4. 路径错误

优先验证：

```python
import laspy

las = laspy.read("test.las")
print(las.header)
```

如果可以正常读取，说明 LAS 文件本身没有问题。

---

# 项目入口

主入口：

```bash
python -m py3dtiles.command_line
```

支持命令：

```text
convert
info
merge
export
view
```

---

# 注意事项

Python 3.14 + Py3DTiles 12.1.1 环境下，
不要使用：

py3dtiles convert

而使用：

python -m py3dtiles.command_line convert

这是当前环境验证通过的启动方式。
