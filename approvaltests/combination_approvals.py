from itertools import product
from typing import Any, Callable, Optional, Tuple, Union, List, Sequence

from py.path import local

from approvaltests import (
    verify_with_namer,
    get_default_namer,
    Reporter,
    initialize_options,
    Options,
    verify, pairwise_combinations,
)
from approvaltests.core.namer import StackFrameNamer
from approvaltests.pairwise_combinations import get_best_covering_pairs
from approvaltests.reporters.testing_reporter import ReporterForTesting

VariationForEachParameter = Sequence[Sequence[Any]]
CombinationsOfParameters = Sequence[Sequence[Any]]


def calculate_total_size(input_arguments):
    from functools import reduce
    return reduce(lambda current_size, arguments: len(arguments) * current_size, input_arguments, 1)


def verify_best_covering_pairs(
        function_under_test: Callable,
        input_arguments: VariationForEachParameter,
        formatter: Optional[Callable] = None,
        reporter: Optional[ReporterForTesting] = None,
        *,  # enforce keyword arguments - https://www.python.org/dev/peps/pep-3102/
        options: Optional[Options] = None) -> None:
    count = 0

    def create_pairs(parameters):
        combinations = get_best_covering_pairs(parameters)
        nonlocal count
        count = len(combinations)
        return combinations

    text = print_combinations(formatter, function_under_test, input_arguments, create_pairs)
    options = initialize_options(options, reporter)
    total = calculate_total_size(input_arguments)

    header = f"Testing an optimized {count}/{total} scenarios:\n\n"
    verify(header + text, options=options)


def verify_all_combinations(
        function_under_test: Callable,
        input_arguments: VariationForEachParameter,
        formatter: Optional[Callable] = None,
        reporter: Optional[ReporterForTesting] = None,
        *,  # enforce keyword arguments - https://www.python.org/dev/peps/pep-3102/
        options: Optional[Options] = None
) -> None:
    """Run func with all possible combinations of args and verify outputs against the recorded approval file.

    Args:
        function_under_test (function): function under test.
        input_arguments: list of values to test for each input argument.  For example, a function f(product, quantity)
            could be tested with the input_arguments [['water', 'cola'], [1, 4]], which would result in outputs for the
            following calls being recorded and verified: f('water', 1), f('water', 4), f('cola', 1), f('cola', 4).
        formatter (function): function for formatting the function inputs/outputs before they are recorded to an
            approval file for comparison.
        reporter (approvaltests.reporter.Reporter): an approval reporter.

    Raises:
        ApprovalException: if the results to not match the approved results.
    """
    options = initialize_options(options, reporter)
    verify_all_combinations_with_namer(
        function_under_test, input_arguments, formatter, None, options=options
    )


def verify_all_combinations_with_namer(
        function_under_test: Callable,
        input_arguments: VariationForEachParameter,
        formatter: Optional[Callable] = None,
        reporter: Optional[Reporter] = None,
        *,  # enforce keyword arguments - https://www.python.org/dev/peps/pep-3102/
        options: Optional[Options] = None
) -> None:
    """Run func with all possible combinations of args and verify outputs against the recorded approval file.

    Args:
        function_under_test (function): function under test.
        input_arguments: list of values to test for each input argument.  For example, a function f(product, quantity)
            could be tested with the input_arguments [['water', 'cola'], [1, 4]], which would result in outputs for the
            following calls being recorded and verified: f('water', 1), f('water', 4), f('cola', 1), f('cola', 4).
        namer (approvaltests.Namer): A namer that defines the name of received and approved files.
        formatter (function): function for formatting the function inputs/outputs before they are recorded to an
            approval file for comparison.
        reporter (approvaltests.reporter.Reporter): an approval reporter.

    Raises:
        ApprovalException: if the results to not match the approved results.
    """
    text = print_combinations(formatter, function_under_test, input_arguments, lambda i: product(*i))
    options = initialize_options(options, reporter)
    verify(text, options=options)


def print_combinations(
        formatter: Optional[Callable],
        function_under_test: Callable,
        input_arguments: VariationForEachParameter,
        combiner: Callable[[VariationForEachParameter], CombinationsOfParameters]
) -> str:
    if formatter is None:
        formatter = args_and_result_formatter
    approval_strings = []
    for args in combiner(input_arguments):
        try:
            result = function_under_test(*args)
        except Exception as e:
            result = e
        approval_strings.append(formatter(args, result))
    return "".join(approval_strings)


def args_and_result_formatter(args: List[Any], result: int) -> str:
    return "args: {} => {}\n".format(repr(args), repr(result))
