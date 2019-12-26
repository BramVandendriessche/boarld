from setuptools import setup, find_packages


setup(name='boarld',
      packages= find_packages(),
      version = '1.0',
      description='Framework for the ToThePoint Reinforcement Learning workshop',
      url='https://gitlab.com/tothepoint/reinforcement-learning-workshop/rl-gridworld',
      author='Bram Vandendriessche, Katrien Van Meulder',
      install_requires=['progressbar2'],
      # include_package_data=True,
      # package_data = {
      #     'facesmodule': ['*.mat', "*.txt"],
      #     }
      )