from setuptools import setup, find_packages

setup(
    name="glocal-policy-guardrail",
    version="0.1.0",
    description="Automated Policy-as-Code framework for Smart TV/OTT platforms",
    author="Glocal Policy Team",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pyyaml>=6.0.1",
        "pydantic>=2.5.3",
    ],
    extras_require={
        "test": [
            "pytest>=7.4.4",
            "httpx>=0.26.0",
        ],
    },
    python_requires=">=3.8",
)
