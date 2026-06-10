"""
Py3DTiles 命令行入口（专用于 PyInstaller 打包）。

Windows 下将程序打包为 exe 后，convert 会通过 multiprocessing 启动子进程。
若不在入口处调用 freeze_support()，子进程会再次执行 argparse，
误把 parent_pid=... 当作子命令，导致报错并卡住。
"""

import multiprocessing

from py3dtiles.command_line import main


def run() -> None:
    """启动 Py3DTiles 命令行主程序。"""
    main()


if __name__ == "__main__":
    # Windows frozen exe 多进程引导，必须在 main 之前调用
    multiprocessing.freeze_support()
    run()
