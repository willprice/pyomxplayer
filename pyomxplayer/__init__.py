import re
from threading import Thread
from time import sleep

import pexpect

from pyomxplayer.parser import OMXPlayerParser


class OMXPlayer(object):
    _STATUS_REGEX = re.compile(r'A:\s*[\d.]+\s-?([\d.]+).*')
    _DONE_REGEX = re.compile(r'have a nice day.*')

    _LAUNCH_CMD = 'omxplayer -s %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'



    def __init__(self, media_file, args=None, start_playback=False,
                 _parser=OMXPlayerParser, _spawn=pexpect.spawn):
        self.subtitles_visible = True
        self._spawn = _spawn
        self._launch_omxplayer(media_file, args)
        self.parser = _parser(self._process)
        self._monitor_play_position()

        self.position = 0.0

        # By default the process starts playing
        self.paused = False
        if not start_playback:
            self.toggle_pause()
        self.toggle_subtitles()

    def _launch_omxplayer(self, media_file, args):
        if not args:
            args = ''
        cmd = self._LAUNCH_CMD % (media_file, args)
        self._process = self._spawn(cmd)

    def _monitor_play_position(self):
        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REGEX,
                                          pexpect.TIMEOUT,
                                          pexpect.EOF,
                                          self._DONE_REGEX])
            def timed_out():
                return index == 1

            def process_finished():
                return index in (2, 3)

            if timed_out():
                continue
            elif process_finished():
                break
            else:
                # Process is still running (happy path)
                self.position = float(self._process.match.group(1))
            sleep(0.05)

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def toggle_subtitles(self):
        if self._process.send(self._TOGGLE_SUB_CMD):
            self.subtitles_visible = not self.subtitles_visible

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)
