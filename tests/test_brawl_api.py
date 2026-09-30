import unittest
from unittest.mock import Mock, patch

from brawl_api import BrawlAPIError, BrawlStarsAPI


class BrawlApiTests(unittest.TestCase):
    def test_normalize_tag(self):
        self.assertEqual(BrawlStarsAPI.normalize_tag("  #abc123 "), "ABC123")

    def test_empty_tag(self):
        with self.assertRaises(ValueError):
            BrawlStarsAPI.normalize_tag("#")

    @patch("brawl_api.requests.get")
    def test_get_player(self, get):
        response = Mock(status_code=200)
        response.json.return_value = {"tag": "#ABC123", "name": "Player", "trophies": 10}
        get.return_value = response
        data = BrawlStarsAPI("secret").get_player("#abc123")
        self.assertEqual(data["name"], "Player")
        self.assertIn("%23ABC123", get.call_args.args[0])

    @patch("brawl_api.requests.get")
    def test_not_found(self, get):
        get.return_value = Mock(status_code=404)
        with self.assertRaises(BrawlAPIError):
            BrawlStarsAPI("secret").get_player("ABC123")


if __name__ == "__main__":
    unittest.main()
