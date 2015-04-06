from distutils.core import setup
import py2exe

files = [('', ['icon.png']), ('', ['dict.txt'])]

setup(windows=[{"script": "Server.py"}], options={"py2exe": {"includes": ["sip"]}}, requires=['numpy', 'PyQt4'], data_files=files)