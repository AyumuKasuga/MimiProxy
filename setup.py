from distutils.core import setup
import sys

requires = []

if sys.version_info[0] >= 3 and sys.version_info[1] >= 3:
    #ok
    if sys.version_info[1] == 3:
        requires.append('asyncio')
else:
    print("Sorry, this version requires python 3.3 or higher")
    sys.exit()

setup(
    name='MimiProxy',
    packages=['MimiProxy'],
    version='0.0.4-experimental',
    description='Small SOCKS5 proxy server on python3',
    author='Andrey Kostakov',
    author_email='bps@dzen.ws',
    url='https://github.com/AyumuKasuga/MimiProxy',
    download_url='https://github.com/AyumuKasuga/MimiProxy/releases',
    keywords=['proxy', 'socks5', 'python3'],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'mimiproxy = MimiProxy.proxy:run',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
    ],
)
