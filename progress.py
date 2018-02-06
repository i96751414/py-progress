#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import threading


class Progress:
    def __init__(self, show_time=True, keep_bars=False, keep_final=True, size=40):
        assert isinstance(size, int), "size must be an integer"
        assert size > 10, "size must be greater than 10"

        self.__stdout = sys.stdout
        self.__stderr = sys.stderr
        self.__size = size
        self.__keep_bars = keep_bars
        self.__keep_final = keep_final
        self.__lock = threading.Lock()
        self.__is_running = False
        self.__last_len = 0
        self.__last_percent = 0
        self.__start_time = 0
        self.__show_time = show_time

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    class _Stream:
        """
        Helper class to redirect both stdout and stderr.
        """

        def __init__(self, stream, clear_handle, lock):
            self.__stream = stream
            self.__clear_handle = clear_handle
            self.__lock = lock

        def write(self, data):
            self.__lock.acquire()
            self.__clear_handle()
            self.__stream.write(data)
            self.__stream.flush()
            self.__lock.release()

        def flush(self):
            pass

        def __getattr__(self, item):
            return getattr(self.__stream, item)

    def init(self):
        """
        Initializes the progress bar with percentage set to 0.

        :return: None
        """
        self.__is_running = True
        self.__last_percent = 0
        self.__update(0)
        sys.stdout = self._Stream(sys.stdout, self.__clear, self.__lock)
        sys.stderr = self._Stream(sys.stderr, self.__clear, self.__lock)
        self.__start_time = time.time()

    def close(self):
        """
        Closes the progress bar.

        :return: None
        """
        if self.__keep_final:
            self.__lock.acquire()
            self.__update(self.__last_percent)
            self.__stdout.write("\n")
            self.__lock.release()
        else:
            self.__clear()
        sys.stdout = self.__stdout
        sys.stderr = self.__stderr
        self.__is_running = False

    def update(self, percent):
        """
        Updates the progress bar percentage.

        :param percent: Float, a percent value between 0 and 1
        :return: None
        """
        assert self.__is_running, "Percentage() must be initialized first"
        assert 0 <= percent <= 1, "percent parameter must be between 0 and 1"

        self.__lock.acquire()
        self.__update(percent)
        self.__lock.release()

    def __update(self, percent):
        progress = "\r" + ("[%-" + str(self.__size) + "s] %d%%") % (
            "#" * int(round(percent * self.__size)), int(round(percent * 100)))

        if self.__show_time:
            seconds = int(time.time() - self.__start_time)
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            progress = "%s | Time: %d:%02d:%02d" % (progress, h, m, s)

        new_len = len(progress) - 1
        progress += " " * (self.__last_len - new_len)
        self.__stdout.write(progress)
        self.__stdout.flush()
        self.__last_len = new_len
        self.__last_percent = percent

    def __clear(self):
        """
        Clears the current progress bar. If "keep_bars" is set, then simply create a new line.

        :return: None
        """
        if self.__last_len > 0:
            if self.__keep_bars:
                self.__stdout.write("\n")
            else:
                self.__stdout.write("\r" + " " * self.__last_len + "\r")
            self.__stdout.flush()
            self.__last_len = 0
            time.sleep(0.1)
