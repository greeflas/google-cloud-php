# Copyright 2018 Google LLC
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
    service='bigquerydatatransfer',
    version='v1',
    config_path='/google/cloud/bigquery/datatransfer/artman_bigquerydatatransfer.yaml',
    artman_output_name='google-cloud-bigquerydatatransfer-v1')

# copy all src including partial veneer classes
s.move(library / 'src')

# copy proto files to src also
s.move(library / 'proto/src/Google/Cloud/BigQuery/DataTransfer', 'src/')
s.move(library / 'tests/')

# copy GPBMetadata file to metadata
s.move(library / 'proto/src/GPBMetadata/Google/Cloud/Bigquery/Datatransfer', 'metadata/')

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
    '**/Gapic/*GapicClient.php',
    r'Copyright \d{4}',
    'Copyright 2017')
s.replace(
    '**/V1/DataTransferServiceClient.php',
    r'Copyright \d{4}',
    'Copyright 2017')
s.replace(
    'tests/**/V1/*Test.php',
    r'Copyright \d{4}',
    'Copyright 2018')

# Change the wording for the deprecation warning.
s.replace(
    'src/*/*_*.php',
    r'will be removed in the next major release',
    'will be removed in a future release')

s.replace(
    'src/V1/Gapic/DataTransferServiceGapicClient.php',
    r'ListTransferRunsRequest_RunAttempt',
    'ListTransferRunsRequest\RunAttempt')

# fix test group
s.replace(
    'tests/**/V1/*Test.php',
    r'@group datatransfer',
    '@group bigquerydatatransfer')
