from setuptools import find_packages, setup

setup(
    name="write_seqs",
    version="0.0.1",
    author="Malcolm Sailor",
    author_email="malcolm.sailor@gmail.com",
    description="TODO",
    long_description="TODO",
    long_description_content_type="text/markdown",
    install_requires=["pandas", "pyyaml", "omegaconf", "dacite", "music_df"],
    url="TODO",
    project_urls={
        "Bug Tracker": "TODO",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
)
