#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from apple_dictionary import dsl
from apple_dictionary.apple_dictionary_plugin import AppleDictionaryPlugin
from underscore_entry_plugin import UnderscoreEntryPlugin
from apple_dictionary.dsl import jing_test

import dict_template


infile = "./underscorejs.org/index.html"
xml_file = "underscore.xml"

dsl.set_app_data({
	dsl.INFILE: infile,
	dsl.OUTFILE: xml_file,
	dsl.DICTIONARY_PLUGIN_CLASS: AppleDictionaryPlugin,
	dsl.ENTRY_PLUGIN_CLASS: UnderscoreEntryPlugin
	})

dsl.convert()

try:
	jing_test.run( xml_file )
	pass
except Exception, e:
	pass
except KeyboardInterrupt, ke:
	pass

dict_template.run(
	xml_filename	= xml_file,
	plist_filename	= None,
	# prefs_filename	= 'file.html',
	# xsl_filename	= 'file.xsl',
	css_filename	= 'style.css',
	images_dir		= 'underscorejs.org/docs/images',
	display_name	= '_.js',
	identifier		= 'com.ratijas.dictionary._',
	bundle_name		= 'underscore',
	version_string	= '1.6.0'
	)
