import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path('scripts').resolve()))
from specialist_visual_reviewer import _normalize_native_review
from agent_contracts import ContractError

valid_pass = {'verdict': 'PASS', 'identity_ok': [], 'scene_requirements_ok': [], 'defects': [], 'drift': []}
valid_minor = {'verdict': 'MINOR_DEFECT', 'identity_ok': [], 'scene_requirements_ok': [], 'defects': ['a'], 'drift': []}
valid_retry = {'verdict': 'RETRY_ILLUSTRIOUS', 'identity_ok': [], 'scene_requirements_ok': [], 'defects': ['a'], 'drift': []}

malformed = {'identity_ok': True, 'scene_requirements_ok': False, 'defects': [], 'drift': []}
missing_verdict = {'identity_ok': [], 'scene_requirements_ok': [], 'defects': [], 'drift': []}
wrong_verdict = {'verdict': 'MAYBE', 'identity_ok': [], 'scene_requirements_ok': [], 'defects': [], 'drift': []}

def test_normalization(review, expect_success):
    try:
        r = _normalize_native_review(review, identifier='id', stage='illustrious')
        if not expect_success:
            print(f'FAIL: review {review} unexpectedly passed. Result: {r}')
            sys.exit(1)
        print(f'PASS: {review} -> {r}')
    except ContractError as e:
        if expect_success:
            print(f'FAIL: review {review} unexpectedly failed. Error: {e}')
            sys.exit(1)
        print(f'PASS (caught expected failure): {e}')

test_normalization(valid_pass, True)
test_normalization(valid_minor, True)
test_normalization(valid_retry, True)
test_normalization(malformed, False)
test_normalization(missing_verdict, False)
test_normalization(wrong_verdict, False)
print('ALL INTEGRITY TESTS PASSED')

