"""
Fetch and run workflow
@author Michael Steinbaugh
@note Updated 2023-03-21.

@seealso
- https://docs.latch.bio/
- https://docs.python.org/3/library/subprocess.html
"""

from os import chmod, environ
from os.path import join
from shutil import copytree
from subprocess import run
from tempfile import mkdtemp

# pylint: disable=import-error
from latch import custom_task, workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import (
    LatchAuthor,
    LatchDir,
    LatchMetadata,
    LatchParameter,
)


metadata = LatchMetadata(
    display_name="Fetch and Run",
    documentation="https://koopa.acidgenomics.com/",
    author=LatchAuthor(
        name="Michael Steinbaugh",
        email="mike@steinbaugh.com",
        github="mjsteinbaugh",
    ),
    repository="https://github.com/acidgenomics/koopa/",
    license="AGPL-3",
    parameters={
        "project_dir": LatchParameter(
            display_name="Project directory",
            description="Project directory URL (e.g. AWS S3).",
        ),
        "main_script": LatchParameter(
            display_name="Main script",
            description="Main script basename. Relative to project directory.",
            placeholder="main.sh",
        ),
    },
    tags=["fetch-and-run", "koopa"],
)


@custom_task(cpu=4, memory=16)
def fetch_and_run_task(project_dir: LatchDir, main_script: str) -> LatchDir:
    """
    Fetch and run inside a shell subprocess.
    @note Updated 2023-03-21.
    """
    tmpdir = mkdtemp()
    copytree(src=project_dir.local_path, dst=tmpdir, dirs_exist_ok=True)
    script = join(tmpdir, main_script)
    chmod(script, 0o755)
    args = [script]
    run_env = environ.copy()
    run_env["PATH"] = "/opt/koopa/bin:" + run_env["PATH"]
    print(run_env)
    status = run(args=args, cwd=tmpdir, check=True, env=run_env)
    print(status)
    return LatchDir(tmpdir, project_dir.remote_path)


@workflow(metadata)
def fetch_and_run_workflow(
    project_dir: LatchDir, main_script: str
) -> LatchDir:
    """Fetch a project directory, run a main script, and push the output.

    Fetch and run workflow
    ----

    Take a project directory as input, execute a main script in a subprocess
    shell, and push the output back.

    Updated 2023-03-21.
    """
    out = fetch_and_run_task(project_dir=project_dir, main_script=main_script)
    return out


LaunchPlan(
    workflow=fetch_and_run_workflow,
    name="Test Data",
    default_params={
        "project_dir": LatchDir("latch:///examples/fetch-and-run/hello-world"),
        "main_script": "main.sh",
    },
)
