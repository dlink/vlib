#!/bin/env python
#-*- coding: utf-8 -*-

import re

def toEntity(text):
    '''Convert unicode to use XML Character Entity References
       Convert all char. above 127 to &#<num>;'
    '''
    text2 = ''
    for i, c in enumerate(text or ''):
        if ord(c) > 127:
            char_ref = '&#%i;' % ord(c)
            text2 += char_ref
        elif c == '<':
            text2 += '&lt;'
        elif c == '>':
            text2 += '&gt;'
        elif c == '&':
            text2 += '&amp;'
        else:
            text2 += c
    return text2
"""
def toEntity0(text):
    '''Obsolete.  See toEntity'''
    entities = {'\u00a0': '&#xa0;'  ,  # 
                '\u00a3': '&#xa3;'  ,  # 
                '\u00a5': '&#xa5;'  ,  # 
                '\u00a7': '&#xa7;'  ,  # 
                '\u00a9': '&#xa9;'  ,  # copyright sign (©)
                '\u00ae': '&#xae;'  ,  # 
                '\u00b0': '&#xb0;'  ,  # degree sign (°)
                '\u00b5': '&#xb5;'  ,  # 
                '\u00b6': '&#xb6;'  ,  # 
                '\u00b7': '&#xb7;'  ,  # 
                '\u00ba': '&#xba;'  ,  # 
                '\u00bc': '&#xbc;'  ,  # 
                '\u00bd': '&#xbd;'  ,  # 
                '\u00be': '&#xbe;'  ,  # 
                '\u00c9': '&#xc9;'  ,  # 
                '\u00d6': '&#xd6;'  ,  # 
                '\u00d7': '&#xd7;'  ,  # 
                '\u00e0': '&#xe0;'  ,  # 
                '\u00e1': '&#xe1;'  ,  # 
                '\u00e3': '&#xe3;'  ,  # 
                '\u00e7': '&#xe7;'  ,  # 
                '\u00e9': '&#xe9;'  ,  # e with acute (é)
                '\u00ea': '&#xea;'  ,  # 
                '\u00eb': '&#xeb;'  ,  # 
                '\u00ed': '&#xed;'  ,  # 
                '\u00ef': '&#xef;'  ,  # 
                '\u00f1': '&#xf1;'  ,  # small n with tilda (ñ)
                '\u00f2': '&#xf2;'  ,  # 
                '\u00f3': '&#xf3;'  ,  # 
                '\u00f6': '&#xf6;'  ,  # 
                '\u00f7': '&#xf7;'  ,  # 
                '\u00f8': '&#xf8;'  ,  # 
                '\u00f9': '&#xf9;'  ,  # 
                '\u00fa': '&#xfa;'  ,  # 
                '\u0394': '&#x394;' ,  #
                '\u03b1': '&#x3b1;' ,  #
                '\u03b5': '&#x3b5;' ,  #
                '\u2009': '&#x2009;',  # 
                '\u2013': '&#x2013;',  # en dash
                '\u2014': '&#x2014;',  # em dash
                '\u2018': '&#x2018;',  # left single quotation mark (‘)
                '\u2019': '&#x2019;',  # right single quotation mark (’)
                '\u201c': '&#x201c;',  # left double quotation mark
                '\u201d': '&#x201d;',  # right double quotation mark
                '\u2026': '&#x2026;',  # horizontal ellipsis                
                '\u2113': '&#x2113;',  # 
                '\u2122': '&#x2122;',  # trade mark sign (™)
                '\u2192': '&#x2192;',  # 
                '\u2197': '&#x2197;',  # 
                '\u2196': '&#x2196;',  # 
                '\u2212': '&#x2212;',  # minus sign (−)
                '\u2217': '&#x2217;',  # 
                '\u2260': '&#x2260;',  # 
                '\u2261': '&#x2261;',  # identical to (≡)
                '\u2265': '&#x2265;',  # 
                #r'&([^#])':r'&amp;\1',
                }
    return "".join(entities.get(c,c) for c in text)
    
    #for k,v in entities.items():
    #    text = re.sub(k, v, text, 100)
    #return text
"""

#def utf8(text):
#    return text.encode('utf-8')
