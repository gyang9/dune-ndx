##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import sys


class Root(Package):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url      = "https://root.cern.ch/download/root_v6.07.02.source.tar.gz"

    version('6.08.02', '50c4dbb8aa81124aa58524e776fd4b4b')
    version('6.06.06', '4308449892210c8d36e36924261fea26')
    version('6.06.04', '55a2f98dd4cea79c9c4e32407c2d6d17')
    version('6.06.02', 'e9b8b86838f65b0a78d8d02c66c2ec55')
    version('5.34.36', '6a1ad549b3b79b10bbb1f116b49067ee')
    
    if sys.platform == 'darwin':
        patch('math_uint.patch', when='@6.06.02')
        patch('root6-60606-mathmore.patch', when='@6.06.06')

    variant('graphviz', default=False, description='Enable graphviz support')
    variant('gdml', default=True, description='Enable GDML support')
    variant('pythia8', default=False, description='Enable pythia8 support')
    variant('debug', default=False, description='Enable debugging support')
    
    depends_on("cmake", type='build')
    depends_on("pcre")
    depends_on("fftw")
    depends_on("graphviz", when="+graphviz")
    depends_on("python")
    depends_on("gsl")
    depends_on("libxml2")
    depends_on("jpeg")

    if sys.platform != 'darwin':
        depends_on("libpng")
        depends_on("openssl")
        depends_on("freetype")

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        options = [source_directory]
        if '+debug' in spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')
        if 'root@5' in spec:
            print "using cxx98"
            options.append('-DCMAKE_CXX_STANDARD=98')
            options.append('-Dcxx14=off')
        else:
            options.append('-Dcxx14=on')
        options.append('-Dcocoa=off')
        options.append('-Dbonjour=off')
        options.append('-Dx11=on')
        if '+gdml' in spec: options.append('-Dgdml=on')
        else: options.append('-Dgdml=off')
        if '+pythia8' in spec: options.append('-Dpythia8=on')
        else: options.append('-Dpythia8=off')
        options.extend(std_cmake_args)
        if sys.platform == 'darwin':
            darwin_options = [
                '-Dcastor=OFF',
                '-Drfio=OFF',
                '-Ddcache=OFF']
            options.extend(darwin_options)
        with working_dir(build_directory, create=True):
            cmake(*options)
            make()
            make("install")

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('ROOTSYS', self.prefix)
        spack_env.set('ROOT_VERSION', 'v6')
        spack_env.prepend_path('PYTHONPATH', self.prefix.lib)

    def url_for_version(self, version):
        """Handle ROOT's unusual version string."""
        return "https://root.cern.ch/download/root_v%s.source.tar.gz" % version
