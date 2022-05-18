
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
from source.flow.lint import flowma_lint


class test_flowma_lint(unittest.TestCase):

    hellocmake_projroot = os.path.abspath(r'test/testdata/hello-cmake')
    hellocmake_builddir = os.path.abspath(r'test/testdata/hello-cmake/build')
    hellocmake_ccmdjson = os.path.join(hellocmake_builddir,
                                       'compile_commands.json')
    hellocmake_binary = os.path.join(hellocmake_builddir, 'hello_cmake')
    hellocmake_msvcsln = os.path.join(hellocmake_builddir,
                                      'hello_cmake.sln')
    hellocmake_src_cpp = os.path.join(hellocmake_projroot,
                                      'main.cpp')

    def setup_method(self, test_method):
        if os.path.exists(self.hellocmake_builddir):
            shutil.rmtree(self.hellocmake_builddir)

    def teardown_method(self, test_method):
        if os.path.exists(self.hellocmake_builddir):
            shutil.rmtree(self.hellocmake_builddir)

    def test_lint_clangfmt_ninja_clang(self):
        fmabld: flowma_build = flowma_build(build_system.ninja,
                                            build_compiler.clang,
                                            self.hellocmake_projroot,
                                            self.hellocmake_builddir)
        fmalint: flowma_lint = flowma_lint()

        retrs_bld: result = fmabld.probe()
        retrs_lint: result = fmalint.probe()
        if 0 != retrs_bld.errcode:
            pytest.skip("clang or cmake is unsupported with this system")
        elif 0 != retrs_lint.errcode:
            pytest.skip("clang-format is unsupported with this system")
        else:
            retrs: result = fmabld.config()
            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            if 0 == retrs.errcode:
                retrs: result = fmalint.clangformat(self.hellocmake_src_cpp)
                self.assertEqual(retrs.errcode, 0, retrs.stderr)


if __name__ == '__main__':
    unittest.main()
