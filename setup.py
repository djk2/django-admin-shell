# encoding:utf-8
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django-admin-shell',
    version='0.1.2',
    description='',
    url='https://github.com/djk2/django-admin-shell',
    author='Grzegorz Tężycki',
    author_email='grzegorz.tezycki@gmail.com',
    long_description=readme(),
    license='MIT',
    packages=find_packages(exclude=['docs']),
    package_data={'django_admin_shell': [
        'templates/django_admin_shell/*',
        'static/django_admin_shell/js/*',
        'static/django_admin_shell/js/linedtextarea/*',
        'static/django_admin_shell/fonts/*',
        'static/django_admin_shell/css/*',
    ]},
    tests_require=['Django', 'flake8', 'mock'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.9'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords='django admin shell console terminal',
)
