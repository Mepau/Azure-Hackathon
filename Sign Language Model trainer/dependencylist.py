from azureml.core.conda_dependencies import CondaDependencies

dependencies = CondaDependencies()
dependencies.set_python_version("3.8.5")
dependencies.add_pip_package("torch==1.10.2")

dependencies.save_to_file(".", "myenv.yml")