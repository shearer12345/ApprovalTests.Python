# ApprovalTests.Python


<!-- toc -->
## Contents

  * [What can I use ApprovalTests for?](#what-can-i-use-approvaltests-for)
  * [Getting Started](#getting-started)
    * [New Projects](#new-projects)
    * [Adding to Existing Projects](#adding-to-existing-projects)
  * [Overview](#overview)
    * [Example using pytest](#example-using-pytest)
    * [Example using unittest](#example-using-unittest)
  * [Reporters](#reporters)
    * [Selecting a Reporter](#selecting-a-reporter)
    * [JSON file for collection of reporters](#json-file-for-collection-of-reporters)
  * [Support and Documentation](#support-and-documentation)
    * [Dependencies](#dependencies)
  * [For developers](#for-developers)
    * [Weekly Ensemble](#weekly-ensemble)
    * [Pull Requests](#pull-requests)<!-- endToc -->

Capturing Human Intelligence - ApprovalTests is an open source assertion/verification library to aid testing.  
`approvaltests` is the ApprovalTests port for Python.

For more information see: [www.approvaltests.com](http://approvaltests.com/).

[![PyPI version](https://img.shields.io/pypi/v/approvaltests.svg)](https://pypi.org/project/approvaltests)
[![Python versions](https://img.shields.io/pypi/pyversions/approvaltests.svg)](https://pypi.org/project/approvaltests)
[![Build Status](https://github.com/approvals/ApprovalTests.Python/workflows/Test/badge.svg?branch=master)](https://github.com/approvals/ApprovalTests.Python/actions)
[![Build Status](https://github.com/approvals/ApprovalTests.Python/workflows/on-push-do-doco/badge.svg)](https://github.com/approvals/ApprovalTests.Python/actions?query=workflow%3Aon-push-do-doco)
[![Build Status](https://github.com/approvals/ApprovalTests.Python/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/approvals/ApprovalTests.Python/actions?query=workflow%3A%22Upload+Python+Package%22)


## What can I use ApprovalTests for?

You can use ApprovalTests to verify objects that require more than a simple assert including long strings, large arrays, 
and complex hash structures and objects.  ApprovalTests really shines when you need a more granular look at the test 
failure.  Sometimes, trying to find a small difference in a long string printed to STDOUT is just too hard!  
ApprovalTests solves this problem by providing reporters which let you view the test results in one of many popular diff 
utilities.


## Getting Started

### New Projects

If you are starting a new project, we suggest you use the [Starter Project](https://github.com/approvals/ApprovalTests.Python.StarterProject).
You can just clone this and go. It's great for exercises, katas, and green field projects.

###  Adding to Existing Projects 

From [pypi](https://pypi.org/project/approvaltests/):

	pip install approvaltests

## Overview

Approvals work by comparing the test results to a golden master.  If no golden master exists you can create a snapshot 
of the current test results and use that as the golden master.  The reporter helps you manage the golden master.  
Whenever your current results differ from the golden master, Approvals will launch an external application for you to 
examine the differences.  Either you will update the master because you expected the changes and they are good,
or you will go back to your code and update or roll back your changes to get your results back in line with the 
golden master.


### Example using pytest

<!-- snippet: getting_started_with_pytest.py -->
<a id='snippet-getting_started_with_pytest.py'></a>
```py
from approvaltests.approvals import verify


def test_simple():
    result = "Hello ApprovalTests"
    verify(result)
```
<sup><a href='/tests/examples/getting_started_with_pytest.py#L1-L6' title='Snippet source file'>snippet source</a> | <a href='#snippet-getting_started_with_pytest.py' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->

Install the plugin pytest-approvaltests and use it to select a reporter:

    pip install pytest-approvaltests
    pytest --approvaltests-use-reporter='PythonNative'

The reporter is used both to alert you to changes in your test output, and to provide a tool to update the golden 
master. In this snippet, we chose the 'PythonNative' reporter when we ran the tests. For more information about selecting
reporters see [the documentation](https://github.com/approvals/ApprovalTests.Python.PytestPlugin)


### Example using unittest

<!-- snippet: getting_started_with_unittest.py -->
<a id='snippet-getting_started_with_unittest.py'></a>
```py
import unittest

from approvaltests.approvals import verify


class GettingStartedTest(unittest.TestCase):
    def test_simple(self):
        verify("Hello ApprovalTests")


if __name__ == "__main__":
    unittest.main()
```
<sup><a href='/tests/examples/getting_started_with_unittest.py#L1-L12' title='Snippet source file'>snippet source</a> | <a href='#snippet-getting_started_with_unittest.py' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->

This example has the same behaviour as the pytest version, but uses the built-in test framework `unittest` instead.


## Reporters

### Selecting a Reporter

All verify functions take an optional `options` parameter that can configure reporters (as well as many other aspects).

ApprovalTests.Python comes with a few reporters configured, supporting Linux, Mac OSX, and Windows.

In the example shown below, we pass in an options with a reporter we're selecting directly:

<!-- snippet: select_reporter_from_class -->
<a id='snippet-select_reporter_from_class'></a>
```py
class TestSelectReporterFromClass(unittest.TestCase):
    def test_simple(self):
        verify("Hello", options=Options().with_reporter(report_with_beyond_compare()))
```
<sup><a href='/tests/samples/test_getting_started.py#L24-L30' title='Snippet source file'>snippet source</a> | <a href='#snippet-select_reporter_from_class' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->

You can also use the `GenericDiffReporterFactory` to find and select the first diff utility that exists on our system.

An advantage of this method is you can modify the reporters.json file directly to handle your unique system.

<!-- snippet: select_reporter_from_factory -->
<a id='snippet-select_reporter_from_factory'></a>
```py
class TestSelectReporter(unittest.TestCase):
    def setUp(self):
        self.factory = GenericDiffReporterFactory()

    def test_simple(self):
        verify(
            "Hello", options=Options().with_reporter(self.factory.get("BeyondCompare"))
        )
```
<sup><a href='/tests/samples/test_getting_started.py#L11-L22' title='Snippet source file'>snippet source</a> | <a href='#snippet-select_reporter_from_factory' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->



Or you can build your own GenericDiffReporter on the fly

<!-- snippet: custom_generic_diff_reporter -->
<a id='snippet-custom_generic_diff_reporter'></a>
```py
class GettingStartedTest(unittest.TestCase):
    def test_simple(self):
        verify(
            "Hello",
            options=Options().with_reporter(
                GenericDiffReporter.create(r"C:\my\favorite\diff\utility.exe")
            ),
        )
```
<sup><a href='/tests/samples/test_getting_started.py#L32-L43' title='Snippet source file'>snippet source</a> | <a href='#snippet-custom_generic_diff_reporter' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->

As long as `C:/my/favorite/diff/utility.exe` can be invoked from the command line using the format `utility.exe file1 file2` 
then it will be compatible with GenericDiffReporter.  Otherwise you will have to derive your own reporter, which 
we won't cover here.

### JSON file for collection of reporters

To wrap things up, I should note that you can completely replace the collection of reporters known to the reporter 
factory by writing your own JSON file and loading it.

For example if you had `C:/myreporters.json`

```json
[
    [
        "BeyondCompare4",
        "C:/Program Files (x86)/Beyond Compare 4/BCompare.exe"
    ],
    [
        "WinMerge",
        "C:/Program Files (x86)/WinMerge/WinMergeU.exe"
    ],
    [
        "Tortoise",
        "C:/Program Files (x86)/TortoiseSVN/bin/tortoisemerge.exe"
    ]
]
```

You could then use that file by loading it into the factory:

```python

import unittest

from approvaltests.approvals import verify
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory


class GettingStartedTest(unittest.TestCase):
    def setUp(self):
        factory = GenericDiffReporterFactory()
        factory.load('C:/myreporters.json')
        self.reporter = factory.get_first_working()

    def test_simple(self):
        verify('Hello', self.reporter)

if __name__ == "__main__":
    unittest.main()
```

Of course, if you have some interesting new reporters in `myreporters.json` then please consider updating the 
`reporters.json` file that ships with Approvals and submitting a pull request.

## Support and Documentation

* [Documentation](/docs/README.md)

* GitHub: [https://github.com/approvals/ApprovalTests.Python](https://github.com/approvals/ApprovalTests.Python)

* ApprovalTests Homepage: [http://www.approvaltests.com](http://www.approvaltests.com)

### Dependencies

ApprovalTests require Python 3.6 or greater and the following dependencies:
#### Required dependencies
These dependencies are always required for approvaltests
<!-- snippet: requirements.prod.required.txt -->
<a id='snippet-requirements.prod.txt'></a>
```txt
-r requirements.prod.required.txt
-r requirements.prod.extras.txt
```
<sup><a href='/requirements.prod.txt#L1-L2' title='Snippet source file'>snippet source</a> | <a href='#snippet-requirements.prod.txt' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->
#### Extra dependencies
These dependencies are required if you are going to use the related functionality
If you want the bare minimum you can use the pypi project 
[approvaltests-minimal](https://pypi.org/project/approvaltests-minimal/) 
<!-- snippet: requirements.prod.extras.txt -->

## For developers
### Weekly Ensemble

The best way to contribute is to [join our weekly mob/ensemble](./docs/Contribute.md)

### Pull Requests
Pull requests are welcomed, particularly those accompanied by automated tests.

To run the self-tests, install pytest and tox, then execute

    python -m tox

This will run the self-tests on several python versions. We support python 3.6 and above. 

All pull requests will be pre-checked using GitHub actions to execute all these tests. You can see the [results of test
runs here](https://github.com/approvals/ApprovalTests.Python/actions).
