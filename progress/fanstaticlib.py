""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from pkg_resources import resource_filename


#Libs
deformlib = Library('deform', resource_filename('deform', 'static'))
progress_jslib = Library('progress_js', 'js')
progress_csslib = Library('progress_css', 'css')


reset = Resource(progress_csslib, 'reset.css')
progress_main_css = Resource(progress_csslib, 'main.css', depends=(reset,))

jquery = Resource(progress_jslib, 'jquery-1.6.min.js')
