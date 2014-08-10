import re


class OMXPlayerParser(object):
    _VIDEO_PROPERTIES_REGEX = re.compile(r'.*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*')
    _AUDIO_PROPERTIES_REGEX = re.compile(r'Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*')

    def __init__(self, process):
        self._process = process
        self.video = dict()
        self.audio = dict()
        self._parse_properties()

    def _parse_properties(self):
        self._parse_video_properties()
        self._parse_audio_properties()

    def _parse_video_properties(self):
        matches = self._VIDEO_PROPERTIES_REGEX.match(self._process.readline())
        if matches:
            video_props = matches.groups()
            self.video['decoder'] = video_props[0]
            self.video['dimensions'] = tuple(int(x) for x in video_props[1:3])
            self.video['profile'] = int(video_props[3])
            self.video['fps'] = float(video_props[4])

    def _parse_audio_properties(self):
        matches = self._AUDIO_PROPERTIES_REGEX.match(self._process.readline())
        if matches:
            audio_props = matches.groups()
            self.audio['decoder'] = audio_props[0]
            (self.audio['channels'], self.audio['rate'],
             self.audio['bps']) = [int(x) for x in audio_props[1:]]