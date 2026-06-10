# Python 点云转换环境部署手册

## 1. 环境准备

### 1.1 安装 Python

推荐版本：

```text
Python 3.10+
```

检查是否安装成功：

```bash
python --version
```

或：

```bash
python -V
```

示例输出：

```text
Python 3.12.3
```

---

### 1.2 检查 Pip

Pip 是 Python 的包管理器。

检查版本：

```bash
pip --version
```

示例输出：

```text
pip 25.1
```

如果提示不存在，可执行：

```bash
python -m ensurepip --upgrade
```

---

### 1.3 升级 Pip

建议安装完成后立即升级：

```bash
python -m pip install --upgrade pip
```

---

## 2. 创建独立虚拟环境（推荐）

服务器部署时建议使用虚拟环境。

创建环境：

```bash
python -m venv venv
```

激活环境：

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

成功后命令行前面会出现：

```text
(venv)
```

---

## 3. 安装点云处理工具

### 3.1 安装 laspy

用于读取和写入 LAS/LAZ 文件。

```bash
pip install laspy
```

如果需要读取 LAZ：

```bash
pip install laspy[lazrs]
```

验证：

```bash
python -c "import laspy; print(laspy.__version__)"
```

---

### 3.2 安装 py3dtiles

用于生成 3D Tiles。

```bash
pip install py3dtiles
```

验证：

```bash
python -m py3dtiles.command_line --help
```

如果输出帮助信息说明安装成功。

---

### 3.3 安装 PDAL（推荐）

PDAL 是点云领域最常用的工具。

官网：

https://pdal.io/

验证：

```bash
pdal --version
```

查看点云信息：

```bash
pdal info xxx.las
```

查看汇总信息：

```bash
pdal info --summary xxx.las
```

---

## 4. COPC.LAZ 转 LAS

### 什么是 COPC

COPC（Cloud Optimized Point Cloud）：

```text
.copc.laz
```

本质上仍然是：

```text
LAZ
```

只是增加了空间索引结构。

---

### 方法一：使用 laspy（推荐）

创建：

```python
import laspy

las = laspy.read("input.copc.laz")
las.write("output.las")
```

执行：

```bash
python copc_to_las.py
```

---

### 方法二：使用 PDAL

转换：

```bash
pdal translate input.copc.laz output.las
```

---

### 方法三：CloudCompare

打开：

```text
input.copc.laz
```

然后：

```text
File
 └ Export
      └ LAS
```

保存即可。

---

## 5. 检查 LAS 是否包含颜色

查看信息：

```bash
pdal info output.las
```

重点检查：

```json
"Red"
"Green"
"Blue"
```

如果存在这些字段：

```text
说明包含 RGB 颜色
```

---

## 6. LAS 转 3D Tiles

### 基本命令

```bash
py3dtiles convert input.las
```

或：

```bash
python -m py3dtiles.command_line convert input.las
```

---

### 指定输出目录

```bash
py3dtiles convert input.las \
  --out output_tiles
```

生成：

```text
output_tiles/
├── tileset.json
├── r.pnts
└── ...
```

---

### Cesium 推荐参数

```bash
py3dtiles convert input.las \
  --srs_out 4978 \
  --out output_tiles
```

说明：

```text
EPSG:4978
=
Cesium 默认地心坐标系
```

---

## 7. 黑色点云问题

如果转换后点云全黑：

先检查 RGB 范围：

```bash
pdal info output.las
```

查看：

```json
Red
Green
Blue
```

---

### 情况一：RGB 范围是 0-255

例如：

```text
Red max=255
Green max=255
Blue max=255
```

转换时增加：

```bash
--color_scale 256
```

示例：

```bash
py3dtiles convert input.las \
  --color_scale 256
```

---

### 情况二：RGB 范围是 0-65535

例如：

```text
Red max=65535
Green max=65535
Blue max=65535
```

这是标准 LAS。

无需添加：

```bash
--color_scale
```

---

## 8. 常用排查命令

查看 LAS 信息：

```bash
pdal info file.las
```

查看 CRS：

```bash
pdal info --summary file.las
```

查看 RGB：

```bash
pdal info file.las
```

查看 py3dtiles 版本：

```bash
python -m py3dtiles.command_line --version
```

查看安装位置：

```bash
python -c "import py3dtiles;print(py3dtiles.__file__)"
```

查看 Python 搜索路径：

```bash
python -c "import sys;print(sys.path)"
```

---

## 9. 服务器部署推荐安装命令

首次部署：

```bash
python -m pip install --upgrade pip

pip install laspy[lazrs]

pip install py3dtiles
```

验证：

```bash
python -m py3dtiles.command_line --help
```

成功后即可执行：

```bash
python -m py3dtiles.command_line convert input.las
```

---

## 10. Windows 独立 exe 打包（无需客户安装 Python）

若需将本仓库打包为 `py3dtiles.exe` 交付客户，请参阅：

```text
PyInstaller打包说明.md
```

入口脚本为 `run_py3dtiles.py`，配置文件为 `py3dtiles.spec`。
