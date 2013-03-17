from setuptools import setup, find_packages

entry_points = '''
'''

setup(
        name = 'callbacks',
        version = '0.1',
        packages = find_packages(exclude=[
            'tests',
        ]),
        entry_points = entry_points,
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
