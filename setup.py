#!/usr/bin/env python3

import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kcell-kubeflow-alerts",
    version='1.8',
    author="Rauan Akylzhanov",
    author_email="rauan.akylzhanov@kcell.kz",
    description="KCell Kubeflow Alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["kcell_kfp_alerts"],
)
