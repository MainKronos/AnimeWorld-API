import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animeworld", # Replace with your own username
    version="1.3.6",
    author="MainKronos",
    author_email="lorenzo.chesi@live.it",
    description="AnimeWorld UNOFFICIAL API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MainKronos/AnimeWorld-API",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'youtube_dl', 'beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)