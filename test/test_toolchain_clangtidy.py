
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

    def test_test_clangtidy_main_cpp(self):

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

        source_path = os.path.join(self.hellocmake_projroot, 'main.cpp')
        config_path = os.path.join(self.hellocmake_projroot, '_clang-tidy')
        compiler_database_path = os.path.join(self.hellocmake_builddir, 'compile_commands.json')
        tidy = clangtidy(config_path,
                         compiler_database_path)
        retrs: result = tidy.run(source_path, config_path)
        self.assertEqual(retrs.errcode, 0)


if __name__ == '__main__':
    unittest.main()
