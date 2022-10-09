import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animeworld",
    version="1.4.20",
    author="MainKronos",
    description="AnimeWorld UNOFFICIAL API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MainKronos/AnimeWorld-API",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'youtube_dl', 'beautifulsoup4'],
	license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
		"Topic :: Utilities",
    ],
    python_requires='>=3.6',
)