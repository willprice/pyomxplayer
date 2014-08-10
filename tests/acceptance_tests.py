import unittest
import time

from pyomxplayer import OMXPlayer


class AcceptanceTest(unittest.TestCase):
    def test_opening_mp4_file(self):
       player = OMXPlayer('./tests/test.mp4')
       player.toggle_pause()
       time.sleep(1)
       player.stop()
       self.assertTrue("Completed playing example without errors")