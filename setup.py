from setuptools import setup, find_packages

setup(
    name="AI",  # 库的名称，导入时用这个名字
    version="0.1",  # 版本号，更新代码时递增
    packages=find_packages(),  # 自动找到所有包
    author="EPI",  # 可选，作者名
    description="My personal Python library"  # 可选，简单描述
)
