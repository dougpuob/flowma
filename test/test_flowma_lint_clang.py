
import sys
import os
import shutil
import os.path
import pytest
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)


from source.lib.execute import process, result
from source.lib.define import build_compiler, build_system, os_helper, os_kind
from source.flow.build import flowma_build
from source.flow.lint import flowma_lint, lint_config


hellocmake_projroot = os.path.abspath(r'test/testdata/hello-cmake')
hellocmake_builddir = os.path.abspath(r'test/testdata/hello-cmake/build')

hellocmake_ccmdjson = os.path.join(hellocmake_builddir,
                                   'compile_commands.json')

hellocmake_binary = os.path.join(hellocmake_builddir,
                                 'hello_cmake')

hellocmake_msvcsln = os.path.join(hellocmake_builddir,
                                  'hello_cmake.sln')

hellocmake_src_cpp = os.path.join(hellocmake_projroot,
                                  'main.cpp')

hellocmake_cfgftm = os.path.join(hellocmake_builddir, '_clang-format')
hellocmake_cfgtidy = os.path.join(hellocmake_builddir, '_clang-tidy')


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


class test_flowma_lint_clang(unittest.TestCase):

    def test_lint_clangfmt_ninja_v14(self):

        lint_cfg: lint_config = lint_config()
        lint_cfg.llvm.specific_version = 14
        lint_cfg.llvm.compile_commands = hellocmake_ccmdjson

        cfgfmt: str = os.path.join(hellocmake_projroot,
                                   'config',
                                   str(lint_cfg.llvm.specific_version),
                                   '_clang-format_llvm')
        lint_cfg.llvm.config.clangformat = cfgfmt

        cfgtidy: str = os.path.join(hellocmake_projroot,
                                    'config',
                                    str(lint_cfg.llvm.specific_version),
                                    '_clang-tidy')
        lint_cfg.llvm.config.clangtidy = cfgtidy

        self.assertEqual(True, os.path.exists(lint_cfg.llvm.config.clangformat))
        self.assertEqual(True, os.path.exists(lint_cfg.llvm.config.clangtidy))

        retrs: result = None
        obj_flowma_lint: flowma_lint = flowma_lint(lint_cfg)
        if obj_flowma_lint.check_version():
            retrs = obj_flowma_lint.clangformat(hellocmake_src_cpp)
            self.assertEqual(True, isinstance(retrs, result))

            if 0 != retrs.errcode:
                print("retrs.errcode={}".format(retrs.errcode))
                print("retrs.stdout={}".format(retrs.stdout))
                print("retrs.stderr={}".format(retrs.stderr))

            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            self.assertEqual(retrs.errcode, 0, "retrs.stderr={}".format(retrs.stderr))
        else:
            pytest.skip("clang-format is unsupported with this system")

    def test_lint_clangfmt_ninja_v15(self):

        lint_cfg: lint_config = lint_config()
        lint_cfg.llvm.specific_version = 15
        lint_cfg.llvm.compile_commands = hellocmake_ccmdjson

        cfgfmt: str = os.path.join(hellocmake_projroot,
                                   'config',
                                   str(lint_cfg.llvm.specific_version),
                                   '_clang-format_llvm')
        lint_cfg.llvm.config.clangformat = cfgfmt

        cfgtidy: str = os.path.join(hellocmake_projroot,
                                    'config',
                                    str(lint_cfg.llvm.specific_version),
                                    '_clang-tidy')
        lint_cfg.llvm.config.clangtidy = cfgtidy

        self.assertEqual(True, os.path.exists(lint_cfg.llvm.config.clangformat))
        self.assertEqual(True, os.path.exists(lint_cfg.llvm.config.clangtidy))

        retrs: result = None
        obj_flowma_lint: flowma_lint = flowma_lint(lint_cfg)
        if obj_flowma_lint.check_version():
            retrs = obj_flowma_lint.clangformat(hellocmake_src_cpp)
            self.assertEqual(True, isinstance(retrs, result))

            if 0 != retrs.errcode:
                print("retrs.errcode={}".format(retrs.errcode))
                print("retrs.stdout={}".format(retrs.stdout))
                print("retrs.stderr={}".format(retrs.stderr))

            self.assertEqual(retrs.errcode, 0, retrs.stderr)
            self.assertEqual(retrs.errcode, 0, "retrs.stderr={}".format(retrs.stderr))
        else:
            pytest.skip("clang utilities are unsupported with this system")


if __name__ == '__main__':
    unittest.main()
