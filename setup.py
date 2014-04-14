from distutils.core import setup

setup(
    name='MiMiProxy',
    packages=['MiMiProxy'],
    version='0.0.4',
    description='Small SOCKS5 proxy server on python3',
    author='Andrey Kostakov',
    author_email='bps@dzen.ws',
    url='https://github.com/AyumuKasuga/MimiProxy',
    download_url='https://github.com/AyumuKasuga/MimiProxy/releases',
    keywords=['proxy', 'socks5', 'python3'],
    entry_points={
        'console_scripts': [
            'MiMiProxy = MiMiProxy.proxy:run',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
    ],
)
