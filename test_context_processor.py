import unittest
from mock import patch

import app


class ContextTestCase(unittest.TestCase):
    @patch("app.get_locale")
    def test_language(self, locale):
        locale.return_value = "es"
        r = app.language()
        self.assertEqual("es", r["language"])
        locale.assert_called_with()
