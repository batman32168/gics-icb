from distutils.core import setup

setup(
    name='icb',
    packages=['icb', 'icb.definitions'],
    version='0.1-alpha.1',
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='This library provides a way to parse, manipulate and analyze ICB codes.',
    author='Batman32168',
    author_email='batman32168@web.de',
    url='https://github.com/batman32168/py-icb',
    download_url='https://github.com/dorklein/batman32168/archive/v0.1-alpha.6.tar.gz',
    keywords=['ICB', 'Industry Classification Benchmark'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)