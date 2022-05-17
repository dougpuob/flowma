
import sys
import os
import shutil
import pytest
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)


from source.lib.execute import process, result
from source.lib.define import build_compiler, build_system, os_helper, os_kind
from source.flow.build import flowma_build


class test_flowma_build(unittest.TestCase):

    proc: process = process()
    hellocmake_projroot = os.path.abspath(r'test/testdata/hello-cmake')
    hellocmake_builddir = os.path.abspath(r'test/testdata/hello-cmake/build')
    hellocmake_ccmdjson = os.path.join(hellocmake_builddir,
                                       'compile_commands.json')
    hellocmake_binary = os.path.join(hellocmake_builddir, 'hello_cmake')
    hellocmake_msvcsln = os.path.join(hellocmake_builddir,
                                      'hello_cmake.sln')

    def setup_method(self, test_method):
        if os.path.exists(self.hellocmake_builddir):
            shutil.rmtree(self.hellocmake_builddir)

    def teardown_method(self, test_method):
        if os.path.exists(self.hellocmake_builddir):
            shutil.rmtree(self.hellocmake_builddir)

    def test_ninja_clang(self):
        fmabld: flowma_build = flowma_build(build_system.ninja,
                                            build_compiler.clang,
                                            self.hellocmake_projroot,
                                            self.hellocmake_builddir)
        retrs: result = fmabld.probe()
        if 0 != retrs.errcode:
            pytest.skip("clang or cmake is unsupported with this system")
        else:
            retrs: result = fmabld.config()
            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            if 0 == retrs.errcode:
                retrs: result = fmabld.build()
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertTrue(os.path.exists(self.hellocmake_ccmdjson),
                                self.hellocmake_ccmdjson)

            retrs: result = self.proc.exec(self.hellocmake_binary)
            if 0 == retrs.errcode:
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertEqual("".join(retrs.stdout), 'Hello CMake!')

    def test_ninja_gcc(self):
        fmabld: flowma_build = flowma_build(build_system.ninja,
                                            build_compiler.gcc,
                                            self.hellocmake_projroot,
                                            self.hellocmake_builddir)
        retrs: result = fmabld.probe()
        if 0 != retrs.errcode:
            pytest.skip("gcc or cmake is unsupported with this system")
        else:
            retrs: result = fmabld.config()
            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            if 0 == retrs.errcode:
                retrs: result = fmabld.build()
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertTrue(os.path.exists(self.hellocmake_ccmdjson),
                                self.hellocmake_ccmdjson)

            retrs: result = self.proc.exec(self.hellocmake_binary)
            if 0 == retrs.errcode:
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertEqual("".join(retrs.stdout), 'Hello CMake!')

    def test_ninja_msvc(self):
        fmabld: flowma_build = flowma_build(build_system.ninja,
                                            build_compiler.msvc,
                                            self.hellocmake_projroot,
                                            self.hellocmake_builddir)
        retrs: result = fmabld.probe()
        if 0 != retrs.errcode:
            pytest.skip("msvc is unsupported with this system")
        else:
            retrs: result = fmabld.config()
            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            if 0 == retrs.errcode:
                retrs: result = fmabld.build()
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertTrue(os.path.exists(self.hellocmake_ccmdjson),
                                self.hellocmake_ccmdjson)

            retrs: result = self.proc.exec(self.hellocmake_binary)
            if 0 == retrs.errcode:
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertEqual("".join(retrs.stdout), 'Hello CMake!')

    def test_msbuild_msvc(self):
        fmabld: flowma_build = flowma_build(build_system.msbuild,
                                            build_compiler.msvc,
                                            self.hellocmake_projroot,
                                            self.hellocmake_builddir)
        retrs: result = fmabld.probe()
        if 0 != retrs.errcode:
            pytest.skip("msvc is unsupported with this system")
        else:
            retrs: result = fmabld.config()
            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            if 0 == retrs.errcode:
                retrs: result = fmabld.build()
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertFalse(os.path.exists(self.hellocmake_ccmdjson),
                                 self.hellocmake_ccmdjson)
                self.assertTrue(os.path.exists(self.hellocmake_msvcsln),
                                self.hellocmake_msvcsln)

            retrs: result = self.proc.exec(self.hellocmake_binary)
            if 0 == retrs.errcode:
                self.assertEqual(retrs.errcode, 0, retrs.stderr)
                self.assertEqual("".join(retrs.stdout), 'Hello CMake!')


if __name__ == '__main__':
    unittest.main()
