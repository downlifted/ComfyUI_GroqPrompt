from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ComfyUI_GroqPrompt",
    version="1.0.0",
    author="downlifted",
    author_email="downlifted@gmail.com",
    description="Advanced GROQ API nodes for ComfyUI with text generation, vision analysis, document processing, code assistance, and audio processing capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/downlifted/ComfyUI_GROQ-PromptWizard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "groq>=0.4.1",
        "torch>=1.9.0",
        "numpy>=1.21.0",
        "Pillow>=8.0.0",
        "requests>=2.25.0",
    ],
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json"],
    },
)
