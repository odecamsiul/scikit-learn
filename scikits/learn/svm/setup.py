from os.path import join
import numpy
from ConfigParser import ConfigParser
import warnings

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.system_info import get_info, get_standard_file, \
         BlasNotFoundError

    config = Configuration('svm', parent_package, top_path)

    config.add_subpackage('tests')
    config.add_subpackage('sparse')

    # Section LibSVM
    libsvm_includes = [numpy.get_include()]
    libsvm_sources = [join('src', 'libsvm', '_libsvm.c'),
                      join('src', 'libsvm', 'svm.cpp')]
    libsvm_depends = [join('src', 'libsvm', 'svm.h'),
                      join('src', 'libsvm', 'libsvm_helper.c')]

    config.add_extension('_libsvm',
                         sources=libsvm_sources,
                         define_macros=[('_DENSE_REP', 1)],
                         include_dirs=libsvm_includes,
                         depends=libsvm_depends,
                         )

    ### liblinear module
    blas_sources = [join('src', 'blas', 'daxpy.c'),
                    join('src', 'blas', 'ddot.c'),
                    join('src', 'blas', 'dnrm2.c'),
                    join('src', 'blas', 'dscal.c')]

    liblinear_sources = [join('src', 'liblinear', '_liblinear.c'),
                         join('src', 'liblinear', '*.cpp')]

    liblinear_depends = [join('src', 'liblinear', '*.h'),
                         join('src', 'liblinear', 'liblinear_helper.c')]

    # we try to link agains system-wide blas
    blas_info = get_info('blas_opt', 0)

    if not blas_info:
        config.add_library('blas', blas_sources)
        warnings.warn(BlasNotFoundError.__doc__)

    config.add_extension('_liblinear',
                         sources=liblinear_sources,
                         libraries = blas_info.pop('libraries', ['blas']),
                         include_dirs=['src',
                                       numpy.get_include(),
                                       blas_info.pop('include_dirs', [])],
                         depends=liblinear_depends,
                         **blas_info)

    ## end liblinear module

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

