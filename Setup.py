"""!
@file setup.py
@brief Скрипт для установки пакета

Содержит функции для чтения зависимостей и настройки пакета.
"""

from setuptools import setup, find_packages
import json
import os


def read_pipenv_dependencies(fname):
    """!
    @brief Получает зависимости из файла requirements.txt

    @param fname Имя файла с зависимостями
    @return Список зависимостей
    """
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


if __name__ == '__main__':
    setup(
        name='demo',
        version=os.getenv('PACKAGE_VERSION', '0.0.dev0'),
        package_dir={'': 'src'},
        packages=find_packages('src', include=[
            'demo*'
        ]),
        description='A demo package.',
        install_requires=[
            *read_pipenv_dependencies('requirements.txt'),
        ]
    )