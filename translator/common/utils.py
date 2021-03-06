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


import logging
import math
import numbers
import re
from translator.toscalib.utils.gettextutils import _
import translator.toscalib.utils.yamlparser

YAML_ORDER_PARSER = translator.toscalib.utils.yamlparser.simple_ordered_parse
log = logging.getLogger('tosca')


class MemoryUnit(object):

    UNIT_SIZE_DEFAULT = 'B'
    UNIT_SIZE_DICT = {'B': 1, 'KB': 1000, 'KIB': 1024, 'MB': 1000000,
                      'MIB': 1048576, 'GB': 1000000000,
                      'GIB': 1073741824, 'TB': 1000000000000,
                      'TIB': 1099511627776}

    @staticmethod
    def convert_unit_size_to_num(size, unit=None):
        """Convert given size to a number representing given unit.
        If unit is None, convert to a number representing UNIT_SIZE_DEFAULT

        :param size: unit size e.g. 1 TB
        :param unit: unit to be converted to e.g GB
        :return: converted number e.g. 1000 for 1 TB size and unit GB
        """

        if unit:
            MemoryUnit.validate_unit(unit)
        else:
            unit = MemoryUnit.UNIT_SIZE_DEFAULT

        regex = re.compile('(\d*)\s*(\w*)')
        result = regex.match(str(size)).groups()
        if result[1]:
            MemoryUnit.validate_unit(result[1])
            converted = int(str_to_num(result[0])
                            * MemoryUnit.UNIT_SIZE_DICT[result[1].upper()]
                            * math.pow(MemoryUnit.UNIT_SIZE_DICT
                                       [unit.upper()], -1))
        else:
            converted = (str_to_num(result[0]))
        return converted

    @staticmethod
    def validate_unit(unit):
        if unit.upper() not in MemoryUnit.UNIT_SIZE_DICT.keys():
            msg = _('Provided unit "{0}" is not valid. The valid units are '
                    '{1}').format(unit, MemoryUnit.UNIT_SIZE_DICT.keys())
            raise ValueError(msg)


class CompareUtils(object):

    @staticmethod
    def compare_dicts(dict1, dict2):
        '''Returns False if not equal or any input parameter is empty.
           Returns True if both are equal.
        '''
        if not dict1 or not dict2:
            return False
        #compare generated and expected hot templates
        both_equal = True
        for generated_item, expected_item in zip(dict1.items(), dict2.items()):
            if generated_item != expected_item:
                log.warning("<Generated> : %s \n is not equal to "
                            "\n<Expected>: %s", generated_item,
                            expected_item)
                both_equal = False
                break
        return both_equal

    @staticmethod
    def compare_hot_yamls(generated_yaml, expected_yaml):
        hot_translated_dict = YAML_ORDER_PARSER(generated_yaml)
        hot_expected_dict = YAML_ORDER_PARSER(expected_yaml)
        return CompareUtils.compare_dicts(hot_translated_dict,
                                          hot_expected_dict)


def str_to_num(value):
    '''Convert a string representation of a number into a numeric type.'''
    if isinstance(value, numbers.Number):
        return value
    try:
        return int(value)
    except ValueError:
        return float(value)
