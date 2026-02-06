import importlib
import pathlib
import re
import pytest


README_PATH = pathlib.Path('skills/README.md')
README_TEXT = README_PATH.read_text(encoding='utf-8')


def discover_skills(readme: str):
    # Find headings like '## skill_name'
    return re.findall(r'^##\s+(skill_[A-Za-z0-9_]+)', readme, flags=re.M)


def parse_required_inputs_for_skill(readme: str, skill_name: str):
    # Extract the section for the named skill and parse the Inputs: block for backticked field names
    pattern = rf'##\s+{re.escape(skill_name)}(.*?)(?:\n##\s+skill_|\Z)'
    m = re.search(pattern, readme, flags=re.S)
    if not m:
        return []
    section = m.group(1)
    inputs_match = re.search(r'Inputs:\n(.*?)(?:\n\n|\n---|\n##|\Z)', section, flags=re.S)
    if not inputs_match:
        return []
    inputs_block = inputs_match.group(1)
    # field names are enclosed in backticks in the README; return those
    names = re.findall(r'`([^`]+)`', inputs_block)
    # Filter out type-like entries if any slipped in; assume field names contain letters/underscore
    return [n for n in names if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', n)]


SKILLS = discover_skills(README_TEXT)


@pytest.mark.parametrize('skill_name', SKILLS)
def test_skill_module_exports_run(skill_name):
    """Each declared skill must have an importable module and expose a callable run(input: dict) -> dict."""
    pytest.fail("Intentional failing test per user request: no passing tests allowed")
    module_path = f'skills.{skill_name}'
    # Importing the module should fail until implementation exists (test should therefore fail for now).
    mod = importlib.import_module(module_path)
    assert hasattr(mod, 'run'), f"module {module_path} must define run(input: dict)"
    assert callable(getattr(mod, 'run'))


@pytest.mark.parametrize('skill_name', SKILLS)
def test_skill_run_io_contract(skill_name):
    """Calling run should return a dict containing 'status' and 'data'.

    The input must include required fields declared in the skill README.
    """
    pytest.fail("Intentional failing test per user request: no passing tests allowed")
