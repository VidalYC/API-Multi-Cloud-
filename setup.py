"""
Setup configuration for VM Provisioning API
"""
from setuptools import setup, find_packages

setup(
    name='vm-provisioning-api',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask>=3.0.0',
        'flask-cors>=4.0.0',
        'python-dotenv>=1.0.0',
        'requests>=2.31.0',
    ],
    python_requires='>=3.8',
    author='Universidad Popular del Cesar',
    description='API Multi-Cloud VM Provisioning with Factory Method Pattern',
)