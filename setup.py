from setuptools import setup, find_packages

setup(
    name="guess_who_i_am",
    version="1.0.0",
    description="A guessing game featuring Bollywood and Hollywood celebrities, as well as famous scientists, with a beautiful CLI interface",
    author="Game Developer",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'guess-who-i-am=main:main',
        ],
    },
    install_requires=[
        'rich>=10.0.0',
        'questionary>=1.10.0',
        'pyfiglet>=0.8.post1',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Games/Entertainment',
        'Topic :: Education',
    ],
    keywords='game, cli, celebrity, bollywood, hollywood, scientists, quiz, guess, education, entertainment',
)