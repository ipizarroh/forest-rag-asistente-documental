import unittest
from public_demo.check_zero_cost import validate
class CostGuardTests(unittest.TestCase):
    def setUp(self):
        self.workflow="jobs:\n  test:\n    if: github.event.repository.private == false\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@"+("a"*40)+"\n"
    def test_public_standard_runner_allowed(self):
        self.assertEqual(validate({"test":self.workflow}),1)
    def test_paid_or_dynamic_runner_rejected(self):
        for runner in ["ubuntu-8-cores","self-hosted","${{ inputs.runner }}"]:
            with self.subTest(runner=runner), self.assertRaises(ValueError):
                validate({"test":self.workflow.replace("ubuntu-latest",runner)})
    def test_private_repository_guard_is_required(self):
        with self.assertRaises(ValueError):validate({"test":self.workflow.replace("if: github.event.repository.private == false","if: always()")})
    def test_storage_and_unapproved_actions_are_blocked(self):
        for extra in ["\n      - uses: actions/upload-artifact@"+("b"*40),"\n          cache: npm","\n      - uses: vendor/paid-service@"+("c"*40)]:
            with self.subTest(extra=extra),self.assertRaises(ValueError):validate({"test":self.workflow+extra})
