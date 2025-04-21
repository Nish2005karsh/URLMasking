from setuptools import setup, find_packages

setup(
    name='maskgod',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pyshorteners',
        'qrcode[pil]',
    ],
    entry_points={
        'console_scripts': [
            'maskgod=maskgod.main:main',
        ],
    },
    author="Nishkarsh",
    author_email="daynick510@gmail.com",
    description="A URL masking and shortening tool.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nish2005karsh/maskgod',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
