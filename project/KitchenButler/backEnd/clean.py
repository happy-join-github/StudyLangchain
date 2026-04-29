import os
import shutil
from pathlib import Path

def clean_pycache(root_dir: str = None):
    """清除 __pycache__ 目录"""
    if root_dir is None:
        root_dir = os.getcwd()
    
    count = 0
    for pycache_dir in Path(root_dir).rglob("__pycache__"):
        shutil.rmtree(pycache_dir)
        # print(f"已删除: {pycache_dir}")
        count += 1
    
    # 同时清理 .pyc 文件
    for pyc_file in Path(root_dir).rglob("*.pyc"):
        pyc_file.unlink()
        # print(f"已删除: {pyc_file}")
        count += 1
    
    print(f"\n共清除 {count} 个文件/目录")

if __name__ == "__main__":
    clean_pycache()