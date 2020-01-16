import setuptools

description_file = open('README.md', 'r', encoding='utf-8')

setuptools.setup(
    name='BIT Online Code Helper',
    version='1.0.2',
    description='Test your code of "BIT Online coding homework" more easily and conveniently!',
    long_description=description_file.read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Crawler995/BITOnlineCodeHelper',
    author='crawler995',
    author_email='zhang_995@foxmail.com',
    keywords=['BIT', 'code', 'helper'],
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'requests',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'bch=bit_online_code_helper.main:main'
        ]
    }
)