from setuptools import setup, find_packages

setup(
        name = 'callbacks',
        author = 'David Morton',
        author_email = 'davidlmorton@gmail.com',
        version = '0.1.3',
        license = 'LICENSE.txt',
        description = 'Simple callbacks using decorators',
        long_description = open('README.txt').read(),
        url = 'https://github.com/davidlmorton/callbacks',
        packages = find_packages(exclude=[
            'tests',
        ]),
        install_requires = [
        ],
        setup_requires = [
            'nose',
        ],
        tests_require = [
            'nose',
            'coverage',
        ],
        test_suite = 'tests',
)
