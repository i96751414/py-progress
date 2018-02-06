#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import time
from progress import Progress


def example1():
    print("\nEXAMPLE 1: Don't keep bars while printing in the middle, and show final percentage:")
    with Progress() as p:
        for i in range(101):
            p.update(i / 100.0)
            if i == 30:
                print("This is a print")
            elif i == 80:
                print("This is other print", file=sys.stderr)
            time.sleep(0.1)


def example2():
    print("\nEXAMPLE 2: Keep bars while printing in the middle and don't show elapsed time:")
    with Progress(show_time=False, keep_bars=True) as p:
        for i in range(101):
            p.update(i / 100.0)
            if i == 30:
                print("This is a print")
            elif i == 80:
                print("This is other print", file=sys.stderr)
            time.sleep(0.1)


def example3():
    print("\nEXAMPLE 3: Don't keep bars while printing in the middle, and don't show final percentage:")
    with Progress(keep_final=False) as p:
        for i in range(101):
            p.update(i / 100.0)
            if i == 30:
                print("This is a print")
            elif i == 80:
                print("This is other print", file=sys.stderr)
            time.sleep(0.1)


if __name__ == "__main__":
    example1()
    example2()
    example3()
