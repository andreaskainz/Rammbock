#  Copyright 2022 Andreas Kainz
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys


def parse_bool(value):
    if value in ('None', '', None):
        return None
    if value in (True, False):
        return value
    if value.isdigit():
        value = int(value)
    if type(value) == int:
        return value != 0
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    return value


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
