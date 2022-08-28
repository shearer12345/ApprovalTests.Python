from approvaltests import Options, verify, Reporter
from approvaltests.reporters import (
    ReportWithBeyondCompare,
    GenericDiffReporter,
    GenericDiffReporterConfig,
    create_config,
)


class ReportWithGitDiff(Reporter):
    def report(self, received_path: str, approved_path: str) -> bool:
        # call `git diff` on these paths
        #   def __init__(self, name: str, path: str, extra_args: Optional[List[str]] = None):
        return GenericDiffReporter(
            GenericDiffReporterConfig(
                name="gitdiff",
                path="c:/program files/git/usr/bin/diff.exe",
                extra_args=["--color", "-u"],
            )
        ).report(received_path, approved_path)


def test_something():
    verify("applesauce", options=Options().with_reporter(ReportWithGitDiff()))
