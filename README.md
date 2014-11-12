qt-files-converter
==================
qt-files-converter modifies caption files.
It renames caption file name (eg. Job_XXXX.mp4_5823fb160c8346bc82ec90cc4d4472b1.qt to XXXX.qt.text.)
and generates XXXX.smil file from template.smil.
In XXXX.smil file all "{file_name}" tags are replaced into XXXX.
qt-files-converter replaces all square brackets in the caption text (just the caption text, not the QT syntax)
with matching parenthesis.
"[BLANK_AUDIO]" tags and the ending time codes are removed anywhere it appears.


Instaltion:
==================
pip install qt-files-converter
