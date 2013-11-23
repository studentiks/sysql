import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
   name="sysql"
 , version="20131123"
 , author="Roman Denisov"
 , author_email="roman.denisov@mail.ru"
 , description="sysql - use sql queries against output of linux commands"
 , license="MIT"
 , url="https://github.com/studentiks/sysql"
 , long_description=read("README.md")
 , packages = ['commands']
 , scripts=["sysql"]
)