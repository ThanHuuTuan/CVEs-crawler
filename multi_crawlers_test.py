import os
import sys, thread

def run(keyword):
	try:
		command = ("python CVE_crawler_keyword.py %s 2014") % (keyword)
		print command
		os.system(command)
		print "%s Done" % (keyword)
	except Exception as e:
		print e
		sys.exit(keyword)

def get_keywords(fname):
	tmp = []
	with open(fname, "r") as fin:
		for line in fin:
			if "." in line:
				s = line.split(".")[1].strip()
				keyword = "".join(s.split())
				tmp.append(keyword)
			else:
				s = line.strip()
				keyword = "".join(s.split())
				tmp.append(keyword)
	return tmp

if __name__ == "__main__":
	keywords = get_keywords("list.txt")
	for keyword in keywords:
		run(keyword)
		# try:
		# 	print keyword
		# 	thread.start_new_thread(run, (keyword,))
		# except Exception as e:
		# 	print e
		# 	sys.exit(keyword)
	