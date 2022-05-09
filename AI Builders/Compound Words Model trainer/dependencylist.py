from azureml.core.conda_dependencies import CondaDependencies

dependencies = CondaDependencies()
dependencies.set_python_version("3.9.12")
dependencies.add_pip_package("torch==1.11.0")
dependencies.add_pip_package("torchdata==0.3.0")
dependencies.add_pip_package("torchtext==0.12.0")
dependencies.add_pip_package("typing_extensions==4.2.0")
dependencies.save_to_file(".", "myenv.yml")