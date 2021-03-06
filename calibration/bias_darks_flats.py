# Author: Xavier Paredes-Fortuny (xparedesfortuny@gmail.com)
# License: MIT, see LICENSE.md


import os
import numpy as np
from pyraf import iraf
iraf.imred(_doprint=0)
iraf.ccdred(_doprint=0)
import sys
param = {}
execfile(sys.argv[1])


def save_file_list(i):
    file_list = [i+n for n in os.listdir(i) if n[-5:] == '.fits']
    np.savetxt(i+'input.dat', file_list, fmt="%s")
    return file_list


def make_master_bias(b):
    fl = save_file_list(b)
    [iraf.module.ccdhedit(frame, 'imagetyp', 'zero', type="string") for frame in fl]

    iraf.module.zerocombine.setParam('input', '@'+b+'input.dat')
    iraf.module.zerocombine.setParam('output', b+'master_bias')
    iraf.module.zerocombine.setParam('combine', 'average')
    iraf.module.zerocombine.setParam('reject', 'minmax')
    iraf.module.zerocombine.setParam('ccdtype', 'zero')
    iraf.module.zerocombine.setParam('process', 'no')
    iraf.module.zerocombine.setParam('delete', 'no')
    iraf.module.zerocombine.setParam('clobber', 'no')
    iraf.module.zerocombine.setParam('scale', 'none')
    iraf.module.zerocombine.setParam('statsec', ' ')
    iraf.module.zerocombine.setParam('nlow', 0)
    iraf.module.zerocombine.setParam('nhigh', 1)
    iraf.module.zerocombine.setParam('nkeep', 1)
    iraf.module.zerocombine.setParam('mclip', 'yes')
    iraf.module.zerocombine.setParam('lsigma', 3.0)
    iraf.module.zerocombine.setParam('hsigma', 3.0)
    iraf.module.zerocombine.setParam('rdnoise', 0.)
    iraf.module.zerocombine.setParam('gain', 1.)
    iraf.module.zerocombine.setParam('snoise', 0.)
    iraf.module.zerocombine.setParam('pclip', -0.5)
    iraf.module.zerocombine.setParam('blank', 0.0)
    iraf.module.zerocombine.setParam('mode', 'al')
    iraf.module.zerocombine(mode='h', Stdout=0)


def make_master_dark(d):
    fl = save_file_list(d)
    [iraf.module.ccdhedit(frame, 'imagetyp', 'dark', type="string") for frame in fl]

    # ccdproc setup
    iraf.module.ccdproc.setParam('noproc', 'no')
    iraf.module.ccdproc.setParam('fixpix', 'no')
    iraf.module.ccdproc.setParam('overscan', 'no')
    iraf.module.ccdproc.setParam('trim', 'no')
    iraf.module.ccdproc.setParam('zerocor', 'no')
    iraf.module.ccdproc.setParam('darkcor', 'no')
    iraf.module.ccdproc.setParam('flatcor', 'no')
    iraf.module.ccdproc.setParam('illumcor', 'no')
    iraf.module.ccdproc.setParam('fringecor', 'no')
    iraf.module.ccdproc.setParam('readcor', 'no')
    iraf.module.ccdproc.setParam('scancor', 'no')
    iraf.module.ccdproc.setParam('readaxis', 'line')
    iraf.module.ccdproc.setParam('fixfile', ' ')
    iraf.module.ccdproc.setParam('biassec', ' ')
    iraf.module.ccdproc.setParam('trimsec', ' ')
    iraf.module.ccdproc.setParam('zero', ' ')
    iraf.module.ccdproc.setParam('dark', ' ')
    iraf.module.ccdproc.setParam('flat', ' ')
    iraf.module.ccdproc.setParam('illum', ' ')
    iraf.module.ccdproc.setParam('fringe', '')
    iraf.module.ccdproc.setParam('minreplace', 1.0)
    iraf.module.ccdproc.setParam('scantype', 'shortscan')
    iraf.module.ccdproc.setParam('nscan', 1)
    iraf.module.ccdproc.setParam('interactive', 'no')
    iraf.module.ccdproc.setParam('function', 'legendre')
    iraf.module.ccdproc.setParam('order', '1')
    iraf.module.ccdproc.setParam('sample', '*')
    iraf.module.ccdproc.setParam('naverage', '1')
    iraf.module.ccdproc.setParam('niterate', '1')
    iraf.module.ccdproc.setParam('low_reject', '3.0')
    iraf.module.ccdproc.setParam('high_reject', '3.0')
    iraf.module.ccdproc.setParam('grow', '0.0')

    # master dark
    iraf.module.darkcombine.setParam('input', '@'+d + 'input.dat')
    iraf.module.darkcombine.setParam('output', d + 'master_dark')
    iraf.module.darkcombine.setParam('combine', 'average')
    iraf.module.darkcombine.setParam('reject', 'minmax')
    iraf.module.darkcombine.setParam('ccdtype', 'dark')
    iraf.module.darkcombine.setParam('process', 'yes')
    iraf.module.darkcombine.setParam('delete', 'no')
    iraf.module.darkcombine.setParam('clobber', 'no')
    iraf.module.darkcombine.setParam('scale', 'exposure')
    iraf.module.darkcombine.setParam('statsec', ' ')
    iraf.module.darkcombine.setParam('nlow', 0)
    iraf.module.darkcombine.setParam('nhigh', 1)
    iraf.module.darkcombine.setParam('nkeep', 1)
    iraf.module.darkcombine.setParam('mclip', 'yes')
    iraf.module.darkcombine.setParam('lsigma', 3.0)
    iraf.module.darkcombine.setParam('hsigma', 3.0)
    iraf.module.darkcombine.setParam('rdnoise', 0.)
    iraf.module.darkcombine.setParam('gain', 1.)
    iraf.module.darkcombine.setParam('snoise', 0.)
    iraf.module.darkcombine.setParam('pclip', -0.5)
    iraf.module.darkcombine.setParam('blank', 0.0)
    iraf.module.darkcombine(mode='h', Stdout=0)


def make_master_flat(f, b):
    fl = save_file_list(f)
    [iraf.module.ccdhedit(frame, 'imagetyp', 'flat', type="string") for frame in fl]

    # master flat
    iraf.module.flatcombine.setParam('input', '@'+f + 'input.dat')
    iraf.module.flatcombine.setParam('output', f + 'master_flat')
    iraf.module.flatcombine.setParam('combine', 'median')
    iraf.module.flatcombine.setParam('reject', 'crreject')
    iraf.module.flatcombine.setParam('ccdtype', 'flat')
    iraf.module.flatcombine.setParam('process', 'yes')
    iraf.module.flatcombine.setParam('subsets', 'yes')
    iraf.module.flatcombine.setParam('delete', 'no')
    iraf.module.flatcombine.setParam('clobber', 'no')
    iraf.module.flatcombine.setParam('scale', 'mode')
    iraf.module.flatcombine.setParam('statsec', ' ')
    iraf.module.flatcombine.setParam('nlow', 1)
    iraf.module.flatcombine.setParam('nhigh', 1)
    iraf.module.flatcombine.setParam('nkeep', 1)
    iraf.module.flatcombine.setParam('mclip', 'yes')
    iraf.module.flatcombine.setParam('lsigma', 3.0)
    iraf.module.flatcombine.setParam('hsigma', 3.0)
    iraf.module.flatcombine.setParam('rdnoise', 0.)
    iraf.module.flatcombine.setParam('gain', 1.)
    iraf.module.flatcombine.setParam('snoise', 0.)
    iraf.module.flatcombine.setParam('pclip', -0.5)
    iraf.module.flatcombine.setParam('blank', 0.0)
    iraf.module.flatcombine(mode='h', Stdout=0)


def calibrate_science_frames(s, b, d, f):
    fl = save_file_list(s)
    [iraf.module.ccdhedit(frame, 'imagetyp', 'object', type="string") for frame in fl]

    if param['disable_bias'] == 0:
        # science - bias
        iraf.module.ccdproc.setParam('images', '@'+s+'input.dat')
        iraf.module.ccdproc.setParam('output', ' ')
        iraf.module.ccdproc.setParam('ccdtype', 'object')
        iraf.module.ccdproc.setParam('max_cache', 0)
        iraf.module.ccdproc.setParam('noproc', 'no')
        iraf.module.ccdproc.setParam('fixpix', 'no')
        iraf.module.ccdproc.setParam('overscan', 'no')
        iraf.module.ccdproc.setParam('trim', 'no')
        iraf.module.ccdproc.setParam('zerocor', 'yes')
        iraf.module.ccdproc.setParam('darkcor', 'no')
        iraf.module.ccdproc.setParam('flatcor', 'no')
        iraf.module.ccdproc.setParam('illumcor', 'no')
        iraf.module.ccdproc.setParam('fringecor', 'no')
        iraf.module.ccdproc.setParam('readcor', 'no')
        iraf.module.ccdproc.setParam('scancor', 'no')
        iraf.module.ccdproc.setParam('readaxis', 'line')
        iraf.module.ccdproc.setParam('fixfile', ' ')
        iraf.module.ccdproc.setParam('biassec', ' ')
        iraf.module.ccdproc.setParam('trimsec', ' ')
        iraf.module.ccdproc.setParam('zero', b+'master_bias')
        iraf.module.ccdproc.setParam('dark',' ')
        iraf.module.ccdproc.setParam('flat', ' ')
        iraf.module.ccdproc.setParam('illum', ' ')
        iraf.module.ccdproc.setParam('fringe', '')
        iraf.module.ccdproc.setParam('minreplace', 1.0)
        iraf.module.ccdproc.setParam('scantype', 'shortscan')
        iraf.module.ccdproc.setParam('nscan', 1)
        iraf.module.ccdproc.setParam('interactive', 'no')
        iraf.module.ccdproc.setParam('function', 'legendre')
        iraf.module.ccdproc.setParam('order', '1')
        iraf.module.ccdproc.setParam('sample', '*')
        iraf.module.ccdproc.setParam('naverage', '1')
        iraf.module.ccdproc.setParam('niterate', '1')
        iraf.module.ccdproc.setParam('low_reject', '3.0')
        iraf.module.ccdproc.setParam('high_reject', '3.0')
        iraf.module.ccdproc.setParam('grow', '0.0')
        iraf.module.ccdproc(mode='h', Stdout=0)

    # science - darks
    iraf.module.ccdproc.setParam('images', '@'+s+'input.dat')
    iraf.module.ccdproc.setParam('output', ' ')
    iraf.module.ccdproc.setParam('ccdtype', 'object')
    iraf.module.ccdproc.setParam('max_cache', 0)
    iraf.module.ccdproc.setParam('noproc', 'no')
    iraf.module.ccdproc.setParam('fixpix', 'no')
    iraf.module.ccdproc.setParam('overscan', 'no')
    iraf.module.ccdproc.setParam('trim', 'no')
    iraf.module.ccdproc.setParam('zerocor', 'no')
    iraf.module.ccdproc.setParam('darkcor', 'yes')
    iraf.module.ccdproc.setParam('flatcor', 'no')
    iraf.module.ccdproc.setParam('illumcor', 'no')
    iraf.module.ccdproc.setParam('fringecor', 'no')
    iraf.module.ccdproc.setParam('readcor', 'no')
    iraf.module.ccdproc.setParam('scancor', 'no')
    iraf.module.ccdproc.setParam('readaxis', 'line')
    iraf.module.ccdproc.setParam('fixfile', ' ')
    iraf.module.ccdproc.setParam('biassec', ' ')
    iraf.module.ccdproc.setParam('trimsec', ' ')
    iraf.module.ccdproc.setParam('zero', ' ')
    iraf.module.ccdproc.setParam('dark', d+'master_dark')
    iraf.module.ccdproc.setParam('flat', ' ')
    iraf.module.ccdproc.setParam('illum', ' ')
    iraf.module.ccdproc.setParam('fringe', '')
    iraf.module.ccdproc.setParam('minreplace', 1.0)
    iraf.module.ccdproc.setParam('scantype', 'shortscan')
    iraf.module.ccdproc.setParam('nscan', 1)
    iraf.module.ccdproc.setParam('interactive', 'no')
    iraf.module.ccdproc.setParam('function', 'legendre')
    iraf.module.ccdproc.setParam('order', '1')
    iraf.module.ccdproc.setParam('sample', '*')
    iraf.module.ccdproc.setParam('naverage', '1')
    iraf.module.ccdproc.setParam('niterate', '1')
    iraf.module.ccdproc.setParam('low_reject', '3.0')
    iraf.module.ccdproc.setParam('high_reject', '3.0')
    iraf.module.ccdproc.setParam('grow', '0.0')
    iraf.module.ccdproc(mode='h', Stdout=0)

    if param['disable_normal_flat'] == 0 or param['disable_screen_flat'] == 0:
    # science / flat
        iraf.module.ccdproc.setParam('images', '@'+s+'input.dat')
        iraf.module.ccdproc.setParam('output', ' ')
        iraf.module.ccdproc.setParam('ccdtype', 'object')
        iraf.module.ccdproc.setParam('max_cache', 0)
        iraf.module.ccdproc.setParam('noproc', 'no')
        iraf.module.ccdproc.setParam('fixpix', 'no')
        iraf.module.ccdproc.setParam('overscan', 'no')
        iraf.module.ccdproc.setParam('trim', 'no')
        iraf.module.ccdproc.setParam('zerocor', 'no')
        iraf.module.ccdproc.setParam('darkcor', 'no')
        iraf.module.ccdproc.setParam('flatcor', 'yes')
        iraf.module.ccdproc.setParam('illumcor', 'no')
        iraf.module.ccdproc.setParam('fringecor', 'no')
        iraf.module.ccdproc.setParam('readcor', 'no')
        iraf.module.ccdproc.setParam('scancor', 'no')
        iraf.module.ccdproc.setParam('readaxis', 'line')
        iraf.module.ccdproc.setParam('fixfile', ' ')
        iraf.module.ccdproc.setParam('biassec', ' ')
        iraf.module.ccdproc.setParam('trimsec', ' ')
        iraf.module.ccdproc.setParam('zero', ' ')
        iraf.module.ccdproc.setParam('dark', ' ')
        iraf.module.ccdproc.setParam('flat', f+'master_flat')
        iraf.module.ccdproc.setParam('illum', ' ')
        iraf.module.ccdproc.setParam('fringe', '')
        iraf.module.ccdproc.setParam('minreplace', 1.0)
        iraf.module.ccdproc.setParam('scantype', 'shortscan')
        iraf.module.ccdproc.setParam('nscan', 1)
        iraf.module.ccdproc.setParam('interactive', 'no')
        iraf.module.ccdproc.setParam('function', 'legendre')
        iraf.module.ccdproc.setParam('order', '1')
        iraf.module.ccdproc.setParam('sample', '*')
        iraf.module.ccdproc.setParam('naverage', '1')
        iraf.module.ccdproc.setParam('niterate', '1')
        iraf.module.ccdproc.setParam('low_reject', '3.0')
        iraf.module.ccdproc.setParam('high_reject', '3.0')
        iraf.module.ccdproc.setParam('grow', '0.0')
        iraf.module.ccdproc(mode='h', Stdout=0)


def calibrate_data(i):
    if param['disable_bias'] == 0:
        make_master_bias(i+'bias/')
    make_master_dark(i+'darks/')
    if param['disable_screen_flat'] == 1 and param['disable_normal_flat'] == 0:
        make_master_flat(i+'flats/', i+'bias/')
    calibrate_science_frames(i+'science/', i+'bias/', i+'darks/', i+'flats/')
    try:
        os.remove('logfile')
    except OSError:
        pass


if __name__ == '__main__':
    # Testing
    field_name = param['field_name']
    fp = param['test_path']
    calibrate_data(fp, fp+'/phot/'+field_name+'/tmp/')
    print('DONE')
