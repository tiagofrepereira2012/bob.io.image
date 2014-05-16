#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Mon 16 Apr 08:18:08 2012 CEST

from setuptools import setup, find_packages, dist
dist.Distribution(dict(setup_requires=['xbob.blitz', 'xbob.io.base']))
from xbob.extension.utils import egrep, find_header, find_library
from xbob.blitz.extension import Extension
import xbob.io.base

include_dirs = [xbob.io.base.get_include()]

packages = ['bob-io >= 2.0.0a2', 'libtiff-4', 'libpng']
version = '2.0.0a0'

def libjpeg_version(header):

  version = egrep(header, r"#\s*define\s+JPEG_LIB_VERSION_(MINOR|MAJOR)\s+(\d+)")
  if not len(version): return None

  # we have a match, produce a string version of the version number
  major = int(version[0].group(2))
  minor = int(version[1].group(2))
  return '%d.%d' % (major, minor)

class jpeg:

  def __init__ (self, requirement='', only_static=False):
    """
    Searches for libjpeg in stock locations. Allows user to override.

    If the user sets the environment variable XBOB_PREFIX_PATH, that prefixes
    the standard path locations.

    Parameters:

    requirement, str
      A string, indicating a version requirement for this library. For example,
      ``'>= 8.2'``.

    only_static, boolean
      A flag, that indicates if we intend to link against the static library
      only. This will trigger our library search to disconsider shared
      libraries when searching.
    """

    self.name = 'libjpeg'
    header = 'jpeglib.h'

    candidates = find_header(header)

    if not candidates:
      raise RuntimeError("could not find %s's `%s' - have you installed %s on this machine?" % (self.name, header, self.name))

    found = False

    if not requirement:
      self.include_directory = os.path.dirname(candidates[0])
      self.version = libjpeg_version(candidates[0])
      found = True

    else:

      # requirement is 'operator' 'version'
      operator, required = [k.strip() for k in requirement.split(' ', 1)]

      # now check for user requirements
      for candidate in candidates:
        version = libjpeg_version(candidate)
        available = LooseVersion(version)
        if (operator == '<' and available < required) or \
           (operator == '<=' and available <= required) or \
           (operator == '>' and available > required) or \
           (operator == '>=' and available >= required) or \
           (operator == '==' and available == required):
          self.include_directory = os.path.dirname(candidate)
          self.version = version
          found = True
          break

    if not found:
      raise RuntimeError("could not find the required (%s) version of %s on the file system (looked at: %s)" % (requirement, self.name, ', '.join(candidates)))

    # normalize
    self.include_directory = os.path.normpath(self.include_directory)

    # find library
    prefix = os.path.dirname(os.path.dirname(self.include_directory))
    module = 'jpeg'
    candidates = find_library(module, version=self.version, prefixes=[prefix], only_static=only_static)

    if not candidates:
      raise RuntimeError("cannot find required %s binary module `%s' - make sure libsvm is installed on `%s'" % (self.name, module, prefix))

    # libraries
    self.libraries = []
    name, ext = os.path.splitext(os.path.basename(candidates[0]))
    if ext in ['.so', '.a', '.dylib', '.dll']:
      self.libraries.append(name[3:]) #strip 'lib' from the name
    else: #link against the whole thing
      self.libraries.append(':' + os.path.basename(candidates[0]))

    # library path
    self.library_directory = os.path.dirname(candidates[0])

  def macros(self):
    return [
        ('HAVE_%s' % self.name.upper(), '1'),
        ('%s_VERSION' % self.name.upper(), '"%s"' % self.version),
        ]

def libgif_version(header):

  version = egrep(header, r"#\s*define\s+GIFLIB_(RELEASE|MINOR|MAJOR)\s+(\d+)")
  if not len(version): return None

  # we have a match, produce a string version of the version number
  major = int(version[0].group(2))
  minor = int(version[1].group(2))
  release = int(version[2].group(2))
  return '%d.%d.%d' % (major, minor, release)

class gif:

  def __init__ (self, requirement='', only_static=False):
    """
    Searches for libgif in stock locations. Allows user to override.

    If the user sets the environment variable XBOB_PREFIX_PATH, that prefixes
    the standard path locations.

    Parameters:

    requirement, str
      A string, indicating a version requirement for this library. For example,
      ``'>= 8.2'``.

    only_static, boolean
      A flag, that indicates if we intend to link against the static library
      only. This will trigger our library search to disconsider shared
      libraries when searching.
    """

    self.name = 'giflib'
    header = 'gif_lib.h'

    candidates = find_header(header)

    if not candidates:
      raise RuntimeError("could not find %s's `%s' - have you installed %s on this machine?" % (self.name, header, self.name))

    found = False

    if not requirement:
      self.include_directory = os.path.dirname(candidates[0])
      self.version = libgif_version(candidates[0])
      found = True

    else:

      # requirement is 'operator' 'version'
      operator, required = [k.strip() for k in requirement.split(' ', 1)]

      # now check for user requirements
      for candidate in candidates:
        version = libgif_version(candidate)
        available = LooseVersion(version)
        if (operator == '<' and available < required) or \
           (operator == '<=' and available <= required) or \
           (operator == '>' and available > required) or \
           (operator == '>=' and available >= required) or \
           (operator == '==' and available == required):
          self.include_directory = os.path.dirname(candidate)
          self.version = version
          found = True
          break

    if not found:
      raise RuntimeError("could not find the required (%s) version of %s on the file system (looked at: %s)" % (requirement, self.name, ', '.join(candidates)))

    # normalize
    self.include_directory = os.path.normpath(self.include_directory)

    # find library
    prefix = os.path.dirname(os.path.dirname(self.include_directory))
    module = 'gif'
    candidates = find_library(module, version=self.version, prefixes=[prefix], only_static=only_static)

    if not candidates:
      raise RuntimeError("cannot find required %s binary module `%s' - make sure libsvm is installed on `%s'" % (self.name, module, prefix))

    # libraries
    self.libraries = []
    name, ext = os.path.splitext(os.path.basename(candidates[0]))
    if ext in ['.so', '.a', '.dylib', '.dll']:
      self.libraries.append(name[3:]) #strip 'lib' from the name
    else: #link against the whole thing
      self.libraries.append(':' + os.path.basename(candidates[0]))

    # library path
    self.library_directory = os.path.dirname(candidates[0])

  def macros(self):
    return [
        ('HAVE_%s' % self.name.upper(), '1'),
        ('%s_VERSION' % self.name.upper(), '"%s"' % self.version),
        ]

class netpbm:

  def __init__ (self, only_static=False):
    """
    Searches for netpbm in stock locations. Allows user to override.

    If the user sets the environment variable XBOB_PREFIX_PATH, that prefixes
    the standard path locations.

    Parameters:

    only_static, boolean
      A flag, that indicates if we intend to link against the static library
      only. This will trigger our library search to disconsider shared
      libraries when searching.
    """

    self.name = 'netpbm'
    header = 'pam.h'

    candidates = find_header(header, subpaths=[self.name])

    if not candidates:
      raise RuntimeError("could not find %s's `%s' - have you installed %s on this machine?" % (self.name, header, self.name))

    self.include_directory = os.path.dirname(candidates[0])
    found = True

    # normalize
    self.include_directory = os.path.normpath(self.include_directory)

    # find library
    prefix = os.path.dirname(os.path.dirname(self.include_directory))
    module = 'netpbm'
    candidates = find_library(module, prefixes=[prefix], only_static=only_static)

    if not candidates:
      raise RuntimeError("cannot find required %s binary module `%s' - make sure libsvm is installed on `%s'" % (self.name, module, prefix))

    # libraries
    self.libraries = []
    name, ext = os.path.splitext(os.path.basename(candidates[0]))
    if ext in ['.so', '.a', '.dylib', '.dll']:
      self.libraries.append(name[3:]) #strip 'lib' from the name
    else: #link against the whole thing
      self.libraries.append(':' + os.path.basename(candidates[0]))

    # library path
    self.library_directory = os.path.dirname(candidates[0])

  def macros(self):
    return [ ('HAVE_%s' % self.name.upper(), '1'), ]

jpeg_pkg = jpeg()
gif_pkg = gif()
netpbm_pkg = netpbm()

extra_compile_args = [
    '-isystem', jpeg_pkg.include_directory,
    '-isystem', gif_pkg.include_directory,
    '-isystem', netpbm_pkg.include_directory,
    ]

library_dirs = [
    jpeg_pkg.library_directory,
    gif_pkg.library_directory,
    netpbm_pkg.library_directory,
    ]

libraries = \
    jpeg_pkg.libraries + \
    gif_pkg.libraries + \
    netpbm_pkg.libraries

define_macros = \
    jpeg_pkg.macros() + \
    gif_pkg.macros() + \
    netpbm_pkg.macros()

setup(

    name='xbob.io.image',
    version=version,
    description='Image I/O support for Bob',
    url='http://github.com/bioidiap/xbob.io.image',
    license='BSD',
    author='Andre Anjos',
    author_email='andre.anjos@idiap.ch',

    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
      'setuptools',
      'xbob.blitz',
      'xbob.io.base',
    ],

    namespace_packages=[
      "xbob",
      "xbob.io",
      ],

    ext_modules = [
      Extension("xbob.io.image.version",
        [
          "xbob/io/image/version.cpp",
          ],
        packages = packages,
        include_dirs = include_dirs,
        version = version,
        extra_compile_args = extra_compile_args,
        library_dirs = library_dirs,
        libraries = libraries,
        define_macros = define_macros,
        ),
      Extension("xbob.io.image._library",
        [
          "xbob/io/image/tiff.cpp",
          "xbob/io/image/gif.cpp",
          "xbob/io/image/png.cpp",
          "xbob/io/image/jpeg.cpp",
          "xbob/io/image/bmp.cpp",
          "xbob/io/image/netpbm.cpp",
          "xbob/io/image/main.cpp",
          ],
        packages = packages,
        include_dirs = include_dirs,
        version = version,
        extra_compile_args = extra_compile_args,
        library_dirs = library_dirs,
        libraries = libraries,
        define_macros = define_macros,
        ),
      ],

    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Environment :: Plugins',
      ],

    )
