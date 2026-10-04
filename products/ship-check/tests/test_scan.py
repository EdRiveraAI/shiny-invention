"""Tests for the Ship Check scanner. Run: python3 -m unittest discover -s tests"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(HERE, "..", "skills", "ship-check", "scripts", "scan.py")
sys.path.insert(0, os.path.dirname(SCAN))
import scan  # noqa: E402

# Fake secrets are assembled at runtime so this file never contains a real-looking key.
FAKE_AWS = "AKIA" + "Q" * 16
FAKE_STRIPE = "sk_" + "live_" + "a1B2" * 6


def write(root, rel, content):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(content)


def ids(result):
    return {f["id"] for f in result["findings"]}


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def scan(self):
        return scan.Scanner(self.root).run()

    def test_risky_repo_is_blocked(self):
        write(self.root, "package.json", "{}")
        write(self.root, ".env", "DB_PASSWORD=hunter2hunter2\n")
        write(self.root, "src/app.js",
              f'const key = "{FAKE_AWS}";\n'
              f'const stripe = "{FAKE_STRIPE}";\n'
              "console.log('debug');\n"
              "const url = process.env.DB_URL;\n"
              "app.use(cors({ origin: '*' }));\n")
        write(self.root, "Dockerfile", "FROM node:latest\nCMD node src/app.js\n")
        r = self.scan()
        found = ids(r)
        for expected in ["env-file-committed", "secret:aws-access-key", "secret:stripe-live-key",
                         "debug-statement", "missing-env-example", "cors-wildcard",
                         "docker-root", "docker-unpinned", "no-tests", "no-ci", "no-lockfile",
                         "missing-readme"]:
            self.assertIn(expected, found)
        self.assertEqual(r["verdict"], "BLOCKED")
        self.assertIn("Node.js", r["stack"])

    def test_secrets_are_masked(self):
        write(self.root, "config.py", f'AWS = "{FAKE_AWS}"\n')
        out = json.dumps(self.scan())
        self.assertNotIn(FAKE_AWS, out)
        self.assertIn(FAKE_AWS[:4], out)

    def test_placeholders_and_tests_not_flagged(self):
        write(self.root, "app.py", 'password = "your_password_here"\n')
        write(self.root, "tests/test_app.py", 'password = "realLookingPass123"\n')
        self.assertNotIn("secret:hardcoded-credential", ids(self.scan()))

    def test_clean_repo_is_ready(self):
        write(self.root, "README.md", "# App\n")
        write(self.root, "LICENSE", "MIT\n")
        write(self.root, ".github/workflows/ci.yml", "on: push\n")
        write(self.root, "app.py", "import os\nURL = os.environ['URL']\n")
        write(self.root, ".env.example", "URL=\n")
        write(self.root, "tests/test_app.py", "def test_ok():\n    assert True\n")
        r = self.scan()
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["score"], 100)
        self.assertEqual(r["verdict"], "READY")

    def test_cli_fail_on_and_markdown(self):
        write(self.root, "app.py", f'K = "{FAKE_AWS}"\n')
        proc = subprocess.run([sys.executable, SCAN, self.root, "--format", "markdown", "--fail-on", "high"],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("# Ship Check scan", proc.stdout)
        self.assertNotIn(FAKE_AWS, proc.stdout)


if __name__ == "__main__":
    unittest.main()
