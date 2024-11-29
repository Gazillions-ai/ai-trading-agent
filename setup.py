from setuptools import setup, find_packages

setup(
    name="ai-trading-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'streamlit',
        'plotly',
        'vaderSentiment',
        'torch',
        'transformers'
    ]
)
