# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import os
# https://github.com/googleapis/artman/pull/655#issuecomment-507784277
os.environ["SYNTHTOOL_ARTMAN_VERSION"] = "0.29.1"
import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

library = gapic.php_library(
    service='securitycenter',
    version='v1',
    config_path=f'/google/cloud/securitycenter/artman_securitycenter_v1.yaml',
    artman_output_name=f'google-cloud-securitycenter-v1')

# copy all src
s.move(library / f'src/V1')

# copy proto files to src also
s.move(library / f'proto/src/Google/Cloud/SecurityCenter', f'src/')
s.move(library / f'tests/')

# copy GPBMetadata file to metadata
s.move(library / f'proto/src/GPBMetadata/Google/Cloud/SecurityCenter', f'metadata/')

# document and utilize apiEndpoint instead of serviceAddress
s.replace(
    "**/Gapic/*GapicClient.php",
    r"'serviceAddress' =>",
    r"'apiEndpoint' =>")
s.replace(
    "**/Gapic/*GapicClient.php",
    r"@type string \$serviceAddress\n\s+\*\s+The address",
    r"""@type string $serviceAddress
     *           **Deprecated**. This option will be removed in a future major release. Please
     *           utilize the `$apiEndpoint` option instead.
     *     @type string $apiEndpoint
     *           The address""")
s.replace(
    "**/Gapic/*GapicClient.php",
    r"\$transportConfig, and any \$serviceAddress",
    r"$transportConfig, and any `$apiEndpoint`")

# fix year
s.replace(
    'src/**/**/*.php',
    r'Copyright \d{4}',
    r'Copyright 2019')
s.replace(
    'tests/**/**/*Test.php',
    r'Copyright \d{4}',
    r'Copyright 2019')

# Use new namespace in the doc sample. See
# https://github.com/googleapis/gapic-generator/issues/2141
s.replace(
    'src/V1/Gapic/SecurityCenterGapicClient.php',
    r'Finding_State',
    r'Finding\\State')
# Change the wording for the deprecation warning.
s.replace(
    'src/*/*_*.php',
    r'will be removed in the next major release',
    'will be removed in a future release')
