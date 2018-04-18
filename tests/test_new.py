from __future__ import absolute_import

import pytest
import os
import sys
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pycdlib

from test_common import *

def do_a_test(iso, check_func):
    out = BytesIO()
    iso.write_fp(out)

    check_func(iso, len(out.getvalue()))

    iso2 = pycdlib.PyCdlib()
    iso2.open_fp(out)
    check_func(iso2, len(out.getvalue()))
    iso2.close()

def test_new_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_onefile():
    # Now open up the ISO with pycdlib and check some things out.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a directory.
    iso.add_directory("/DIR1")

    do_a_test(iso, check_onedir)

    iso.close()

def test_new_twofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add new files.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/BAR.;1")

    do_a_test(iso, check_twofiles)

    iso.close()

def test_new_twofiles2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add new files.
    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/BAR.;1")
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    do_a_test(iso, check_twofiles)

    iso.close()

def test_new_twodirs():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new directories.
    iso.add_directory("/AA")
    iso.add_directory("/BB")

    do_a_test(iso, check_twodirs)

    iso.close()

def test_new_twodirs2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new directories.
    iso.add_directory("/BB")
    iso.add_directory("/AA")

    do_a_test(iso, check_twodirs)

    iso.close()

def test_new_onefileonedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    # Add new directory.
    iso.add_directory("/DIR1")

    do_a_test(iso, check_onefileonedir)

    iso.close()

def test_new_onefileonedir2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add new directory.
    iso.add_directory("/DIR1")
    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    do_a_test(iso, check_onefileonedir)

    iso.close()

def test_new_onefile_onedirwithfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    # Add new directory.
    iso.add_directory("/DIR1")
    # Add new sub-file.
    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/DIR1/BAR.;1")

    do_a_test(iso, check_onefile_onedirwithfile)

    iso.close()

def test_new_tendirs():
    numdirs = 10

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    for i in range(1, 1+numdirs):
        iso.add_directory("/DIR%d" % i)

    do_a_test(iso, check_tendirs)

    iso.close()

def test_new_dirs_overflow_ptr_extent():
    numdirs = 295

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    for i in range(1, 1+numdirs):
        iso.add_directory("/DIR%d" % i)

    do_a_test(iso, check_dirs_overflow_ptr_extent)

    iso.close()

def test_new_dirs_just_short_ptr_extent():
    numdirs = 293

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    for i in range(1, 1+numdirs):
        iso.add_directory("/DIR%d" % i)
    # Now add two more to push it over the boundary
    iso.add_directory("/DIR294")
    iso.add_directory("/DIR295")

    # Now remove them to put it back down below the boundary.
    iso.rm_directory("/DIR295")
    iso.rm_directory("/DIR294")

    do_a_test(iso, check_dirs_just_short_ptr_extent)

    iso.close()

def test_new_twoextentfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    outstr = b""
    for j in range(0, 8):
        for i in range(0, 256):
            outstr += struct.pack("=B", i)
    outstr += struct.pack("=B", 0)

    iso.add_fp(BytesIO(outstr), len(outstr), "/BIGFILE.;1")

    do_a_test(iso, check_twoextentfile)

    iso.close()

def test_new_twoleveldeepdir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new directory.
    iso.add_directory("/DIR1")
    iso.add_directory("/DIR1/SUBDIR1")

    do_a_test(iso, check_twoleveldeepdir)

    iso.close()

def test_new_twoleveldeepfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new directory.
    iso.add_directory("/DIR1")
    iso.add_directory("/DIR1/SUBDIR1")
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/DIR1/SUBDIR1/FOO.;1")

    do_a_test(iso, check_twoleveldeepfile)

    iso.close()

def test_new_dirs_overflow_ptr_extent_reverse():
    numdirs = 295

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    for i in reversed(range(1, 1+numdirs)):
        iso.add_directory("/DIR%d" % i)

    do_a_test(iso, check_dirs_overflow_ptr_extent)

    iso.close()

def test_new_toodeepdir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a directory.
    iso.add_directory("/DIR1")
    iso.add_directory("/DIR1/DIR2")
    iso.add_directory("/DIR1/DIR2/DIR3")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/DIR8")

    # Now make sure we can re-open the written ISO.
    out = BytesIO()
    iso.write_fp(out)
    pycdlib.PyCdlib().open_fp(out)

    iso.close()

def test_new_toodeepfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a directory.
    iso.add_directory("/DIR1")
    iso.add_directory("/DIR1/DIR2")
    iso.add_directory("/DIR1/DIR2/DIR3")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7")
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/FOO.;1")

    # Now make sure we can re-open the written ISO.
    out = BytesIO()
    iso.write_fp(out)
    pycdlib.PyCdlib().open_fp(out)

    iso.close()

def test_new_removefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    # Add second new file.
    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/BAR.;1")

    # Remove the second file.
    iso.rm_file("/BAR.;1")

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_removedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    # Add new directory.
    iso.add_directory("/DIR1")

    # Remove the directory
    iso.rm_directory("/DIR1")

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_eltorito():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    do_a_test(iso, check_eltorito_nofiles)

    iso.close()

def test_new_rm_eltorito():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.rm_eltorito()
    iso.rm_file("/BOOT.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_eltorito_twofile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AA.;1")

    do_a_test(iso, check_eltorito_twofile)

    iso.close()

def test_new_rr_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    do_a_test(iso, check_rr_nofiles)

    iso.close()

def test_new_rr_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    do_a_test(iso, check_rr_onefile)

    iso.close()

def test_new_rr_twofile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    # Add a new file.
    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/BAR.;1", rr_name="bar")

    do_a_test(iso, check_rr_twofile)

    iso.close()

def test_new_rr_onefileonedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    # Add new directory.
    iso.add_directory("/DIR1", rr_name="dir1")

    do_a_test(iso, check_rr_onefileonedir)

    iso.close()

def test_new_rr_onefileonedirwithfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    # Add new directory.
    iso.add_directory("/DIR1", rr_name="dir1")

    # Add a new file.
    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/DIR1/BAR.;1", rr_name="bar")

    do_a_test(iso, check_rr_onefileonedirwithfile)

    iso.close()

def test_new_rr_symlink():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    iso.add_symlink("/SYM.;1", "sym", "foo")

    do_a_test(iso, check_rr_symlink)

    iso.close()

def test_new_rr_symlink2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add new directory.
    iso.add_directory("/DIR1", rr_name="dir1")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/DIR1/FOO.;1", rr_name="foo")

    iso.add_symlink("/SYM.;1", "sym", "dir1/foo")

    do_a_test(iso, check_rr_symlink2)

    iso.close()

def test_new_rr_symlink_dot():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_symlink("/SYM.;1", "sym", ".")

    do_a_test(iso, check_rr_symlink_dot)

    iso.close()

def test_new_rr_symlink_dotdot():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_symlink("/SYM.;1", "sym", "..")

    do_a_test(iso, check_rr_symlink_dotdot)

    iso.close()

def test_new_rr_symlink_broken():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_symlink("/SYM.;1", "sym", "foo")

    do_a_test(iso, check_rr_symlink_broken)

    iso.close()

def test_new_rr_verylongname():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_rr_verylongname)

    iso.close()

def test_new_rr_verylongname_joliet():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*RR_MAX_FILENAME_LENGTH, joliet_path="/"+"a"*64)

    do_a_test(iso, check_rr_verylongname_joliet)

    iso.close()

def test_new_rr_manylongname():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*RR_MAX_FILENAME_LENGTH)

    bbstr = b"bb\n"
    iso.add_fp(BytesIO(bbstr), len(bbstr), "/BBBBBBBB.;1", rr_name="b"*RR_MAX_FILENAME_LENGTH)

    ccstr = b"cc\n"
    iso.add_fp(BytesIO(ccstr), len(ccstr), "/CCCCCCCC.;1", rr_name="c"*RR_MAX_FILENAME_LENGTH)

    ddstr = b"dd\n"
    iso.add_fp(BytesIO(ddstr), len(ddstr), "/DDDDDDDD.;1", rr_name="d"*RR_MAX_FILENAME_LENGTH)

    eestr = b"ee\n"
    iso.add_fp(BytesIO(eestr), len(eestr), "/EEEEEEEE.;1", rr_name="e"*RR_MAX_FILENAME_LENGTH)

    ffstr = b"ff\n"
    iso.add_fp(BytesIO(ffstr), len(ffstr), "/FFFFFFFF.;1", rr_name="f"*RR_MAX_FILENAME_LENGTH)

    ggstr = b"gg\n"
    iso.add_fp(BytesIO(ggstr), len(ggstr), "/GGGGGGGG.;1", rr_name="g"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_rr_manylongname)

    iso.close()

def test_new_rr_manylongname2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*RR_MAX_FILENAME_LENGTH)

    bbstr = b"bb\n"
    iso.add_fp(BytesIO(bbstr), len(bbstr), "/BBBBBBBB.;1", rr_name="b"*RR_MAX_FILENAME_LENGTH)

    ccstr = b"cc\n"
    iso.add_fp(BytesIO(ccstr), len(ccstr), "/CCCCCCCC.;1", rr_name="c"*RR_MAX_FILENAME_LENGTH)

    ddstr = b"dd\n"
    iso.add_fp(BytesIO(ddstr), len(ddstr), "/DDDDDDDD.;1", rr_name="d"*RR_MAX_FILENAME_LENGTH)

    eestr = b"ee\n"
    iso.add_fp(BytesIO(eestr), len(eestr), "/EEEEEEEE.;1", rr_name="e"*RR_MAX_FILENAME_LENGTH)

    ffstr = b"ff\n"
    iso.add_fp(BytesIO(ffstr), len(ffstr), "/FFFFFFFF.;1", rr_name="f"*RR_MAX_FILENAME_LENGTH)

    ggstr = b"gg\n"
    iso.add_fp(BytesIO(ggstr), len(ggstr), "/GGGGGGGG.;1", rr_name="g"*RR_MAX_FILENAME_LENGTH)

    hhstr = b"hh\n"
    iso.add_fp(BytesIO(hhstr), len(hhstr), "/HHHHHHHH.;1", rr_name="h"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_rr_manylongname2)

    iso.close()

def test_new_rr_verylongnameandsymlink():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*RR_MAX_FILENAME_LENGTH)

    iso.add_symlink("/BBBBBBBB.;1", "b"*RR_MAX_FILENAME_LENGTH, "a"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_rr_verylongnameandsymlink)

    iso.close()

def test_new_alternating_subdir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    ddstr = b"dd\n"
    iso.add_fp(BytesIO(ddstr), len(ddstr), "/DD.;1")

    bbstr = b"bb\n"
    iso.add_fp(BytesIO(bbstr), len(bbstr), "/BB.;1")

    iso.add_directory("/CC")

    iso.add_directory("/AA")

    subdirfile1 = b"sub1\n"
    iso.add_fp(BytesIO(subdirfile1), len(subdirfile1), "/AA/SUB1.;1")

    subdirfile2 = b"sub2\n"
    iso.add_fp(BytesIO(subdirfile2), len(subdirfile2), "/CC/SUB2.;1")

    do_a_test(iso, check_alternating_subdir)

    iso.close()

def test_new_joliet_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_joliet_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_onedir)

    iso.close()

def test_new_joliet_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    do_a_test(iso, check_joliet_onefile)

    iso.close()

def test_new_joliet_onefileonedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.add_directory("/DIR1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_onefileonedir)

    iso.close()

def test_new_joliet_and_rr_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    do_a_test(iso, check_joliet_and_rr_nofiles)

    iso.close()

def test_new_joliet_and_rr_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo", joliet_path="/foo")

    do_a_test(iso, check_joliet_and_rr_onefile)

    iso.close()

def test_new_joliet_and_rr_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    # Add a directory.
    iso.add_directory("/DIR1", rr_name="dir1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_and_rr_onedir)

    iso.close()

def test_new_rr_and_eltorito_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    do_a_test(iso, check_rr_and_eltorito_nofiles)

    iso.close()

def test_new_rr_and_eltorito_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    do_a_test(iso, check_rr_and_eltorito_onefile)

    iso.close()

def test_new_rr_and_eltorito_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.add_directory("/DIR1", rr_name="dir1")

    do_a_test(iso, check_rr_and_eltorito_onedir)

    iso.close()

def test_new_rr_and_eltorito_onedir2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/DIR1", rr_name="dir1")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    do_a_test(iso, check_rr_and_eltorito_onedir)

    iso.close()

def test_new_joliet_and_eltorito_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    do_a_test(iso, check_joliet_and_eltorito_nofiles)

    iso.close()

def test_new_joliet_and_eltorito_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    do_a_test(iso, check_joliet_and_eltorito_onefile)

    iso.close()

def test_new_joliet_and_eltorito_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.add_directory("/DIR1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_and_eltorito_onedir)

    iso.close()

def test_new_isohybrid():
    # Create a new ISO
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add Eltorito
    isolinuxstr = b'\x00'*0x40 + b'\xfb\xc0\x78\x70'
    iso.add_fp(BytesIO(isolinuxstr), len(isolinuxstr), "/ISOLINUX.BIN;1")
    iso.add_eltorito("/ISOLINUX.BIN;1", "/BOOT.CAT;1", boot_load_size=4)
    # Now add the syslinux data
    iso.add_isohybrid()

    do_a_test(iso, check_isohybrid)

    iso.close()

def test_new_isohybrid_mac_uefi():
    # Create a new ISO
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add Eltorito
    isolinuxstr = b'\x00'*0x40 + b'\xfb\xc0\x78\x70'
    iso.add_fp(BytesIO(isolinuxstr), len(isolinuxstr), "/ISOLINUX.BIN;1")
    efibootstr = b'a'
    iso.add_fp(BytesIO(efibootstr), len(efibootstr), "/EFIBOOT.IMG;1")
    macbootstr = b'b'
    iso.add_fp(BytesIO(macbootstr), len(macbootstr), "/MACBOOT.IMG;1")

    iso.add_eltorito("/ISOLINUX.BIN;1", "/BOOT.CAT;1", boot_load_size=4, boot_info_table=True)
    iso.add_eltorito("/MACBOOT.IMG;1", efi=True)
    iso.add_eltorito("/EFIBOOT.IMG;1", efi=True)
    # Now add the syslinux data
    iso.add_isohybrid(mac=True)

    do_a_test(iso, check_isohybrid_mac_uefi)

    iso.close()

def test_new_joliet_rr_and_eltorito_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    do_a_test(iso, check_joliet_rr_and_eltorito_nofiles)

    iso.close()

def test_new_joliet_rr_and_eltorito_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo", joliet_path="/foo")

    do_a_test(iso, check_joliet_rr_and_eltorito_onefile)

    iso.close()

def test_new_joliet_rr_and_eltorito_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.add_directory("/DIR1", rr_name="dir1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_rr_and_eltorito_onedir)

    iso.close()

def test_new_rr_rmfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    iso.rm_file("/FOO.;1", rr_name="foo")

    do_a_test(iso, check_rr_nofiles)

    iso.close()

def test_new_rr_rmdir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/DIR1", rr_name="dir1")

    iso.rm_directory("/DIR1", rr_name="dir1")

    do_a_test(iso, check_rr_nofiles)

    iso.close()

def test_new_joliet_rmfile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")

    iso.rm_file("/BOOT.;1", joliet_path="/boot")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_joliet_rmdir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    iso.rm_directory("/DIR1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_rr_deep():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory('/DIR1', rr_name='dir1')
    iso.add_directory('/DIR1/DIR2', rr_name='dir2')
    iso.add_directory('/DIR1/DIR2/DIR3', rr_name='dir3')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4', rr_name='dir4')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5', rr_name='dir5')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6', rr_name='dir6')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7', rr_name='dir7')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/DIR8', rr_name='dir8')

    do_a_test(iso, check_rr_deep_dir)

    iso.close()

def test_new_xa_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(xa=True)

    do_a_test(iso, check_xa_nofiles)

    iso.close()

def test_new_xa_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(xa=True)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    do_a_test(iso, check_xa_onefile)

    iso.close()

def test_new_xa_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(xa=True)

    iso.add_directory("/DIR1")

    do_a_test(iso, check_xa_onedir)

    iso.close()

def test_new_sevendeepdirs():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/DIR1", rr_name="dir1")
    iso.add_directory("/DIR1/DIR2", rr_name="dir2")
    iso.add_directory("/DIR1/DIR2/DIR3", rr_name="dir3")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4", rr_name="dir4")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5", rr_name="dir5")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6", rr_name="dir6")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7", rr_name="dir7")

    do_a_test(iso, check_sevendeepdirs)

    iso.close()

def test_new_xa_joliet_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, xa=True)

    do_a_test(iso, check_xa_joliet_nofiles)

    iso.close()

def test_new_xa_joliet_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, xa=True)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    do_a_test(iso, check_xa_joliet_onefile)

    iso.close()

def test_new_xa_joliet_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, xa=True)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    do_a_test(iso, check_xa_joliet_onedir)

    iso.close()

def test_new_isolevel4_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    do_a_test(iso, check_isolevel4_nofiles)

    iso.close()

def test_new_isolevel4_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/foo")

    do_a_test(iso, check_isolevel4_onefile)

    iso.close()

def test_new_isolevel4_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    iso.add_directory("/dir1")

    do_a_test(iso, check_isolevel4_onedir)

    iso.close()

def test_new_isolevel4_eltorito():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat")

    do_a_test(iso, check_isolevel4_eltorito)

    iso.close()

def test_new_everything():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4, rock_ridge="1.09", joliet=3, xa=True)

    iso.add_directory("/dir1", rr_name="dir1", joliet_path="/dir1")
    iso.add_directory("/dir1/dir2", rr_name="dir2", joliet_path="/dir1/dir2")
    iso.add_directory("/dir1/dir2/dir3", rr_name="dir3", joliet_path="/dir1/dir2/dir3")
    iso.add_directory("/dir1/dir2/dir3/dir4", rr_name="dir4", joliet_path="/dir1/dir2/dir3/dir4")
    iso.add_directory("/dir1/dir2/dir3/dir4/dir5", rr_name="dir5", joliet_path="/dir1/dir2/dir3/dir4/dir5")
    iso.add_directory("/dir1/dir2/dir3/dir4/dir5/dir6", rr_name="dir6", joliet_path = "/dir1/dir2/dir3/dir4/dir5/dir6")
    iso.add_directory("/dir1/dir2/dir3/dir4/dir5/dir6/dir7", rr_name="dir7", joliet_path="/dir1/dir2/dir3/dir4/dir5/dir6/dir7")
    iso.add_directory("/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8", rr_name="dir8", joliet_path="/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot", rr_name="boot", joliet_path="/boot")
    iso.add_eltorito("/boot", "/boot.cat", boot_info_table=True)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/foo", rr_name="foo", joliet_path="/foo")

    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8/bar", rr_name="bar", joliet_path="/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8/bar")

    iso.add_symlink("/sym", "sym", "foo", joliet_path="/sym")

    iso.add_hard_link(iso_new_path="/dir1/foo", iso_old_path="/foo", rr_name="foo")
    iso.add_hard_link(iso_old_path="/foo", joliet_new_path="/dir1/foo")

    do_a_test(iso, check_everything)

    iso.close()

def test_new_rr_xa_nofiles():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", xa=True)

    do_a_test(iso, check_rr_xa_nofiles)

    iso.close()

def test_new_rr_xa_onefile():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", xa=True)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    do_a_test(iso, check_rr_xa_onefile)

    iso.close()

def test_new_rr_xa_onedir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", xa=True)

    iso.add_directory("/DIR1", rr_name="dir1")

    do_a_test(iso, check_rr_xa_onedir)

    iso.close()

def test_new_rr_joliet_symlink():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo", joliet_path="/foo")

    iso.add_symlink("/SYM.;1", "sym", "foo", joliet_path="/sym")

    do_a_test(iso, check_rr_joliet_symlink)

    iso.close()

def test_new_rr_joliet_deep():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)

    iso.add_directory("/DIR1", rr_name="dir1", joliet_path="/dir1")
    iso.add_directory("/DIR1/DIR2", rr_name="dir2", joliet_path="/dir1/dir2")
    iso.add_directory("/DIR1/DIR2/DIR3", rr_name="dir3", joliet_path="/dir1/dir2/dir3")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4", rr_name="dir4", joliet_path="/dir1/dir2/dir3/dir4")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5", rr_name="dir5", joliet_path="/dir1/dir2/dir3/dir4/dir5")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6", rr_name="dir6", joliet_path = "/dir1/dir2/dir3/dir4/dir5/dir6")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7", rr_name="dir7", joliet_path="/dir1/dir2/dir3/dir4/dir5/dir6/dir7")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/DIR8", rr_name="dir8", joliet_path="/dir1/dir2/dir3/dir4/dir5/dir6/dir7/dir8")

    do_a_test(iso, check_rr_joliet_deep)

    iso.close()

def test_new_duplicate_child():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory("/DIR1")

def test_new_eltorito_multi_boot():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat")

    boot2str = b"boot2\n"
    iso.add_fp(BytesIO(boot2str), len(boot2str), "/boot2")
    iso.add_eltorito("/boot2", "/boot.cat")

    do_a_test(iso, check_eltorito_multi_boot)

    iso.close()

def test_new_eltorito_boot_table():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat", boot_info_table=True)

    do_a_test(iso, check_eltorito_boot_info_table)

    iso.close()

def test_new_eltorito_boot_table_large():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot"*20
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat", boot_info_table=True)

    do_a_test(iso, check_eltorito_boot_info_table_large)

    iso.close()

def test_new_hard_link():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    # Add a directory.
    iso.add_directory("/DIR1")

    iso.add_hard_link(iso_new_path="/DIR1/FOO.;1", iso_old_path="/FOO.;1")

    do_a_test(iso, check_hard_link)

    iso.close()

def test_new_invalid_interchange():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(interchange_level=5)

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(interchange_level=0)

def test_new_open_twice():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new()

    iso.close()

def test_new_add_fp_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

def test_new_add_fp_no_rr_name():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

def test_new_add_fp_rr_name():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

def test_new_add_fp_no_joliet_name():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    do_a_test(iso, check_onefile_joliet_no_file)

    iso.close()

def test_new_add_fp_joliet_name():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.close()

def test_new_add_fp_joliet_name_too_long():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/"+'a'*65)

    iso.close()

def test_new_add_dir_joliet_name_too_long():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory("/DIR1", joliet_path="/"+'a'*65)

    iso.close()

def test_new_close_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.close()

def test_new_rm_isohybrid_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_isohybrid()

def test_new_add_isohybrid_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_isohybrid()

def test_new_add_isohybrid_bad_boot_load_size():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    isolinux_fp = open('/bin/ls', 'rb')
    iso.add_fp(isolinux_fp, os.fstat(isolinux_fp.fileno()).st_size, "/ISOLINUX.BIN;1")
    iso.add_eltorito("/ISOLINUX.BIN;1", "/BOOT.CAT;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_isohybrid()

    iso.close()

def test_new_add_isohybrid_bad_file_signature():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    isolinux_fp = open('/bin/ls', 'rb')
    iso.add_fp(isolinux_fp, os.fstat(isolinux_fp.fileno()).st_size, "/ISOLINUX.BIN;1")
    iso.add_eltorito("/ISOLINUX.BIN;1", "/BOOT.CAT;1", boot_load_size=4)
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_isohybrid()

    iso.close()

def test_new_add_eltorito_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/ISOLINUX.BIN;1", "/BOOT.CAT;1", boot_load_size=4)

def test_new_add_file(tmpdir):
    # Now open up the ISO with pycdlib and check some things out.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a new file.

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")

    iso.add_file(str(testout), "/FOO.;1")

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_add_file_twoleveldeep(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add new directory.
    iso.add_directory("/DIR1")
    iso.add_directory("/DIR1/SUBDIR1")
    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")
    iso.add_file(str(testout), "/DIR1/SUBDIR1/FOO.;1")

    do_a_test(iso, check_twoleveldeepfile)

    iso.close()

def test_new_rr_symlink_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_symlink("/SYM.;1", "sym", "foo")

def test_new_rr_symlink_no_rr():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_symlink("/SYM.;1", "sym", "foo")

    iso.close()

def test_new_rr_symlink_absolute():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_symlink("/SYM.;1", "sym", "/usr/local/foo")

    do_a_test(iso, check_rr_absolute_symlink)

    iso.close()

def test_new_add_file_no_rr_name(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_file(str(testout), "/FOO.;1")

def test_new_add_file_not_initialized(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_file(str(testout), "/FOO.;1")

def test_new_hard_link_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(iso_new_path="/DIR1/FOO.;1", iso_old_path="/FOO.;1")

def test_new_write_fp_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.write_fp(out)

def test_new_same_dirname_different_parent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    iso.new(rock_ridge="1.09", joliet=3)

    # Add new directory.
    iso.add_directory("/DIR1", rr_name="dir1", joliet_path="/dir1")
    iso.add_directory("/DIR1/BOOT", rr_name="boot", joliet_path="/dir1/boot")
    iso.add_directory("/DIR2", rr_name="dir2", joliet_path="/dir2")
    iso.add_directory("/DIR2/BOOT", rr_name="boot", joliet_path="/dir2/boot")

    do_a_test(iso, check_same_dirname_different_parent)

    iso.close()

def test_new_joliet_isolevel4():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4, joliet=3)
    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/foo", joliet_path="/foo")
    # Add new directory.
    iso.add_directory("/dir1", joliet_path="/dir1")

    do_a_test(iso, check_joliet_isolevel4)

    iso.close()

def test_new_eltorito_hide():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")
    iso.rm_hard_link(iso_path="/BOOT.CAT;1")

    do_a_test(iso, check_eltorito_nofiles_hide)

    iso.close()

def test_new_eltorito_nofiles_hide_joliet():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")
    iso.rm_hard_link(joliet_path="/boot.cat")
    iso.rm_hard_link(iso_path="/BOOT.CAT;1")

    do_a_test(iso, check_joliet_and_eltorito_nofiles_hide)

    iso.close()

def test_new_eltorito_nofiles_hide_joliet_only():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")
    # After add_fp:
    #  boot - 1 link (1 Joliet)
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")
    # After add_eltorito:
    #  boot - 1 link (1 Joliet, eltorito initial entry is "special")
    #  boot.cat - 1 link (1 Joliet)
    iso.rm_hard_link(joliet_path="/boot.cat")
    # After rm_hard_link:
    #  boot - 1 link (1 Joliet, eltorito initial entry is "special")
    #  boot.cat - 0 links (ISO only)

    do_a_test(iso, check_joliet_and_eltorito_nofiles_hide_only)

    iso.close()

def test_new_eltorito_nofiles_hide_iso_only():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")
    iso.rm_hard_link(iso_path="/BOOT.CAT;1")

    do_a_test(iso, check_joliet_and_eltorito_nofiles_hide_iso_only)

    iso.close()

def test_new_hard_link_reshuffle():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.add_hard_link(iso_new_path="/BAR.;1", iso_old_path="/FOO.;1")

    do_a_test(iso, check_hard_link_reshuffle)

    iso.close()

def test_new_invalid_sys_ident():
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(sys_ident='a'*33)

def test_new_invalid_vol_ident():
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(vol_ident='a'*33)

def test_new_seqnum_greater_than_set_size():
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(seqnum=99)

def test_new_invalid_vol_set_ident():
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(vol_set_ident='a'*129)

def test_new_invalid_app_use():
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(app_use='a'*513)

def test_new_invalid_app_use_xa():
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(xa=True, app_use='a'*142)

def test_new_invalid_filename_character():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FO#.;1")

def test_new_invalid_filename_semicolons():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FO0;1.;1")

def test_new_invalid_filename_version():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;32768")

def test_new_invalid_filename_dotonly():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/.")

def test_new_invalid_filename_toolong():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/THISISAVERYLONGNAME.;1")

def test_new_invalid_extension_toolong():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/NAME.LONGEXT;1")

def test_new_invalid_dirname():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a directory.
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory("/")

def test_new_invalid_dirname_toolong():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a directory.
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory("/THISISAVERYLONGDIRECTORY")

def test_new_invalid_dirname_toolong4():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3)
    # Add a directory.
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory("/"+"a"*208)

def test_new_rr_invalid_name(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_file(str(testout), "/FOO.;1", rr_name="foo/bar")

def test_new_hard_link_invalid_keyword(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")

    iso.add_file(str(testout), "/FOO.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(foo='bar')

def test_new_hard_link_no_eltorito():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(boot_catalog_old=True)

def test_new_hard_link_no_old_kw(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")

    iso.add_file(str(testout), "/FOO.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(iso_new_path='/FOO.;1')

def test_new_hard_link_no_new_kw(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")

    iso.add_file(str(testout), "/FOO.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(iso_old_path='/FOO.;1')

def test_new_hard_link_new_missing_rr(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    testout = tmpdir.join("writetest.iso")
    with open(str(testout), 'wb') as outfp:
        outfp.write(b"foo\n")

    iso.add_file(str(testout), "/FOO.;1", rr_name="foo")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(iso_old_path='/FOO.;1', iso_new_path="/BAR.;1")

def test_new_hard_link_eltorito():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.rm_hard_link("/BOOT.CAT;1")
    iso.add_hard_link(boot_catalog_old=True, iso_new_path="/BOOT.CAT;1")

    do_a_test(iso, check_eltorito_nofiles)

    iso.close()

def test_new_rm_hard_link_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link()

def test_new_rm_hard_link_no_path():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link()

def test_new_rm_hard_link_both_paths():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link(iso_path="/BOOT.;1", joliet_path="/boot")

def test_new_rm_hard_link_bad_path():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link(iso_path="BOOT.;1")

def test_new_rm_hard_link_dir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add a directory.
    iso.add_directory("/DIR1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link(iso_path="/DIR1")

def test_new_rm_hard_link_no_joliet():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link(joliet_path="/boot")

def test_new_rm_hard_link_remove_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")

    iso.rm_hard_link(iso_path="/BOOT.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_rm_hard_link_joliet_remove_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")

    iso.rm_hard_link(iso_path="/BOOT.;1")
    iso.rm_hard_link(joliet_path="/boot")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_rm_hard_link_rm_second():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAR.;1")
    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAZ.;1")

    iso.rm_hard_link(iso_path="/BAR.;1")
    iso.rm_hard_link(iso_path="/BAZ.;1")

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_rm_hard_link_rm_joliet_first():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.rm_hard_link(joliet_path="/foo")
    iso.rm_hard_link(iso_path="/FOO.;1")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_rm_hard_link_rm_joliet_and_links():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")
    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAR.;1")
    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAZ.;1")

    iso.rm_hard_link(joliet_path="/foo")
    iso.rm_hard_link(iso_path="/BAR.;1")
    iso.rm_hard_link(iso_path="/BAZ.;1")
    iso.rm_hard_link(iso_path="/FOO.;1")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_rm_hard_link_isolevel4():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.rm_hard_link(iso_path="/FOO.;1")

    do_a_test(iso, check_isolevel4_nofiles)

    iso.close()

def test_add_hard_link_joliet_to_joliet():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")
    iso.add_hard_link(joliet_old_path="/foo", joliet_new_path="/bar")

    iso.close()

def test_new_rr_deeper():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory('/DIR1', rr_name='dir1')
    iso.add_directory('/DIR1/DIR2', rr_name='dir2')
    iso.add_directory('/DIR1/DIR2/DIR3', rr_name='dir3')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4', rr_name='dir4')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5', rr_name='dir5')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6', rr_name='dir6')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7', rr_name='dir7')
    iso.add_directory('/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/DIR8', rr_name='dir8')

    iso.add_directory('/A1', rr_name='a1')
    iso.add_directory('/A1/A2', rr_name='a2')
    iso.add_directory('/A1/A2/A3', rr_name='a3')
    iso.add_directory('/A1/A2/A3/A4', rr_name='a4')
    iso.add_directory('/A1/A2/A3/A4/A5', rr_name='a5')
    iso.add_directory('/A1/A2/A3/A4/A5/A6', rr_name='a6')
    iso.add_directory('/A1/A2/A3/A4/A5/A6/A7', rr_name='a7')
    iso.add_directory('/A1/A2/A3/A4/A5/A6/A7/A8', rr_name='a8')

    do_a_test(iso, check_rr_deeper_dir)

    iso.close()

def test_new_eltorito_boot_table_large_odd():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boo"*27
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat", boot_info_table=True)

    do_a_test(iso, check_eltorito_boot_info_table_large_odd)

    iso.close()

def test_new_joliet_large_directory():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    for i in range(1, 50):
        iso.add_directory("/DIR%d" % i, joliet_path="/dir%d" % i)

    do_a_test(iso, check_joliet_large_directory)

    iso.close()

def test_new_zero_byte_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=1)

    foostr = b""
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/BAR.;1")

    do_a_test(iso, check_zero_byte_file)

    iso.close()

def test_new_eltorito_hide_boot():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.rm_hard_link(iso_path="/BOOT.;1")

    do_a_test(iso, check_eltorito_hide_boot)

    iso.close()

def test_new_full_path_from_dirrecord():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/DIR1/BOOT.;1")

    full_path = None
    for child in iso.list_children(iso_path="/DIR1"):
        if child.file_identifier() == b"BOOT.;1":
            full_path = iso.full_path_from_dirrecord(child)
            assert(full_path == b"/DIR1/BOOT.;1")
            break

    assert(full_path is not None)
    iso.close()

def test_new_full_path_from_dirrecord_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.full_path_from_dirrecord(None)

def test_new_eltorito_no_joliet_bootcat():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", joliet_path="/boot")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", joliet_bootcatfile=None)

    iso.close()

def test_new_rock_ridge_one_point_twelve():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.12")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot")

    iso.close()

def test_new_duplicate_pvd():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.duplicate_pvd()

    do_a_test(iso, check_duplicate_pvd)

    iso.close()

def test_new_duplicate_pvd_not_initialized():
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.duplicate_pvd()

def test_new_eltorito_multi_multi_boot():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat")

    boot2str = b"boot2\n"
    iso.add_fp(BytesIO(boot2str), len(boot2str), "/boot2")
    iso.add_eltorito("/boot2", "/boot.cat")

    boot3str = b"boot3\n"
    iso.add_fp(BytesIO(boot3str), len(boot3str), "/boot3")
    iso.add_eltorito("/boot3", "/boot.cat")

    do_a_test(iso, check_eltorito_multi_multi_boot)

    iso.close()

def test_new_duplicate_pvd_not_same(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.duplicate_pvd()

    indir = tmpdir.mkdir('duplicatepvdnotsame')
    outfile = str(indir) + '.iso'

    iso.write(outfile)

    iso.close()

    with open(outfile, 'r+b') as changefp:
        # Back up to the application use portion of the duplicate PVD to make
        # it different than the primary one.  The duplicate PVD lives at extent
        # 17, so go to extent 18, backup 653 (to skip the zeros), then backup
        # one more to get back into the application use area.
        changefp.seek(18*2048 - 653 - 1)
        changefp.write(b'\xff')

    iso2 = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidISO):
        iso2.open(outfile)

def infinitenamechecks(iso, filesize):
    dr = iso.pvd.root_dir_record.children[2]
    assert(len(dr.rock_ridge.dr_entries.nm_records) == 1)
    assert(dr.rock_ridge.dr_entries.nm_records[0].posix_name == b"a"*172)
    assert(dr.rock_ridge.dr_entries.nm_records[0].posix_name_flags == 1)

    assert(dr.rock_ridge.dr_entries.ce_record is not None)
    assert(len(dr.rock_ridge.ce_entries.nm_records) == 2)
    assert(dr.rock_ridge.ce_entries.nm_records[0].posix_name == b"a"*250)
    assert(dr.rock_ridge.ce_entries.nm_records[0].posix_name_flags == 1)
    assert(dr.rock_ridge.ce_entries.nm_records[1].posix_name == b"a"*78)
    assert(dr.rock_ridge.ce_entries.nm_records[1].posix_name_flags == 0)

def test_new_rr_exceedinglylongname():
    # This is a test to test out names > 255 in pycdlib.  Note that the Linux
    # kernel doesn't support this (nor does genisoimage), so this is strictly
    # an internal-only test to make sure we get things correct.

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*500)

    do_a_test(iso, infinitenamechecks)

    iso.close()

def symlink_path_checks(iso, size):
    assert(iso.pvd.root_dir_record.children[3].rock_ridge.symlink_path() == b"aaaaaaaa")

def test_new_rr_symlink_path():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="aaaaaaaa")

    iso.add_symlink("/BBBBBBBB.;1", "bbbbbbbb", "aaaaaaaa")

    do_a_test(iso, symlink_path_checks)

    iso.close()

def test_new_rr_symlink_path_not_symlink():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="aaaaaaaa")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.pvd.root_dir_record.children[2].rock_ridge.symlink_path()

def verylongsymlinkchecks(iso, size):
    assert(iso.pvd.root_dir_record.children[3].rock_ridge.symlink_path() == b"a"*RR_MAX_FILENAME_LENGTH)

def test_new_rr_verylongnameandsymlink_symlink_path():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="a"*RR_MAX_FILENAME_LENGTH)

    iso.add_symlink("/BBBBBBBB.;1", "b"*RR_MAX_FILENAME_LENGTH, "a"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, verylongsymlinkchecks)

    iso.close()

def verylong_symlink_path_checks(iso, size):
    assert(iso.pvd.root_dir_record.children[3].rock_ridge.symlink_path() == b"a"*RR_MAX_FILENAME_LENGTH)

def test_new_rr_verylongsymlink_symlink_path():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="aaaaaaaa")

    iso.add_symlink("/BBBBBBBB.;1", "bbbbbbbb", "a"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, verylong_symlink_path_checks)

    iso.close()

def extremelylong_symlink_path_checks(iso, size):
    assert(iso.pvd.root_dir_record.children[3].rock_ridge.symlink_path() == b"a"*500)

def test_new_rr_extremelylongsymlink_symlink_path():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", rr_name="aaaaaaaa")

    iso.add_symlink("/BBBBBBBB.;1", "bbbbbbbb", "a"*500)

    do_a_test(iso, extremelylong_symlink_path_checks)

    iso.close()

def test_new_rr_invalid_rr_version():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(rock_ridge="1.90")

def test_new_rr_onefile_onetwelve():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.12")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    do_a_test(iso, check_rr_onefile_onetwelve)

    iso.close()

def test_new_set_hidden_file():
    iso = pycdlib.PyCdlib()
    iso.new()

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1")
    iso.set_hidden("/AAAAAAAA.;1")

    do_a_test(iso, check_hidden_file)

    iso.close()

def test_new_set_hidden_dir():
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")
    iso.set_hidden("/DIR1")

    do_a_test(iso, check_hidden_dir)

    iso.close()

def test_new_set_hidden_joliet_file():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", joliet_path="/aaaaaaaa")
    iso.set_hidden(joliet_path="/aaaaaaaa")

    do_a_test(iso, check_hidden_joliet_file)

    iso.close()

def test_new_set_hidden_joliet_dir():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")
    iso.set_hidden(joliet_path="/dir1")

    do_a_test(iso, check_hidden_joliet_dir)

    iso.close()

def test_new_set_hidden_rr_onefileonedir():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")
    iso.set_hidden(rr_path="/foo")

    iso.add_directory("/DIR1", rr_name="dir1")
    iso.set_hidden(rr_path="/dir1")

    do_a_test(iso, check_rr_onefileonedir_hidden)

    iso.close()

def test_new_clear_hidden_joliet_file():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")
    iso.clear_hidden(joliet_path="/foo")

    do_a_test(iso, check_joliet_onefile)

    iso.close()

def test_new_clear_hidden_joliet_dir():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")
    iso.clear_hidden(joliet_path="/dir1")

    do_a_test(iso, check_joliet_onedir)

    iso.close()

def test_new_clear_hidden_rr_onefileonedir():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")
    iso.clear_hidden(rr_path="/foo")

    iso.add_directory("/DIR1", rr_name="dir1")
    iso.clear_hidden(rr_path="/dir1")

    do_a_test(iso, check_rr_onefileonedir)

    iso.close()

def test_new_set_hidden_not_initialized():
    iso = pycdlib.PyCdlib()
    iso.new()

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1")
    iso.close()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.set_hidden("/AAAAAAAA.;1")

def test_new_clear_hidden_file():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    iso.clear_hidden("/FOO.;1")

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_clear_hidden_dir():
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")
    iso.clear_hidden("/DIR1")

    do_a_test(iso, check_onedir)

    iso.close()

def test_new_clear_hidden_not_initialized():
    iso = pycdlib.PyCdlib()
    iso.new()

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1")
    iso.close()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.clear_hidden("/AAAAAAAA.;1")

def test_new_duplicate_rrmoved_name():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/A", rr_name="A")
    iso.add_directory("/A/B", rr_name="B")
    iso.add_directory("/A/B/C", rr_name="C")
    iso.add_directory("/A/B/C/D", rr_name="D")
    iso.add_directory("/A/B/C/D/E", rr_name="E")
    iso.add_directory("/A/B/C/D/E/F", rr_name="F")
    iso.add_directory("/A/B/C/D/E/F/G", rr_name="G")
    iso.add_directory("/A/B/C/D/E/F/G/1", rr_name="1")

    iso.add_directory("/A/B/C/D/E/F/H", rr_name="H")
    iso.add_directory("/A/B/C/D/E/F/H/1", rr_name="1")

    firststr = b"first\n"
    iso.add_fp(BytesIO(firststr), len(firststr), "/A/B/C/D/E/F/G/1/FIRST.;1", rr_name="first")

    secondstr = b"second\n"
    iso.add_fp(BytesIO(secondstr), len(secondstr), "/A/B/C/D/E/F/H/1/SECOND.;1", rr_name="second")

    do_a_test(iso, check_rr_two_dirs_same_level)

    iso.close()

def test_new_eltorito_hd_emul():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x01\x01\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    do_a_test(iso, check_eltorito_hd_emul)

    iso.close()

def test_new_eltorito_hd_emul_too_short():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    iso.close()

def test_new_eltorito_hd_emul_bad_keybyte1():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x01\x01\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x56' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    iso.close()

def test_new_eltorito_hd_emul_bad_keybyte2():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x01\x01\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xab'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    iso.close()

def test_new_eltorito_hd_emul_multiple_part():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x01\x01\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00\x01\x01\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    iso.close()

def test_new_eltorito_hd_emul_no_part():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    iso.close()

def test_new_eltorito_hd_emul_bad_sec():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x00\x00\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    do_a_test(iso, check_eltorito_hd_emul_bad_sec)

    iso.close()

def test_new_eltorito_hd_emul_invalid_geometry():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul')

    do_a_test(iso, check_eltorito_hd_emul_invalid_geometry)

    iso.close()

def test_new_eltorito_hd_emul_not_bootable():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*446 + b"\x00\x01\x01\x00\x02\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00" + b"\x00"*16 + b"\x00"*16 + b"\x00"*16 + b'\x55' + b'\xaa'
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='hdemul', bootable=False)

    do_a_test(iso, check_eltorito_hd_emul_not_bootable)

    iso.close()

def test_new_eltorito_floppy12():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*(2400*512)
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='floppy', bootable=True)

    do_a_test(iso, check_eltorito_floppy12)

    iso.close()

def test_new_eltorito_floppy144():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*(2880*512)
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='floppy', bootable=True)

    do_a_test(iso, check_eltorito_floppy144)

    iso.close()

def test_new_eltorito_floppy288():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*(5760*512)
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='floppy', bootable=True)

    do_a_test(iso, check_eltorito_floppy288)

    iso.close()

def test_new_eltorito_bad_floppy():
    iso = pycdlib.PyCdlib()

    iso.new(interchange_level=1)

    bootstr = b"\x00"*(576*512)
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1", media_name='floppy', bootable=True)

    iso.close()

def test_new_eltorito_multi_hidden():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat")

    boot2str = b"boot2\n"
    iso.add_fp(BytesIO(boot2str), len(boot2str), "/boot2")
    iso.add_eltorito("/boot2", "/boot.cat")

    iso.rm_hard_link(iso_path="/boot2")

    do_a_test(iso, check_eltorito_multi_hidden)

    iso.close()

def test_new_eltorito_rr_verylongname():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")
    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot")

    iso.add_eltorito("/BOOT.;1", "/AAAAAAAA.;1", rr_bootcatname="a"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_eltorito_rr_verylongname)

    iso.close()

def test_new_isohybrid_file_before():
    # Create a new ISO
    iso = pycdlib.PyCdlib()
    iso.new()
    # Add Eltorito
    isolinuxstr = b'\x00'*0x40 + b'\xfb\xc0\x78\x70'
    iso.add_fp(BytesIO(isolinuxstr), len(isolinuxstr), "/ISOLINUX.BIN;1")
    iso.add_eltorito("/ISOLINUX.BIN;1", "/BOOT.CAT;1", boot_load_size=4)
    # Now add the syslinux data
    iso.add_isohybrid()

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    do_a_test(iso, check_isohybrid_file_before)

    iso.close()

def test_new_force_consistency_not_initialized():
    # Create a new ISO
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.force_consistency()

def test_new_eltorito_rr_joliet_verylongname():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09", joliet=3)
    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1", rr_name="boot", joliet_path="/boot")

    iso.add_eltorito("/BOOT.;1", "/AAAAAAAA.;1", rr_bootcatname="a"*RR_MAX_FILENAME_LENGTH, joliet_bootcatfile='/'+'a'*64)

    do_a_test(iso, check_eltorito_rr_joliet_verylongname)

    iso.close()

def test_new_joliet_dirs_overflow_ptr_extent():
    numdirs = 216

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    for i in range(1, 1+numdirs):
        iso.add_directory("/DIR%d" % i, joliet_path="/dir%d" % i)

    do_a_test(iso, check_joliet_dirs_overflow_ptr_extent)

    iso.close()

def test_new_joliet_dirs_just_short_ptr_extent():
    numdirs = 215

    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    for i in range(1, 1+numdirs):
        iso.add_directory("/DIR%d" % i, joliet_path="/dir%d" % i)

    do_a_test(iso, check_joliet_dirs_just_short_ptr_extent)

    iso.close()

def test_new_joliet_rm_large_directory():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    for i in range(1, 50):
        iso.add_directory("/DIR%d" % i, joliet_path="/dir%d" % i)

    for i in range(1, 50):
        iso.rm_directory("/DIR%d" % i, joliet_path="/dir%d" % i)

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_overflow_root_dir_record():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o']:
        thisstr = b'\n'
        iso.add_fp(BytesIO(thisstr), len(thisstr), "/"+letter.upper()*7+'.;1', rr_name=letter*20, joliet_path="/"+letter*20)

    do_a_test(iso, check_overflow_root_dir_record)

    iso.close()

def test_new_overflow_correct_extents():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    thisstr = b'\n'
    for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']:
        iso.add_fp(BytesIO(thisstr), len(thisstr), "/"+letter.upper()*8+'.;1', rr_name=letter*136, joliet_path="/"+letter*64)

    iso.add_fp(BytesIO(thisstr), len(thisstr), "/OOOOOOOO.;1", rr_name='o'*57, joliet_path="/"+'o'*57)

    iso.add_fp(BytesIO(thisstr), len(thisstr), "/P.;1", rr_name='p', joliet_path="/p")

    do_a_test(iso, check_overflow_correct_extents)

    iso.close()

def test_new_overflow_correct_extents2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    thisstr = b'\n'

    iso.add_fp(BytesIO(thisstr), len(thisstr), "/P.;1", rr_name='p', joliet_path="/p")

    iso.add_fp(BytesIO(thisstr), len(thisstr), "/OOOOOOOO.;1", rr_name='o'*57, joliet_path="/"+'o'*57)

    for letter in ['n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']:
        iso.add_fp(BytesIO(thisstr), len(thisstr), "/"+letter.upper()*8+'.;1', rr_name=letter*136, joliet_path="/"+letter*64)

    do_a_test(iso, check_overflow_correct_extents)

    iso.close()

def test_new_duplicate_deep_dir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    iso.add_directory("/BOOKS", rr_name="books", joliet_path="/books")
    iso.add_directory("/BOOKS/LKHG", rr_name="lkhg", joliet_path="/books/lkhg")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW", rr_name="HyperNews", joliet_path="/books/lkhg/HyperNews")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET", rr_name="get", joliet_path="/books/lkhg/HyperNews/get")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/FS", rr_name="fs", joliet_path="/books/lkhg/HyperNews/get/fs")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/FS/FS", rr_name="fs", joliet_path="/books/lkhg/HyperNews/get/fs/fs")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/FS/FS/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/fs/fs/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG", rr_name="khg", joliet_path="/books/lkhg/HyperNews/get/khg")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/117", rr_name="117", joliet_path="/books/lkhg/HyperNews/get/khg/117")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/117/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/117/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/117/1/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/117/1/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/117/1/1/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/117/1/1/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/117/1/1/1/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/117/1/1/1/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/35", rr_name="35", joliet_path="/books/lkhg/HyperNews/get/khg/35")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/35/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/35/1")
    iso.add_directory("/BOOKS/LKHG/HYPERNEW/GET/KHG/35/1/1", rr_name="1", joliet_path="/books/lkhg/HyperNews/get/khg/35/1/1")

    do_a_test(iso, check_duplicate_deep_dir)

    iso.close()

def test_new_always_consistent():
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new(joliet=3)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.rm_hard_link(joliet_path="/foo")

    iso.add_directory("/DIR1", joliet_path="/dir1")

    iso.rm_hard_link(iso_path="/FOO.;1")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.rm_file("/FOO.;1", joliet_path="/foo")

    iso.rm_directory("/DIR1", joliet_path="/dir1")

    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")
    iso.add_eltorito("/FOO.;1", "/BOOT.CAT;1")

    iso.rm_eltorito()

    do_a_test(iso, check_joliet_onefile)

    iso.close()

def test_new_remove_eighth_dir():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/DIR1", rr_name="dir1")
    iso.add_directory("/DIR1/DIR2", rr_name="dir2")
    iso.add_directory("/DIR1/DIR2/DIR3", rr_name="dir3")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4", rr_name="dir4")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5", rr_name="dir5")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6", rr_name="dir6")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7", rr_name="dir7")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/DIR8", rr_name="dir8")

    iso.rm_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/DIR8", rr_name="dir8")

    do_a_test(iso, check_sevendeepdirs)

    iso.close()

def test_new_joliet_level_1():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=1)

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_joliet_level_2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=2)

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_joliet_level_3():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_joliet_invalid_level():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.new(joliet=4)

def test_new_duplicate_pvd_always_consistent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.duplicate_pvd()

    do_a_test(iso, check_duplicate_pvd)

    iso.close()

def test_new_rr_symlink_always_consistent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    iso.add_symlink("/SYM.;1", "sym", "foo")

    do_a_test(iso, check_rr_symlink)

    iso.close()

def test_new_eltorito_always_consistent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    do_a_test(iso, check_eltorito_nofiles)

    iso.close()

def test_new_joliet_false():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=False)

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_joliet_true():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=True)

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_eltorito_multi_boot_always_consistent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat")

    boot2str = b"boot2\n"
    iso.add_fp(BytesIO(boot2str), len(boot2str), "/boot2")
    iso.add_eltorito("/boot2", "/boot.cat")

    do_a_test(iso, check_eltorito_multi_boot)

    iso.close()

def test_new_rm_joliet_hard_link():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.rm_hard_link(joliet_path="/foo")

    do_a_test(iso, check_onefile_joliet_no_file)

    iso.close()

def test_new_add_joliet_directory_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_joliet_directory('/foo')

def test_new_add_joliet_directory():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1")
    iso.add_joliet_directory("/dir1")

    do_a_test(iso, check_joliet_onedir)

    iso.close()

def test_new_add_joliet_directory_isolevel4():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4, joliet=3)
    # Add new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/foo", joliet_path="/foo")
    # Add new directory.
    iso.add_directory("/dir1")
    iso.add_joliet_directory("/dir1")

    do_a_test(iso, check_joliet_isolevel4)

    iso.close()

def test_new_add_joliet_directory_always_consistent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new(joliet=3)

    iso.add_directory("/DIR1")
    iso.add_joliet_directory("/dir1")

    do_a_test(iso, check_joliet_onedir)

    iso.close()

def test_new_rm_joliet_directory():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    iso.rm_directory("/DIR1")
    iso.rm_joliet_directory("/dir1")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_rm_joliet_directory_not_initialized():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_joliet_directory("/dir1")

def test_new_rm_joliet_directory_always_consistent():
    # Create a new ISO.
    iso = pycdlib.PyCdlib(always_consistent=True)
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    iso.rm_directory("/DIR1")
    iso.rm_joliet_directory("/dir1")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_rm_joliet_directory_iso_level4():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4, joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    iso.rm_directory("/DIR1")
    iso.rm_joliet_directory("/dir1")

    do_a_test(iso, check_joliet_isolevel4_nofiles)

    iso.close()

def test_new_deep_rr_symlink():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a large directory structure.
    iso.add_directory("/DIR1", rr_name="dir1")
    iso.add_directory("/DIR1/DIR2", rr_name="dir2")
    iso.add_directory("/DIR1/DIR2/DIR3", rr_name="dir3")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4", rr_name="dir4")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5", rr_name="dir5")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6", rr_name="dir6")
    iso.add_directory("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7", rr_name="dir7")

    iso.add_symlink("/DIR1/DIR2/DIR3/DIR4/DIR5/DIR6/DIR7/SYM.;1", "sym", "/usr/share/foo")

    do_a_test(iso, check_deep_rr_symlink)

    iso.close()

def test_new_rr_deep_weird_layout():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/ASTROID", rr_name="astroid")
    iso.add_directory("/ASTROID/ASTROID", rr_name="astroid")
    iso.add_directory("/ASTROID/ASTROID/TESTS", rr_name="tests")
    iso.add_directory("/ASTROID/ASTROID/TESTS/TESTDATA", rr_name="testdata")
    iso.add_directory("/ASTROID/ASTROID/TESTS/TESTDATA/PYTHON3", rr_name="python3")
    iso.add_directory("/ASTROID/ASTROID/TESTS/TESTDATA/PYTHON3/DATA", rr_name="data")
    iso.add_directory("/ASTROID/ASTROID/TESTS/TESTDATA/PYTHON3/DATA/ABSIMP", rr_name="absimp")
    iso.add_directory("/ASTROID/ASTROID/TESTS/TESTDATA/PYTHON3/DATA/ABSIMP/SIDEPACK", rr_name="sidepackage")

    strstr = b"from __future__ import absolute_import, print_functino\nimport string\nprint(string)\n"
    iso.add_fp(BytesIO(strstr), len(strstr), "/ASTROID/ASTROID/TESTS/TESTDATA/PYTHON3/DATA/ABSIMP/STRING.PY;1", rr_name="string.py")

    initstr = b'"""a side package with nothing in it\n"""\n'
    iso.add_fp(BytesIO(initstr), len(initstr), "/ASTROID/ASTROID/TESTS/TESTDATA/PYTHON3/DATA/ABSIMP/SIDEPACK/__INIT__.PY;1", rr_name="__init__.py")

    do_a_test(iso, check_rr_deep_weird_layout)

    iso.close()

def test_new_rr_long_dir_name():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/AAAAAAAA", rr_name="a"*248)

    do_a_test(iso, check_rr_long_dir_name)

    iso.close()

def test_new_rr_out_of_order_ce():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_symlink("/SYM.;1", "sym", "/".join(["a"*RR_MAX_FILENAME_LENGTH, "b"*RR_MAX_FILENAME_LENGTH, "c"*RR_MAX_FILENAME_LENGTH, "d"*RR_MAX_FILENAME_LENGTH, "e"*RR_MAX_FILENAME_LENGTH]))
    iso.add_directory("/AAAAAAAA", rr_name="a"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_rr_out_of_order_ce)

    iso.close()

def test_new_rr_ce_removal():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/AAAAAAAA", rr_name="a"*RR_MAX_FILENAME_LENGTH)
    iso.add_directory("/BBBBBBBB", rr_name="b"*RR_MAX_FILENAME_LENGTH)
    iso.add_directory("/CCCCCCCC", rr_name="c"*RR_MAX_FILENAME_LENGTH)
    iso.add_directory("/DDDDDDDD", rr_name="d"*RR_MAX_FILENAME_LENGTH)

    iso.rm_directory("/CCCCCCCC", rr_name="c"*RR_MAX_FILENAME_LENGTH)

    iso.add_directory("/EEEEEEEE", rr_name="e"*RR_MAX_FILENAME_LENGTH)

    do_a_test(iso, check_rr_ce_removal)

    iso.close()

def test_new_duplicate_pvd_joliet():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.duplicate_pvd()

    do_a_test(iso, check_duplicate_pvd_joliet)

    iso.close()

def test_new_write_fp_not_binary(tmpdir):
    # Create a new ISO.
    iso = pycdlib.PyCdlib()

    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        with open(os.path.join(str(tmpdir), 'out.iso'), 'w') as outfp:
            iso.write_fp(outfp)

    iso.close()

def test_new_add_directory_no_path():
    iso = pycdlib.PyCdlib()

    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory()

    iso.close()

def test_new_add_directory_joliet_only():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1")
    iso.add_directory(joliet_path="/dir1")

    do_a_test(iso, check_joliet_onedir)

    iso.close()

def test_new_rm_directory_no_path():
    iso = pycdlib.PyCdlib()

    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_directory()

    iso.close()

def test_new_rm_directory_joliet_only():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_joliet_directory(joliet_path="/dir1")
    iso.rm_directory(joliet_path="/dir1")

    do_a_test(iso, check_joliet_nofiles)

    iso.close()

def test_new_get_and_write_dir():
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_and_write_fp("/DIR1", out)

    iso.close()

def test_new_get_record_not_initialized():
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_record()

def test_new_get_record_invalid_kwarg():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_record(foo='bar')

    iso.close()

def test_new_get_record_multiple_paths():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_record(iso_path='/bar', joliet_path='/bar')

    iso.close()

def test_new_get_record_joliet_path():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    rec = iso.get_record(joliet_path="/dir1")

    assert(rec.file_identifier().decode('utf-16_be') == 'dir1')
    assert(len(rec.children) == 2)

    iso.close()

def test_new_get_record_iso_path():
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")

    rec = iso.get_record(iso_path="/DIR1")

    assert(rec.file_identifier() == b'DIR1')
    assert(len(rec.children) == 2)

    iso.close()

def test_new_get_record_rr_path():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory("/DIR1", rr_name="dir1")

    rec = iso.get_record(rr_path="/dir1")

    assert(rec.file_identifier() == b'DIR1')
    assert(len(rec.children) == 2)
    assert(rec.rock_ridge.name() == b"dir1")

    iso.close()

def test_new_different_joliet_name():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3, rock_ridge="1.09")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo", joliet_path="/bar")

    foojstr = b"foojoliet\n"
    iso.add_fp(BytesIO(foojstr), len(foojstr), "/FOOJ.;1", rr_name="fooj", joliet_path="/foo")

    do_a_test(iso, check_joliet_different_names)

    # Check that we can get the content for the first file using its various names
    out = BytesIO()
    iso.get_file_from_iso_fp(out, iso_path="/FOO.;1")
    assert(out.getvalue() == b"foo\n")

    out2 = BytesIO()
    iso.get_file_from_iso_fp(out2, rr_path="/foo")
    assert(out2.getvalue() == b"foo\n")

    out3 = BytesIO()
    iso.get_file_from_iso_fp(out3, joliet_path="/bar")
    assert(out3.getvalue() == b"foo\n")

    # Check that we can get the content for the second file using its various names
    out4 = BytesIO()
    iso.get_file_from_iso_fp(out4, iso_path="/FOOJ.;1")
    assert(out4.getvalue() == b"foojoliet\n")

    out5 = BytesIO()
    iso.get_file_from_iso_fp(out5, rr_path="/fooj")
    assert(out5.getvalue() == b"foojoliet\n")

    out6 = BytesIO()
    iso.get_file_from_iso_fp(out6, joliet_path="/foo")
    assert(out6.getvalue() == b"foojoliet\n")

    iso.close()

def test_new_different_rr_isolevel4_name():
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4, rock_ridge="1.09")

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/foo", rr_name="bar")

    barstr = b"bar\n"
    iso.add_fp(BytesIO(barstr), len(barstr), "/bar", rr_name="foo")

    out = BytesIO()
    iso.get_file_from_iso_fp(out, iso_path="/foo")
    assert(out.getvalue() == b"foo\n")

    out2 = BytesIO()
    iso.get_file_from_iso_fp(out2, rr_path="/bar")
    assert(out2.getvalue() == b"foo\n")

    iso.close()

def test_new_get_file_from_iso_fp_not_initialized():
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp('foo')

def test_new_get_file_from_iso_fp_invalid_keyword():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp('junk', foo='bar')

def test_new_get_file_from_iso_fp_too_many_args():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp('junk', iso_path='/bar', rr_path='/bar')

def test_new_list_children_not_initialized():
    iso = pycdlib.PyCdlib()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children():
            pass

def test_new_list_children_too_few_args():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children():
            pass

    iso.close()

def test_new_list_children_too_many_args():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children(iso_path='/foo', rr_path='/bar'):
            pass

    iso.close()

def test_new_list_children_invalid_arg():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children(foo='bar'):
            pass

    iso.close()

def test_new_list_children_joliet():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory(joliet_path="/dir1")

    for index,c in enumerate(iso.list_children(joliet_path='/')):
        if index == 2:
            assert(c.file_identifier() == "dir1".encode('utf-16_be'))

    assert(index == 2)

    iso.close()

def test_new_list_children_rr():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory(iso_path="/DIR1", rr_name="dir1")

    for index,c in enumerate(iso.list_children(rr_path='/')):
        if index == 2:
            assert(c.file_identifier() == b"DIR1")
            assert(c.rock_ridge.name() == b"dir1")

    assert(index == 2)

    iso.close()

def test_new_list_children():
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory(iso_path="/DIR1")

    for index,c in enumerate(iso.list_children(iso_path='/')):
        if index == 2:
            assert(c.file_identifier() == b"DIR1")

    assert(index == 2)

    iso.close()

def test_new_list_dir_joliet():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory("/DIR1", joliet_path="/dir1")

    for index,c in enumerate(iso.list_dir("/", joliet=True)):
        if index == 2:
            assert(c.file_identifier() == 'dir1'.encode('utf-16_be'))

    assert(index == 2)

    iso.close()

def test_new_get_file_from_iso_invalid_path():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, iso_path="/FOO.;1/BAR.;1")

    iso.close()

def test_new_get_file_from_iso_invalid_joliet_path():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, joliet_path="/foo/bar")

    iso.close()

def test_new_get_file_from_iso_joliet_path_not_absolute():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, joliet_path="foo")

    iso.close()

def test_new_get_file_from_iso_joliet_path_not_found():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, joliet_path="/bar")

    iso.close()

def test_new_get_file_from_iso_blocksize():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    out = BytesIO()
    iso.get_file_from_iso_fp(out, joliet_path="/foo", blocksize=16384)

    assert(out.getvalue() == b'foo\n')

    iso.close()

def test_new_get_file_from_iso_no_joliet():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, joliet_path="/foo")

    iso.close()

def test_new_get_file_from_iso_no_rr():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, rr_path="/foo")

    iso.close()

def test_new_set_hidden_no_paths():
    iso = pycdlib.PyCdlib()
    iso.new()

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.set_hidden()

    iso.close()

def test_new_clear_hidden_no_paths():
    iso = pycdlib.PyCdlib()
    iso.new()

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.clear_hidden()

    iso.close()

def test_new_set_hidden_too_many_paths():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", joliet_path="/aaaaaaaa")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.set_hidden(iso_path='/AAAAAAAA.;1', joliet_path='/aaaaaaaa')

    iso.close()

def test_new_clear_hidden_too_many_paths():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    aastr = b"aa\n"
    iso.add_fp(BytesIO(aastr), len(aastr), "/AAAAAAAA.;1", joliet_path="/aaaaaaaa")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.clear_hidden(iso_path='/AAAAAAAA.;1', joliet_path='/aaaaaaaa')

    iso.close()

def test_new_add_directory_with_mode():
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory(iso_path="/DIR1", file_mode=0o040555)

    iso.close()

def test_new_full_path_from_dirrecord_root():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    fullpath = iso.full_path_from_dirrecord(iso.pvd.root_directory_record())
    assert(fullpath == b'/')

    iso.close()

def test_new_full_path_rockridge():
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    iso.add_directory(iso_path="/DIR1", rr_name="dir1")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/DIR1/BOOT.;1", rr_name="boot")

    full_path = None
    for child in iso.list_children(rr_path="/dir1"):
        if child.file_identifier() == b"BOOT.;1":
            full_path = iso.full_path_from_dirrecord(child, rockridge=True)
            assert(full_path == b"/dir1/boot")
            break

    assert(full_path is not None)
    iso.close()

def test_new_list_children_joliet_subdir():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    iso.add_directory(iso_path="/DIR1", joliet_path="/dir1")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/DIR1/BOOT.;1", joliet_path="/dir1/boot")

    full_path = None
    for child in iso.list_children(joliet_path="/dir1"):
        if child.file_identifier() == "boot".encode('utf-16_be'):
            full_path = iso.full_path_from_dirrecord(child)
            assert(full_path == "/dir1/boot".encode('utf-16_be'))
            break

    assert(full_path is not None)
    iso.close()

def test_new_joliet_encoded_system_identifier():
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4, joliet=3, rock_ridge="1.09", sys_ident='LINUX', vol_ident='cidata')

    user_data_str = b"""\
#cloud-config
password: password
chpasswd: { expire: False }
ssh_pwauth: True
"""
    iso.add_fp(BytesIO(user_data_str), len(user_data_str), "/user-data", rr_name="user-data", joliet_path="/user-data")

    meta_data_str = b"""\
local-hostname: cloudimg
"""
    iso.add_fp(BytesIO(meta_data_str), len(meta_data_str), "/meta-data", rr_name="meta-data", joliet_path="/meta-data")

    do_a_test(iso, check_joliet_ident_encoding)

    iso.close()

def test_new_duplicate_pvd_isolevel4():
    # 51200 without interchange_level 4, without duplicate_pvd
    # 53248 without interchange level 4, with duplicate pvd
    # 55296 with interchange level 4, with duplicate pvd
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.duplicate_pvd()

    do_a_test(iso, check_duplicate_pvd_isolevel4)

    iso.close()

def test_new_joliet_hidden_iso_file():
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    iso.rm_hard_link(iso_path="/FOO.;1")

    do_a_test(iso, check_joliet_hidden_iso_file)

    iso.close()

def test_new_add_file_hard_link_rm_file():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/LINK.;1")

    iso.rm_file("/FOO.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_file_mode_not_rock_ridge():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", file_mode=0o0100444)

    iso.close()

def test_new_eltorito_hide_boot_link():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")
    iso.add_hard_link(iso_old_path="/BOOT.;1", iso_new_path="/BOOTLINK.;1")
    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    iso.rm_hard_link(iso_path="/BOOT.;1")

    do_a_test(iso, check_eltorito_bootlink)

    iso.close()

def test_new_iso_only_add_rm_hard_link():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAR.;1")

    iso.rm_hard_link("/BAR.;1")

    iso.rm_file("/FOO.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_rm_hard_link_twice():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAR.;1")

    iso.rm_hard_link(iso_path="/BAR.;1")
    iso.rm_hard_link(iso_path="/FOO.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_rm_hard_link_twice2():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    iso.add_hard_link(iso_old_path="/FOO.;1", iso_new_path="/BAR.;1")

    iso.rm_hard_link(iso_path="/FOO.;1")
    iso.rm_hard_link(iso_path="/BAR.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

def test_new_rm_eltorito_leave_file():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.add_eltorito("/FOO.;1", "/BOOT.CAT;1")

    iso.rm_eltorito()

    do_a_test(iso, check_onefile)

    iso.close()

def test_new_add_eltorito_rm_file():
    iso = pycdlib.PyCdlib()
    iso.new()

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/BOOT.;1")

    iso.add_eltorito("/BOOT.;1", "/BOOT.CAT;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_file("/BOOT.;1")

    iso.close()

def test_new_eltorito_multi_boot_rm_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/boot")
    iso.add_eltorito("/boot", "/boot.cat")

    boot2str = b"boot2\n"
    iso.add_fp(BytesIO(boot2str), len(boot2str), "/boot2")
    iso.add_eltorito("/boot2", "/boot.cat")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_file("/boot2")

    iso.close()

def test_new_get_file_from_iso_symlink():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(rock_ridge="1.09")

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", rr_name="foo")

    iso.add_symlink("/SYM.;1", "sym", "foo")

    out = BytesIO()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, iso_path="/SYM.;1")

    iso.close()

def test_new_udf_nofiles():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    do_a_test(iso, check_udf_nofiles)

    iso.close()

def test_new_udf_onedir():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")

    do_a_test(iso, check_udf_onedir)

    iso.close()

def test_new_udf_twodirs():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")
    iso.add_directory("/DIR2", udf_path="/dir2")

    do_a_test(iso, check_udf_twodirs)

    iso.close()

def test_new_udf_subdir():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")
    iso.add_directory("/DIR1/SUBDIR1", udf_path="/dir1/subdir1")

    do_a_test(iso, check_udf_subdir)

    iso.close()

def test_new_udf_subdir_odd():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")
    iso.add_directory("/DIR1/SUBDI1", udf_path="/dir1/subdi1")

    do_a_test(iso, check_udf_subdir_odd)

    iso.close()

def test_new_udf_rm_directory():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")
    iso.rm_directory("/DIR1", udf_path="/dir1")

    do_a_test(iso, check_udf_nofiles)

    iso.close()

def test_new_udf_onefile():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    do_a_test(iso, check_udf_onefile)

    iso.close()

def test_new_udf_onefileonedir():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    iso.add_directory("/DIR1", udf_path="/dir1")

    do_a_test(iso, check_udf_onefileonedir)

    iso.close()

def test_new_udf_rm_file():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    iso.rm_file("/FOO.;1", udf_path="/foo")

    do_a_test(iso, check_udf_nofiles)

    iso.close()

def test_new_udf_dir_spillover():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    for i in range(ord('a'), ord('v')):
        iso_dirname = "/" + chr(i).upper() * 8
        udf_dirname = "/" + chr(i) * 64
        iso.add_directory(iso_dirname, udf_path=udf_dirname)

    do_a_test(iso, check_udf_dir_spillover)

    iso.close()

def test_new_udf_dir_oneshort():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    for i in range(ord('a'), ord('u')):
        iso_dirname = "/" + chr(i).upper() * 8
        udf_dirname = "/" + chr(i) * 64
        iso.add_directory(iso_dirname, udf_path=udf_dirname)

    do_a_test(iso, check_udf_dir_oneshort)

    iso.close()

def test_new_udf_iso_hidden():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    iso.rm_hard_link(iso_path="/FOO.;1")

    do_a_test(iso, check_udf_iso_hidden)

    iso.close()

def test_new_udf_hard_link():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    iso.add_hard_link(iso_old_path="/FOO.;1", udf_new_path="/foo")

    do_a_test(iso, check_udf_onefile)

    iso.close()

def test_new_udf_rm_add_hard_link():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    iso.rm_hard_link(iso_path="/FOO.;1")

    iso.add_hard_link(udf_old_path="/foo", iso_new_path="/FOO.;1")

    do_a_test(iso, check_udf_onefile)

    iso.close()

def test_new_udf_hidden():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    iso.rm_hard_link(udf_path="/foo")

    do_a_test(iso, check_udf_hidden)

    iso.close()

@pytest.mark.slow
def test_new_very_largefile(tmpdir):
    indir = tmpdir.mkdir("verylarge")
    largefile = os.path.join(str(indir), 'bigfile')

    with open(largefile, 'w') as outfp:
        outfp.truncate(5*1024*1024*1024)  # 5 GB

    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3)

    # Add a new file.
    iso.add_file(largefile, "/BIGFILE.;1")

    do_a_test(iso, check_very_largefile)

    iso.close()

    os.unlink(largefile)

@pytest.mark.slow
def test_new_rm_very_largefile(tmpdir):
    indir = tmpdir.mkdir("rmverylarge")
    largefile = os.path.join(str(indir), 'bigfile')

    with open(largefile, 'w') as outfp:
        outfp.truncate(5*1024*1024*1024)  # 5 GB

    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3)

    # Add a new file.
    iso.add_file(largefile, "/BIGFILE.;1")

    iso.rm_file("/BIGFILE.;1")

    do_a_test(iso, check_nofiles)

    iso.close()

    os.unlink(largefile)

@pytest.mark.slow
def test_new_udf_very_large(tmpdir):
    indir = tmpdir.mkdir("udfverylarge")
    largefile = os.path.join(str(indir), 'foo')

    with open(largefile, 'wb') as outfp:
        outfp.truncate(1073739776+1)

    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=1, udf=True)

    # Add a new file.
    iso.add_file(largefile, "/FOO.;1", udf_path='/foo')

    do_a_test(iso, check_udf_very_large)

    iso.close()

    os.unlink(largefile)

def test_new_lookup_after_rmdir():
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")

    rec = iso.get_record(iso_path="/DIR1")
    assert(rec.file_identifier() == b'DIR1')
    assert(len(rec.children) == 2)

    iso.rm_directory("/DIR1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        rec = iso.get_record(iso_path="/DIR1")

    iso.close()

def test_new_lookup_after_rmfile():
    iso = pycdlib.PyCdlib()
    iso.new()

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    rec = iso.get_record(iso_path="/FOO.;1")
    assert(rec.file_identifier() == b'FOO.;1')
    assert(len(rec.children) == 0)

    iso.rm_file("/FOO.;1")
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        rec = iso.get_record(iso_path="/FOO.;1")

    iso.close()

def test_new_udf_lookup_after_rmdir():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")

    rec = iso.get_record(udf_path="/dir1")

    iso.rm_directory("/DIR1", udf_path="/dir1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        rec = iso.get_record(udf_path="/dir1")

    iso.close()

def test_new_udf_lookup_after_rmfile():
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    # Add a new file.
    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    rec = iso.get_record(udf_path="/foo")

    iso.rm_file("/FOO.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        rec = iso.get_record(udf_path="/foo")

    iso.close()

def test_new_full_path_no_rr():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")
    rec = iso.get_record(iso_path="/FOO.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        name = iso.full_path_from_dirrecord(rec, True)

    iso.close()

def test_new_list_children_udf():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")

    bootstr = b"boot\n"
    iso.add_fp(BytesIO(bootstr), len(bootstr), "/DIR1/BOOT.;1", udf_path="/dir1/boot")

    full_path = None
    for child in iso.list_children(udf_path="/dir1"):
        if child is not None:
            if child.file_identifier() == b"boot":
                break
    else:
        assert(false)

    iso.close()

def test_new_udf_list_children_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children(udf_path="/foo"):
            pass

    iso.close()

def test_new_list_children_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children(iso_path="/FOO.;1"):
            pass

    iso.close()

def test_new_list_children_joliet_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(joliet=3)

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", joliet_path="/foo")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        for c in iso.list_children(joliet_path="/foo"):
            pass

    iso.close()

def test_new_udf_remove_base():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_directory(udf_path="/")

    iso.close()

def test_new_remove_udf_path_not_udf():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    iso.add_directory("/DIR1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_directory(udf_path="/dir1")

    iso.close()

def test_new_add_dir_udf_path_not_udf():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_directory(udf_path="/dir1")

    iso.close()

def test_new_rm_link_udf_path_not_udf():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link(udf_path="/foo")

    iso.close()

def test_new_rm_link_udf_path_not_file():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new(udf=True)

    iso.add_directory("/DIR1", udf_path="/dir1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.rm_hard_link(udf_path="/dir1")

    iso.close()

def test_new_add_link_udf_path_not_udf():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_hard_link(iso_old_path="/FOO.;1", udf_new_path="/foo")

    iso.close()

def test_new_add_fp_udf_path_not_udf():
    # Create a new ISO.
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1", udf_path="/foo")

    iso.close()

def test_new_get_file_from_iso_fp_udf_path_not_udf():
    iso = pycdlib.PyCdlib()
    iso.new()

    foostr = b"foo\n"
    iso.add_fp(BytesIO(foostr), len(foostr), "/FOO.;1")

    out = BytesIO()
    with pytest.raises(pycdlib.pycdlibexception.PyCdlibInvalidInput):
        iso.get_file_from_iso_fp(out, udf_path='/foo')

    iso.close()
