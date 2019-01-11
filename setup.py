# coding: utf-8

from setuptools import setup, find_packages



setup(
    name='helpful_vectors',
    version='0.4.1',
    description='Helpful vectors',
    long_description='Helpful vectors for for utility tasks',
    classifiers=[
        'Development Status :: 4',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Data Processing :: Vectors :: Numpy :: Pandas :: Utility',
    ],
    keywords='helpful vectors for for utility tasks',
    url='',
    author='dgr113',
    author_email='dmitry-gr87@yandex.ru',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'more-itertools'
    ],
    include_package_data=True,
    zip_safe=False
)
