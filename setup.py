from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zenbot-pi",
    version="0.1.0",
    author="Inky Ganbold",
    author_email="enkhbold470@gmail.com",
    description="I2C Motor Controller for Raspberry Pi/Arduino robots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enkhbold470",  # Updated URL
    project_urls={
        "Bug Tracker": "https://github.com/enkhbold470/rpi-arduino-motor-rx/issues",  # Updated Bug Tracker URL
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Hardware",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "smbus2>=0.4.2",
    ],
    entry_points={
        "console_scripts": [
            "zenbot-pi=zenbot.main:main",
        ],
    },
) 