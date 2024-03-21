clean:
	rm -f my_cool_job*
	rm -rf log_test	
submit:
	python submitter.py
	
gather:
	python gatherer.py
