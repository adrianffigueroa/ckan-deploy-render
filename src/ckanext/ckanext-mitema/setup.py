from setuptools import setup, find_packages

setup(
    name='ckanext-mitema',
    version='0.0.1',
    description='Tema personalizado para CKAN',
    author='Tu Nombre',
    license='MIT',
    packages=find_packages('ckanext'),  # 👈 importante
    package_dir={'': 'ckanext'},        # 👈 importante
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [ckan.plugins]
        mitema=mitema.plugin:MiTemaPlugin

        [ckan.templates]
        mitema=ckanext.mitema
    ''',
)
