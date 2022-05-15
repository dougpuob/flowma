import unittest
import sys
import os
import shutil


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)


from source.lib.execute import process, result
from source.lib.define import os_helper, os_kind
from source.toolchain.msbuild import msbuild, msvc_information


class test_msbuild(unittest.TestCase):

    hellocamke_projroot = os.path.abspath(r'test/testdata/hello-cmake')
    hellocamke_builddir = os.path.abspath(r'test/testdata/hello-cmake/build')

    def setup_method(self, test_method):
        if os.path.exists(self.hellocamke_builddir):
            shutil.rmtree(self.hellocamke_builddir)

    def teardown_method(self, test_method):
        if os.path.exists(self.hellocamke_builddir):
            shutil.rmtree(self.hellocamke_builddir)

    def test_basic(self):
        if os_helper().get_oskind().value == os_kind.windows.value:
            msbld: msbuild = msbuild()
            self.assertEqual(len(msbld.msvc_info_list) > 0, True)

            for msvc_info in msbld.msvc_info_list:
                msvc_info: msvc_information = msvc_info
                self.assertEqual(len(msvc_info.vcvars_files) > 0, True)

    def test_build_hellocmake(self):
        self.assertEqual(os.path.exists(self.hellocamke_builddir), False)

        proc: process = process()

        vcvars_env = None
        output = os.path.join(self.hellocamke_builddir,
                              'hello_cmake')

        if os_helper().get_oskind().value == os_kind.windows.value:
            msbld: msbuild = msbuild()
            supported_msvc_list = msbld.get_supported()
            self.assertEqual(len(supported_msvc_list) > 0, True)

            msvc_info = supported_msvc_list[0]
            vcvars_env = msbld.dump_vcvars(msvc_info.edition,
                                           msvc_info.version)
            output += '.exe'

        retrs: result = proc.run('cmake',
                                 ['-G', 'Ninja',
                                  '-B', self.hellocamke_builddir],
                                 workdir=self.hellocamke_projroot,
                                 env=vcvars_env)
        self.assertEqual(retrs.errcode, 0)

        retrs: result = proc.run('cmake',
                                 ['--build', self.hellocamke_builddir],
                                 workdir=self.hellocamke_projroot,
                                 env=vcvars_env)
        self.assertEqual(retrs.errcode, 0)
        self.assertEqual(os.path.exists(output), True)

        retrs: result = proc.run(output)
        self.assertEqual(retrs.errcode, 0)
        self.assertEqual("".join(retrs.stdout), 'Hello CMake!')


if __name__ == '__main__':
    unittest.main()
