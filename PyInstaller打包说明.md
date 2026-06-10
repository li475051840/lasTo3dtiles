# PyInstaller 打包说明（Windows 独立运行版）

本文说明如何将**本仓库**（含自定义修改）打包为 Windows 可执行程序，供客户**无需安装 Python** 直接使用。

---

## 1. 为什么需要 `run_py3dtiles.py`

Py3DTiles 的 `convert` 在 Windows 上会使用 `multiprocessing` 启动多个子进程。

若直接用 `py3dtiles.command_line:main` 作为 PyInstaller 入口，子进程 re-exec 时会再次进入 `argparse`，出现类似错误并卡住：

```text
invalid choice: 'parent_pid=35172' (choose from 'convert', 'info', 'merge', 'export', 'view')
```

**正确做法**：以 `run_py3dtiles.py` 为入口，并在其中调用 `multiprocessing.freeze_support()`。

---

## 2. 打包环境准备（仅开发机需要）

### 2.1 推荐 Python 版本

```text
Python 3.12.x（推荐）
```

不建议使用 3.14 作为打包环境（兼容性与依赖成熟度较差）。

### 2.2 创建虚拟环境

```powershell
cd G:\李玮\cxqlhyq\lasTo3dtiles

python -m venv .venv-pack
.\.venv-pack\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 2.3 安装本项目及 LAS 依赖

```powershell
pip install -e ".[las]"
pip install lazrs
pip install pyinstaller
```

验证源码安装成功：

```powershell
python run_py3dtiles.py --help
python run_py3dtiles.py convert --help
```

---

## 3. 执行打包

在项目根目录执行：

```powershell
pyinstaller py3dtiles.spec --noconfirm
```

成功后输出目录：

```text
dist\py3dtiles\
├── py3dtiles.exe          ← 主程序
├── _internal\             ← 依赖库与数据文件（整个文件夹都需要）
└── ...
```

> 采用 **onedir（目录模式）**，比 onefile 更稳定，尤其适用于 numba、pyproj、pyzmq。

---

## 4. 交付给客户的内容

将 **整个** `dist\py3dtiles\` 文件夹打包为 zip 发给客户，例如：

```text
py3dtiles-win64.zip
└── py3dtiles\
    ├── py3dtiles.exe
    └── _internal\
```

客户解压后可直接运行，**不要只拷贝 exe**（`_internal` 必须一起保留）。

---

## 5. 客户使用示例

在 PowerShell 中（路径按实际修改）：

```powershell
cd D:\tools\py3dtiles

.\py3dtiles.exe convert `
"G:\数据\城市路面.las" `
--out "G:\输出\城市路面" `
--overwrite `
--color_scale 256 `
--srs_in 4547 `
--srs_out 4978 `
--pyproj-always-xy `
--verbose
```

### 5.1 可选：提供 `convert.bat` 简化调用

在 `dist\py3dtiles\` 下新建 `convert.bat`：

```bat
@echo off
setlocal
cd /d "%~dp0"
py3dtiles.exe convert %*
endlocal
```

客户用法：

```bat
convert.bat "input.las" --out "output" --overwrite --color_scale 256 --srs_in 4547 --srs_out 4978 --pyproj-always-xy
```

---

## 6. 常见问题

### 6.1 仍然出现 `parent_pid=...` 错误

- 确认打包入口是 **`run_py3dtiles.py`**，不是 `command_line.py`
- 确认使用的是 **`py3dtiles.spec`** 重新打包后的新版本
- 不要只替换 exe，要替换整个 `dist\py3dtiles\` 目录

### 6.2 转换很慢或内存占用高

- 默认 `--jobs` 为 CPU 逻辑核心数，可通过 `--jobs 4` 限制并行数
- 大点云可加 `--cache_size 4096`（单位 MB）

### 6.3 坐标不对

- LAS 无内嵌 CRS 时必须 `--srs_in <EPSG>`
- Cesium 加载需 `--srs_out 4978`
- 国内投影坐标建议加 `--pyproj-always-xy`

### 6.4 RGB 全黑

- 8 位 RGB 写入 16 位字段时加 `--color_scale 256`

### 6.5 只有 intensity、无 RGB

- 本仓库已支持 intensity 转灰度，**不要**对纯 intensity 点云使用 `--color_scale 256`（会导致全白）

### 6.6 打包后运行报缺少模块

在 `py3dtiles.spec` 的 `hiddenimports` 中补充缺失模块后重新打包。常见已包含：

- `py3dtiles` 全子模块
- `laspy` / `lazrs`
- `pyproj`（含 PROJ 数据）
- `numba` / `zmq` / `numpy`

---

## 7. 重新打包流程（发布新版本时）

```powershell
.\.venv-pack\Scripts\Activate.ps1
git pull
pip install -e ".[las]"
pip install lazrs pyinstaller

# 清理旧产物
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

pyinstaller py3dtiles.spec --noconfirm
```

将新的 `dist\py3dtiles\` 打成 zip 发布。

---

## 8. 与 pip 安装方式对比

| 方式 | 客户是否需要 Python | 稳定性 | 适用场景 |
|------|---------------------|--------|----------|
| **PyInstaller（本文）** | 否 | 中（需注意多进程入口） | 交付给无技术背景客户 |
| **pip + venv（见 Py3DTiles部署指南.md）** | 是 | 高 | 内部服务器、可维护环境 |

---

## 9. 相关文件

| 文件 | 说明 |
|------|------|
| `run_py3dtiles.py` | PyInstaller 专用入口，含 `freeze_support()` |
| `py3dtiles.spec` | PyInstaller 打包配置（onedir） |
| `Py3DTiles使用指南.md` | convert 参数说明 |
| `Py3DTiles部署指南.md` | Python 环境部署方式 |
