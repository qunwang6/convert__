#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from apple_dictionary.apple_entry_plugin import AppleEntryPlugin
from lxml import etree

# import pdb

parser = etree.XMLParser( recover=True )

class UnderscoreEntryPlugin( AppleEntryPlugin ):
	"""
	замена preparse и postparse
	"""
	def __init__( self ):
		super( UnderscoreEntryPlugin, self ).__init__()
		# переопределяем значение суперкласса
		self.escapeXML = False

		self.file = None
		self.tree = None
		self.articles = []
		self.categories = []

	def read( self, f ):
		'''
		plugin.read( f )
			-> tuple( title, entry )
			-> None // в случае неудачи
		'''
		if not self.file:
			self.file = f
			self.parse_file()
			header, body = self.front_page()
		else:
			if len( self.articles ) + len( self.categories ) > 0:
				if len( self.articles ) > 0:
					art = self.articles.pop()
					header = art[ 0 ].xpath( './b[@class="header"]' )[ 0 ].text

				elif len( self.categories ) > 0:
					art = self.categories.pop()
					header = art[ 0 ].text

				body = u''.join(
					map( lambda t: etree.tostring(
						t,
						method="xml",
						pretty_print=True,
						encoding='unicode',
						xml_declaration=False
					), art )
				).replace( u'index.html#', u'' )
			else:
				return None
		return header, body.replace( 'docs/underscore.html', 'http://underscorejs.org/docs/underscore.html' )


	def parse_file( self ):
		# пропустить !doctype
		self.file.readline()

		global parser
		self.tree = etree.parse( self.file, parser )

		root = self.tree.getroot()
		docs = root.xpath(r'.//*[@id="documentation"]')[0]
		ps = docs.xpath( "./p[@id]" )

		# индикатор конца списка статей
		stop = False

		for p in ps:
			el = p
			
			# набор последовательно идущих тегов
			article = [ el ]

			while stop != True:
				el = el.getnext()
				# только p, pre, но не p[id], потому что это уже следующая статья
				if el != None and	\
						el.tag.lower() in ( 'p', 'pre' ) and		\
						not ( el.tag == 'p' and ( 'id' in el.attrib )):
					article.append( el )
				else:
					# заголовок <h2 id="links"> означает, что пора остановиться
					if el != None and \
							el.tag == 'h2' and \
							'id' in el.attrib and \
							el.attrib['id'] == 'links':
						stop = True
					break
			self.articles.append( article )

		# #sidebar > a + ul

		sidebar = self.tree.getroot().xpath( './/*[@id="sidebar"]' )[ 0 ]
		self.categories = [ 				\
			( x, x.getnext() )					\
			for x in sidebar.xpath( './a' ) 		\
			if x.getnext() != None and x.getnext().tag == 'ul'	\
		]
		return

	def front_page( self ):
		body = u''.join( map( lambda cat: u''.join(
			map( lambda t: etree.tostring(
				t,
				method="xml",
				pretty_print=True,
				encoding='unicode',
				xml_declaration=False
			), cat )
		), self.categories )).replace( u'index.html#', u'' )

		return u'_', body
