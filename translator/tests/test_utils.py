#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import translator.common.utils
from translator.toscalib.tests.base import TestCase


class CommonUtilsTest(TestCase):

    MemoryUnit = translator.common.utils.MemoryUnit
    cmpUtils = translator.common.utils.CompareUtils

    def test_convert_unit_size_to_num(self):
        size = '1 TB'
        num_to_convert = 'GB'
        expected_output = 1000
        output = self.MemoryUnit.convert_unit_size_to_num(size, num_to_convert)
        self.assertEqual(output, expected_output)

        size = '40 GB'
        num_to_convert = 'MB'
        expected_output = 40000
        output = self.MemoryUnit.convert_unit_size_to_num(size, num_to_convert)
        self.assertEqual(output, expected_output)

        size = '20 B'
        num_to_convert = None
        expected_output = 20
        output = self.MemoryUnit.convert_unit_size_to_num(size, num_to_convert)
        self.assertEqual(output, expected_output)

    def test_validate_unit(self):
        unit = 'AB'
        exp_msg = ('Provided unit "{0}" is not valid. The valid units are '
                   '{1}').format(unit, self.MemoryUnit.UNIT_SIZE_DICT.keys())
        try:
            self.MemoryUnit.validate_unit(unit)
        except Exception as err:
            self.assertTrue(
                isinstance(err, ValueError))
            self.assertEqual(exp_msg, err.__str__())

    def test_str_to_num_value_error(self):
        str_to_convert = '55063.000000'
        expected_output = 55063.0
        output = translator.common.utils.str_to_num(str_to_convert)
        self.assertEquals(output, expected_output)

    def test_compare_dicts_unequal(self):
        dict1 = {'allowed_values': [1, 2, 4, 8],
                 'server3': {'depends_on': ['server1', 'server2']}}
        dict2 = {'allowed_values': [1, 2, 4, 8],
                 'server3': {'depends_on': ['server2', 'server1']}}
        self.assertFalse(self.cmpUtils.compare_dicts(dict1, dict2))

    def test_dicts_equivalent_empty_dicts(self):
        self.assertFalse(self.cmpUtils.compare_dicts(None, None))
        self.assertFalse(self.cmpUtils.compare_dicts(None, {}))
        self.assertFalse(self.cmpUtils.compare_dicts(None, {'x': '2'}))

    def test_assert_value_is_num(self):
        value = 1
        output = translator.common.utils.str_to_num(value)
        self.assertEqual(value, output)
