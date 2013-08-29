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
        elif c == '&':
            text2 += '&amp;'
        else:
            text2 += c
    return text2

def toEntity0(text):
    '''Obsolete.  See toEntity'''
    entities = {u'\u00a0': '&#xa0;'  ,  # 
                u'\u00a3': '&#xa3;'  ,  # 
                u'\u00a5': '&#xa5;'  ,  # 
                u'\u00a7': '&#xa7;'  ,  # 
                u'\u00a9': '&#xa9;'  ,  # copyright sign (©)
                u'\u00ae': '&#xae;'  ,  # 
                u'\u00b0': '&#xb0;'  ,  # degree sign (°)
                u'\u00b5': '&#xb5;'  ,  # 
                u'\u00b6': '&#xb6;'  ,  # 
                u'\u00b7': '&#xb7;'  ,  # 
                u'\u00ba': '&#xba;'  ,  # 
                u'\u00bc': '&#xbc;'  ,  # 
                u'\u00bd': '&#xbd;'  ,  # 
                u'\u00be': '&#xbe;'  ,  # 
                u'\u00c9': '&#xc9;'  ,  # 
                u'\u00d6': '&#xd6;'  ,  # 
                u'\u00d7': '&#xd7;'  ,  # 
                u'\u00e0': '&#xe0;'  ,  # 
                u'\u00e1': '&#xe1;'  ,  # 
                u'\u00e3': '&#xe3;'  ,  # 
                u'\u00e7': '&#xe7;'  ,  # 
                u'\u00e9': '&#xe9;'  ,  # e with acute (é)
                u'\u00ea': '&#xea;'  ,  # 
                u'\u00eb': '&#xeb;'  ,  # 
                u'\u00ed': '&#xed;'  ,  # 
                u'\u00ef': '&#xef;'  ,  # 
                u'\u00f1': '&#xf1;'  ,  # small n with tilda (ñ)
                u'\u00f2': '&#xf2;'  ,  # 
                u'\u00f3': '&#xf3;'  ,  # 
                u'\u00f6': '&#xf6;'  ,  # 
                u'\u00f7': '&#xf7;'  ,  # 
                u'\u00f8': '&#xf8;'  ,  # 
                u'\u00f9': '&#xf9;'  ,  # 
                u'\u00fa': '&#xfa;'  ,  # 
                u'\u0394': '&#x394;' ,  #
                u'\u03b1': '&#x3b1;' ,  #
                u'\u03b5': '&#x3b5;' ,  #
                u'\u2009': '&#x2009;',  # 
                u'\u2013': '&#x2013;',  # en dash
                u'\u2014': '&#x2014;',  # em dash
                u'\u2018': '&#x2018;',  # left single quotation mark (‘)
                u'\u2019': '&#x2019;',  # right single quotation mark (’)
                u'\u201c': '&#x201c;',  # left double quotation mark
                u'\u201d': '&#x201d;',  # right double quotation mark
                u'\u2026': '&#x2026;',  # horizontal ellipsis                
                u'\u2113': '&#x2113;',  # 
                u'\u2122': '&#x2122;',  # trade mark sign (™)
                u'\u2192': '&#x2192;',  # 
                u'\u2197': '&#x2197;',  # 
                u'\u2196': '&#x2196;',  # 
                u'\u2212': '&#x2212;',  # minus sign (−)
                u'\u2217': '&#x2217;',  # 
                u'\u2260': '&#x2260;',  # 
                u'\u2261': '&#x2261;',  # identical to (≡)
                u'\u2265': '&#x2265;',  # 
                #r'&([^#])':r'&amp;\1',
                }
    return "".join(entities.get(c,c) for c in text)
    
    #for k,v in entities.items():
    #    text = re.sub(k, v, text, 100)
    #return text

#def utf8(text):
#    return text.encode('utf-8')
