#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python
# -*- coding: utf-8 -*-
#
# <xbar.title>MyScreen</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>pvdabeel@mac.com</xbar.author>
# <xbar.author.github>pvdabeel</xbar.author.github>
# <xbar.desc>List and connect to screen sessions from the Mac OS X menubar</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
#
# Licence: GPL v3

# Installation instructions: 
# Run 'sudo easy_install screenutils' in Terminal.app
# Ensure you have xbar installed https://github.com/matryer/xbar/releases/latest
# Copy this file to your xbar plugins folder and chmod +x the file from your terminal in that folder
# Run xbar

import sys
import os
import subprocess

from screenutils import list_screens, Screen


# Nice ANSI colors
CEND    = '\33[0m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CGRAY   = '\33[30m'

# Support for OS X Dark Mode
DARK_MODE=os.getenv('XBARDarkMode',0)


# Logo for both dark mode and regular mode
def app_print_logo():
    if bool(DARK_MODE):
       print ('|image=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')
    else:
       print ('|image=iVBORw0KGgoAAAANSUhEUgAAACAAAAAkCAYAAADo6zjiAAAAAXNSR0IArs4c6QAAAIRlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAACQAAAAAQAAAJAAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAACCgAwAEAAAAAQAAACQAAAAASz4lpgAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAuNJREFUWAnllruKVEEQhmdd1xuKmBiLIr6AgSCKYKaBmBgYGpsaGZp4QRAMBBV8C9FYRFAj8Q1MllVQ8YLXXb/vzPmHnjNnxhl3Zjaw4N+q7q6u+qu6+8x2Ov+7LNCARbAV/J5zM8z7fc45B9OlAxdZ2g9+AecisdeYiO1ac5w5demXeefco6wCO/4K3NvMn7vgAtgI2VcymyeBHyTbApbtgGLrN1VW94/t8lJK0MsyTTGmUJYkYLIQcdLEJk1iz6zcxHDdEgKrVp2BUZNc+yy4BvTxueQSYU5XDCysVP0enAaR2xjOfwMSjP969M86zlt0L2AI+DyacosJE3p5pkEiBFZMlEokkODPsX2rpdxkoK+bvbTZ9y86BPo6YCBJJPhL7O2glOsM9JNoyE6VQEiEoSR2g1KuMtBPnxzbpCQSf6ADCWTg3PwX2Ep5JHcY6/u11tk3ru4RKD8+xOqJ7fVLJZH79ay2chicrKz+70c9Nblqss4dcP58HW6p1ib/AFz7BPS1mjaUcZo5eh1gbxUsDuXFOucisqurOkfQH4G+X2qdfaN02z1pJRBHKzwFlJ1d1TmKtmITRecljNLDiPUI5DdAx8gbjIf14DP6GHgEdgCT25En4DJwzk957odxtoFlcAJcAV5ejyO5MPslLA2SLjzDNtBxkNeQyvV/AP4mB3GwAP39jCePeqADzFWVuKh43k/BXuBr8Mw9Dgn6cjwSvweupQNq93thvSuHQJ7u0OqzCd+emMSWGVyRvd0weJINe764DEj2lQs5kndtzAxucluvXSZnWM2FpONIiol2r/EdD5O1NgJxTvscN4MYPN+G+Dd1c09z3fHCKAJtG8q5cRKU/q22leTiRbc6zmiy+pfM8xRTqWhMohZeiUewCKzeX7ayIwxnIuYw1x7gV7RzA0hgI3ApbT8DgQPA95k5zJmIx+0zfw0ezyTDJEGtNhXP+xVUeZM8ehLy0/Cdd9GDnP8ATv97G9cDgnwAAAAASUVORK5CYII=')
    print('---')


def justify(string):
    return justify(string,10)

def justify(string,number):
    length = len(string)
    quot   = (number - length ) // 4
    rem    = (number - length )  % 4
    return string.ljust(length+rem,' ').ljust(length+rem+quot,'\t')

def important(string):
    return CRED + string + CEND


# The main function
def main(argv):

    if DARK_MODE:
        color = '#FFDEDEDE'
        info_color = '#808080'
    else:
        color = 'black' 
        info_color = '#808080'

    app_print_logo()
    prefix = '' 

    no_sessions = True

    for session in list_screens(): 
       no_sessions = False
       if session.status == 'Attached':
          print ('%sSession:\t %s\t%s%s%s| refresh=true terminal=true shell="%s" param1="%s" param2="%s" color=%s' % (prefix, justify(session.name,12), CGREEN,session.status,CEND, 'screen', '-x', session.name, color))
       else:
          print ('%sSession:\t %s\t%s%s%s| refresh=true terminal=true shell="%s" param1="%s" param2="%s" color=%s' % (prefix, justify(session.name,12), CRED,session.status,CEND, 'screen', '-r', session.name, color))
          
    if no_sessions:
        print ('No sessions found')

if __name__ == '__main__':
    main(sys.argv)
