import unittest
from mock import Mock

from pyomxplayer import OMXPlayer

EXAMPLE_OMXPLAYER_OUTPUT = """Video codec omx-h264 width 1280 height 720 profile 77 fps 25.000000
Audio codec aac channels 2 samplerate 48000 bitspersample 16
Subtitle count: 0, state: off, index: 1, delay: 0
V:PortSettingsChanged: 1280x720@0.04 interlace:0 deinterlace:0 par:1.00 layer:0  0k
M:  545774 V:  5.20s   3120k/  4800k A:  5.24   5.09s/  6.07s Cv:     0k Ca:     0k
"""


class OMXPlayerTests(unittest.TestCase):
    def test_paused_at_startup(self):
        mock_process = Mock()
        mock_process.readline = Mock(return_value=EXAMPLE_OMXPLAYER_OUTPUT)
        mock_spawn = Mock(return_value=mock_process)
        player = OMXPlayer("", _spawn=mock_spawn)
        self.assertTrue(player.paused)
