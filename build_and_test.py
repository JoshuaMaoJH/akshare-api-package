#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 构建和测试脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, cwd=None):
    """运行命令"""
    print(f"运行命令: {command}")
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"命令失败: {command}")
            print(f"错误输出: {result.stderr}")
            return False
        else:
            print(f"命令成功: {command}")
            if result.stdout:
                print(f"输出: {result.stdout}")
            return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False


def clean_build():
    """清理构建文件"""
    print("清理构建文件...")
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_clean:
        if os.path.exists(pattern):
            if os.path.isdir(pattern):
                shutil.rmtree(pattern)
            else:
                os.remove(pattern)
    print("构建文件清理完成")


def check_package_structure():
    """检查包结构"""
    print("检查包结构...")
    
    required_files = [
        'akshare_api/__init__.py',
        'akshare_api/cli.py',
        'tests/__init__.py',
        'tests/test_akshare_api.py',
        'README.md',
        'LICENSE',
        'pyproject.toml',
        'setup.py',
        'MANIFEST.in',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"缺少文件: {missing_files}")
        return False
    
    print("包结构检查通过")
    return True


def install_build_dependencies():
    """安装构建依赖"""
    print("安装构建依赖...")
    dependencies = ['build', 'twine', 'wheel']
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}"):
            print(f"安装 {dep} 失败")
            return False
    
    print("构建依赖安装完成")
    return True


def build_package():
    """构建包"""
    print("构建包...")
    
    if not run_command("python -m build"):
        print("包构建失败")
        return False
    
    print("包构建成功")
    return True


def check_package():
    """检查包"""
    print("检查包...")
    
    if not run_command("twine check dist/*"):
        print("包检查失败")
        return False
    
    print("包检查通过")
    return True


def run_tests():
    """运行测试"""
    print("运行测试...")
    
    # 安装包到当前环境
    if not run_command("pip install -e ."):
        print("包安装失败")
        return False
    
    # 运行测试
    if not run_command("python -m pytest tests/ -v"):
        print("测试失败")
        return False
    
    print("测试通过")
    return True


def main():
    """主函数"""
    print("AKShare API 构建和测试脚本")
    print("=" * 50)
    
    # 检查包结构
    if not check_package_structure():
        print("包结构检查失败，退出")
        sys.exit(1)
    
    # 清理构建文件
    clean_build()
    
    # 安装构建依赖
    if not install_build_dependencies():
        print("构建依赖安装失败，退出")
        sys.exit(1)
    
    # 构建包
    if not build_package():
        print("包构建失败，退出")
        sys.exit(1)
    
    # 检查包
    if not check_package():
        print("包检查失败，退出")
        sys.exit(1)
    
    # 运行测试
    if not run_tests():
        print("测试失败，退出")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ 所有步骤完成！")
    print("\n下一步:")
    print("1. 检查 dist/ 目录中的包文件")
    print("2. 上传到测试PyPI: twine upload --repository testpypi dist/*")
    print("3. 测试安装: pip install --index-url https://test.pypi.org/simple/ akshare-api")
    print("4. 上传到正式PyPI: twine upload dist/*")


if __name__ == "__main__":
    main()
