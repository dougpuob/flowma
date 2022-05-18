
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
from source.toolchain.clangtidy import clangtidy, clangtidy_assertion


class test_clangtidy_assertion(unittest.TestCase):

    def test_assertion__misc_misplaced_const(self):
        assertion_message_block = r"D:\workspace\gli\glisdk\baseio\devutil.git\Source\Device\OsdpImp\DeviceManager_Windows.cpp:76:57: warning: 'pDevIfData' declared with a const-qualified typedef; results in the type being '_SP_DEVICE_INTERFACE_DATA *const' instead of 'const _SP_DEVICE_INTERFACE_DATA *' [misc-misplaced-const]"

        faliure_message = """
                        const PSP_DEVICE_INTERFACE_DATA pDevIfData,
                                                        ^"""
        assertion = clangtidy_assertion(assertion_message_block,
                                        faliure_message)

        file_path = r'D:\workspace\gli\glisdk\baseio\devutil.git\Source\Device\OsdpImp\DeviceManager_Windows.cpp'

        error_message = r"warning: 'pDevIfData' declared with a const-qualified typedef; results in the type being '_SP_DEVICE_INTERFACE_DATA *const' instead of 'const _SP_DEVICE_INTERFACE_DATA *'"

        error_identifier = '[misc-misplaced-const]'

        self.assertEqual(assertion.raw_text, assertion_message_block)
        self.assertEqual(assertion.file_path, file_path)
        self.assertEqual(assertion.line_number, 76)
        self.assertEqual(assertion.column_number, 57)
        self.assertEqual(assertion.error_message, error_message)
        self.assertEqual(assertion.error_identifier, error_identifier)
        self.assertEqual(assertion.failure_message, faliure_message)


if __name__ == '__main__':
    unittest.main()
