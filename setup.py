from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(name='portable_wisdom',
      version='0.1.1',
      description='Generate EPUB from Instapaper',
      long_description=readme,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities',
      ],
      url='https://github.com/jacobbudin/portable-wisdom',
      author='Jacob Budin',
      author_email='self@jacobbudin.com',
      license='MIT',
      install_requires=[
          'ebooklib>=0.17', # generates EPUB
          'pillow>=6.0', # downsizes images
          'requests>=2.21', # downloads images
          'beautifulsoup4>=4.7.1', # parses HTML for imags
          'html5lib>=1.0.1', # parses HTML for images
          'diskcache>=3.1.1', # caches article text and images
          'pyinstapaper>=0.2.2', # Instapaper API client
      ],
      packages=find_packages(),
      package_data={
          'portable_wisdom': ['styles/*.css'],
      },
      entry_points={
          'console_scripts': ['portable-wisdom=portable_wisdom.wisdom:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
