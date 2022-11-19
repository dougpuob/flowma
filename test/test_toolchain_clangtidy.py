
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
from source.toolchain.clangtidy import clangtidy, clangtidy_assertion, clangtidy_assertion_parser

hellocmake_projroot = os.path.abspath(r'test/testdata/hello-cmake')
hellocmake_builddir = os.path.abspath(r'test/testdata/hello-cmake/build')

hellocmake_ccmdjson = os.path.join(hellocmake_builddir,
                                   'compile_commands.json')

hellocmake_binary = os.path.join(hellocmake_builddir,
                                 'hello_cmake')

hellocmake_msvcsln = os.path.join(hellocmake_builddir,
                                  'hello_cmake.sln')


def setup_module(module):
    if os.path.exists(hellocmake_builddir):
        shutil.rmtree(hellocmake_builddir)

    fmabld: flowma_build = flowma_build(build_system.ninja,
                                        build_compiler.clang,
                                        hellocmake_projroot,
                                        hellocmake_builddir)
    retrs: result = fmabld.probe()
    if 0 != retrs.errcode:
        pytest.skip("clang or cmake is unsupported with this system")
    else:
        retrs: result = fmabld.config()


def teardown_module(module):
    if os.path.exists(hellocmake_builddir):
        shutil.rmtree(hellocmake_builddir)


class test_clangtidy_assertion(unittest.TestCase):

    def test_assertion__misc_misplaced_const(self):
        stdout_rawtext = r"""
C:\workspace\dougpuob\flowma\flowma.git\test\testdata\hello-cmake\main.cpp:3:14: warning: parameter 'argc' is unused [misc-unused-parameters]
int main(int argc, char *argv[]) {
             ^~~~
              /*argc*/
C:\workspace\dougpuob\flowma\flowma.git\test\testdata\hello-cmake\main.cpp:3:26: warning: parameter 'argv' is unused [misc-unused-parameters]
int main(int argc, char *argv[]) {
                         ^~~~
                          /*argv*/
Suppressed 38921 warnings (38921 in non-user code).
"""
        parser = clangtidy_assertion_parser()
        found_list = parser.parse(stdout_rawtext)

        self.assertEqual(len(found_list), 2)

        # list[0]
        file_path = r'C:\workspace\dougpuob\flowma\flowma.git\test\testdata\hello-cmake\main.cpp'
        line_number = 3
        column_number = 14
        error_message = r"warning: parameter 'argc' is unused"
        error_identifier = r'[misc-unused-parameters]'

        self.assertEqual(found_list[0].file_path, file_path)
        self.assertEqual(found_list[0].line_number, line_number)
        self.assertEqual(found_list[0].column_number, column_number)
        self.assertEqual(found_list[0].error_message, error_message)
        self.assertEqual(found_list[0].error_identifier, error_identifier)
        self.assertEqual(len(found_list[0].failure_message), 3)

        # list[1]
        file_path = r'C:\workspace\dougpuob\flowma\flowma.git\test\testdata\hello-cmake\main.cpp'
        line_number = 3
        column_number = 26
        error_message = r"warning: parameter 'argv' is unused"
        error_identifier = r'[misc-unused-parameters]'

        self.assertEqual(found_list[1].file_path, file_path)
        self.assertEqual(found_list[1].line_number, line_number)
        self.assertEqual(found_list[1].column_number, column_number)
        self.assertEqual(found_list[1].error_message, error_message)
        self.assertEqual(found_list[1].error_identifier, error_identifier)
        self.assertEqual(len(found_list[1].failure_message), 4)


class test_clangtidy(unittest.TestCase):

    def test_clangtidy_v14_main_cpp(self):

        source_path = os.path.join(hellocmake_projroot, 'main.cpp')
        config_path = os.path.join(hellocmake_projroot, '_clang-tidy')
        compiler_database_path = os.path.join(hellocmake_builddir,
                                              'compile_commands.json')

        self.assertEqual(True, os.path.exists(source_path), source_path)
        self.assertEqual(True, os.path.exists(config_path), config_path)
        self.assertEqual(True, os.path.exists(compiler_database_path), compiler_database_path)

        obj_clang_tidy = clangtidy(config_path, compiler_database_path, version=14)
        retrs: result = obj_clang_tidy.run(source_path, config_path)
        if 0 != retrs.errcode:
            print("retrs.errcode={}".format(retrs.errcode))
            print("retrs.stdout={}".format(retrs.stdout))
            print("retrs.stderr={}".format(retrs.stderr))

        self.assertEqual(retrs.errcode, 0, retrs.stderr)
        self.assertEqual(retrs.errcode, 0, retrs.stdout)
        self.assertEqual(len(retrs.data), 2)


if __name__ == '__main__':
    unittest.main()
