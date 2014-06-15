all:
	python __init__.py; cd final/underscore; make; make install; cd ../../; killall Dictionary; sleep 1; open /Applications/Dictionary.app/

clean:
	rm -rf final
	rm *.pyc
	rm underscore.xml
