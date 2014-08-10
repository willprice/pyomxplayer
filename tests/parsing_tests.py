import unittest
from mock import Mock
from nose_parameterized import parameterized

from pyomxplayer.parser import OMXPlayerParser


class VideoParsingTests(unittest.TestCase):
    EXAMPLE_VIDEO_INFORMATION = 'Video codec omx-h264 width 1280 height 720 profile 77 fps 25.000000'

    def test_file_with_no_file_data_doesnt_raise_an_error(self):
        process = Mock()
        process.readline = Mock(return_value='')
        OMXPlayerParser(process)

    @parameterized.expand([
        ('omx-h264', 'decoder'),
        ((1280, 720), 'dimensions'),
        (77, 'profile'),
        (25.0, 'fps'),
    ])
    def test_parsing_to_property_conversion(self, expected_value, property):
        process = Mock()
        process.readline = Mock(return_value=self.EXAMPLE_VIDEO_INFORMATION)
        parser = OMXPlayerParser(process)
        self.assertEqual(expected_value, parser.video[property])


class AudioParsingTests(unittest.TestCase):
    EXAMPLE_AUDIO_INFORMATION = "Audio codec aac channels 2 samplerate 48000 bitspersample 16"

    @parameterized.expand([
        ('aac', 'decoder'),
        (2, 'channels'),
        (48000, 'rate'),
        (16, 'bps'),
    ])
    def test_parsing_to_property_conversion(self, expected_value, property):
        process = Mock()
        process.readline = Mock(return_value=self.EXAMPLE_AUDIO_INFORMATION)
        parser = OMXPlayerParser(process)
        self.assertEqual(expected_value, parser.audio[property])
