# templatehelper.py Copyright (c) 2005,2006 Participatory Culture Foundation
# Contains code shared by template_compiler and template

# Distutils needs this in a .py file, so it knows they're required
# by the entension module. This place seems as good as any.
import cPickle #for database.pyx

import gettext
import shutil
import re
import types
import traceback
import random
from xhtmltools import toUTF8Bytes, urlencode

HTMLPattern = re.compile("^.*<body.*?>(.*)</body\s*>", re.S)
attrPattern = re.compile("^(.*?)@@@(.*?)@@@(.*)$")
resourcePattern = re.compile("^resource:(.*)$")
rawAttrPattern = re.compile("^(.*)\*\*\*(.*?)\*\*\*(.*)$")
evalCache = {}

# Constants for the compiler and runtime function tables
# Eventually, we should eliminate these and use the actual functions
textFunc = 0
textHideFunc = 1
attrFunc = 2
addIDFunc = 3
evalEscapeFunc = 4
evalFunc = 5
includeHideFunc = 6
hideIfEmptyFunc = 7
rawAttrFunc = 8
hideSectionFunc = 9
quoteAndFillFunc = 10

def quoteattr(orig):
    return orig.replace('"','&quot;')

def escape(orig):
    return unicode(orig).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# 'key' is a key name in the template language. Resolve it relative to 'data.'
# For example, 'this feed name' might become data['this'].feed.name().
def evalKey(keyString, indata, originalKey = None, cache = False):
    global evalCache

    data = indata

    if cache and evalCache.has_key(keyString):
        return evalCache[keyString]

    # Save the original expression for use in error messages
    if originalKey is None:
        originalKey = keyString

    keys = keyString.split()

    for key in keys:
        try:
            data = data[key]
        except:
            try:
                data = getattr(data, key)
            except:
                return 'Bad Key'
            try:
                data = data()
            except:
                pass
    if cache:
        evalCache[keyString] = data
    return data

# Clears cache for evalKey
def clearEvalCache():
    global evalCache
    evalCache = {}

def toUni(orig):
    if type(orig) == types.IntType:
        return "%d" % orig
    else:
        orig = toUTF8Bytes(orig)
        return unicode(orig,'utf-8')


# Generate an arbitrary string to use as an ID attribute.
def generateId():
    return "tmplcomp%08d" % random.randint(0,99999999)

