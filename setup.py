import setuptools
import os

setuptools.setup(
    version=os.environ["RELEASE_VERSION"].replace("v.","",1)
)