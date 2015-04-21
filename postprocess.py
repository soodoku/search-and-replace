#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import optparse
import csv
import fnmatch   
import logging
import codecs

# ===========================================================================================================
# Default configuration
TEXT_OUTPUT_DIR       = 'postprocessed'              # Default Postprocessed output directory
WORDLIST_FILENAME     = 'wordlist.csv'               # Word list for search and replace by regular expression
REPLACELIST_FILENAME  = 'replacelist.csv'            # World list for search and replace directly
LOGFILE               = 'postprocess.log'            # Postprocessing log file
RESUME_PP             = False                        # Skipped exist file (not Overwritten)
# ===========================================================================================================

class Logger(object):
    """Standard output wrapper class
    """
    def __init__(self, filename=LOGFILE):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.log.write(message)
        message = message.encode('utf-8', errors='ignore')
        self.terminal.write(message)
        
usage = "Usage: %prog [options] <source text directory>"
def parse_command_line(argv):
    """Command line options parser
    """
            
    parser = optparse.OptionParser(add_help_option=True, usage=usage)
    
    parser.add_option("-o", "--outdir", action="store", 
                      type="string", dest="outdir", default=TEXT_OUTPUT_DIR,
                      help="Text output directory (default: %s)" % (TEXT_OUTPUT_DIR))
    parser.add_option("-r", "--resume", action="store_true", 
                      dest="resume", default=RESUME_PP,
                      help="Resume postprocessing (Skip if existing) (default: %s)" % (RESUME_PP))
    return parser.parse_args(argv)
    
def postproc_re(text, words):
    """Returns text after post processing by regular expression
    """
    def sub_callback(m):
        old = m.group(0)
        i = int(m.groupdict(0).keys()[0][1:])
        new = words[i][0]
        if old != new:
            #print("    %s ==> %s" % (old, new))
            replace.append(old)
        return new
    
    idx = 0
    for wl in words:
        w = wl[0]
        try:
            n = int(wl[1])
        except:
            n = 2
        w = w.decode('utf-8')
        w = w.strip(u'\ufeff')
        for i in range(1, len(w) - 1):
            dc = r".{0,%d}\??[\r\n]*" % (n)
            r = re.escape(w[0:i]) + dc + re.escape(w[i+1:])
            replace = []
            p = "(?P<w%d>" % idx + r + ")"
            text = re.sub(p, sub_callback, text, flags=re.I|re.U|re.DOTALL)
            replaceset = set(replace)
            print("PP rexpr(%d): %s ==> %s" % (len(replace), r, w))
            for r in replaceset:
                print("    %s(%d)" % (r, replace.count(r)))
        idx += 1
    return text
    
def postproc_searchreplace(text, replace):
    """Returns text after post processing by search and replace list
    """        
    for a, b in replace:
        c = re.escape(a.decode('utf-8'))
        (text, n) = re.subn(c, b, text, flags=re.U)
        print("PP replace(%d): %s ==> %s" % (n, a, b))
    return text

def postproc_remove_blank_line(text):
    """Returns text after remove blank lines
    """
    (text, n) = re.subn(r'^\s*\r?\n?', '', text, flags=re.M)
    print("PP remove blank line(%d)" % (n))
    return text

def postproc_remove_hyphen(text):
    """Returns text after remove hyphen and concatenate the word is split across two lines
    """
    (text, n) = re.subn(ur'([A-Z])[\-\u00ad][\r\n]+', r'\1', text, flags=re.I|re.U)
    print("PP remove hyphen(%d)" % (n))
    return text

def getSize(filename):
    """Returns size of file
    """
    try:
        return os.path.getsize(filename)
    except:
        return 0
        
def postproc_main(options):
    """Postprocessing text file and create output file
    """
    try:
        relpath = os.path.relpath(options.filename)
    except:
        relpath = os.path.splitdrive(options.filename)[1]
    relpath = re.sub(r'^[\.|\\|\/]*', '', relpath)
    extdir = options.outdir + '/' + os.path.dirname(relpath)
    fname = extdir + '/' + os.path.basename(relpath)
    print("Postprocessing: %s" % (options.filename))
    try:
        if not os.path.exists(extdir):
            os.makedirs(extdir)
        if getSize(fname) == 0 or not options.resume:
            with open(options.filename, 'rb') as f:
                text = ''.join(f.readlines())        
            text = text.decode('utf-8', errors='ignore')
            text = postproc_remove_blank_line(text)
            text = postproc_remove_hyphen(text)
            text = postproc_searchreplace(text, options.replacelist)
            text = postproc_re(text, options.wordlist)
            with open(fname, 'wb') as f:
                f.write(text)
        else:
            print("Resume, file exist skipped")
    except:
        raise
        print("ERROR")
    
if __name__ == "__main__":
    """ Main Entry Point
    """
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sys.stdout = Logger()
    
    print("%s r6 (2013/07/08)\n" % (sys.argv[0]))

    (options, args) = parse_command_line(sys.argv)

    if len(args) < 2:
        print("Please specify root directory of Text input files (-h/--help for help)")
        sys.exit(-1)

    options.rootdir = args[1]
    
    # Read word list from file
    options.wordlist = []
    with open(WORDLIST_FILENAME, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            options.wordlist.append(row)
    
    # Read word replacement list from file
    options.replacelist = []
    with open(REPLACELIST_FILENAME, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            options.replacelist.append(row)

    # For each Text files in folder and sub-folders
    for root, dirnames, filenames in os.walk(options.rootdir):
      for filename in fnmatch.filter(filenames, '*.txt'):
          fname = os.path.join(root, filename)
          options.filename = fname
          postproc_main(options)
