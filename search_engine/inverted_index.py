import re
import os


def process_files():
	"""
	Function that takes in all files that ends with '.txt' and returns the list of words 
	in each file.
	"""
	file_words = {}
	path="../search_engine/search_files/"
	filelist=[os.path.join(path,i) for i in os.listdir(path) if i.endswith('.txt')]
	for file in filelist:
		pattern = re.compile('[\W_]+')
		file_words[file] = open(file, 'r').read().lower();
		file_words[file] = pattern.sub(' ',file_words[file])
		file_words[file] = file_words[file].split()
	return file_words


def get_single_file_index(single_file_words):
	"""
	Function that takes in the list of word from a single file and returns the index of 
	the words in the file.

	input = [word1, word2, ...]
	output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}

	"""
	single_file_index = {}
	for index, word in enumerate(single_file_words):
		if word in single_file_index.keys():
			single_file_index[word].append(index)
		else:
			single_file_index[word] = [index]
	return single_file_index


def get_full_file_index(file_words):
	"""
	Function that takes in the full list of words from the function process_files(). 
	Then acceses the word list of each file and calls the function get_single_file_index() 
	for each word list.
	Finally combines the single_file_index returned for each file.
	Outputs the combined full_file_index.

	input = {filename: [word1, word2, ...], ...}
	result = {filename: {word: [pos1, pos2, ...]}, ...}

	"""
	full_file_index = {}
	for filename in file_words.keys():
		full_file_index[filename] = get_single_file_index(file_words[filename])
	return full_file_index


def get_full_word_index(full_file_index):
	"""
	Function to create a final full_word_index.
	Creates index list for a word which contains index of the word from all files 

	input = {filename: {word: [pos1, pos2, ...], ... }}
	result = {word: {filename: [pos1, pos2]}, ...}, ...}
	"""
	full_word_index = {}
	for filename in full_file_index.keys():
		for word in full_file_index[filename].keys():
			if word in full_word_index.keys():
				if filename in full_word_index[word].keys():
					full_word_index[word][filename].extend(full_file_index[filename][word][:])
				else:
					full_word_index[word][filename] = full_file_index[filename][word]
			else:
				full_word_index[word] = {filename: full_file_index[filename][word]}
	return full_word_index


def single_word_query(word, full_word_index):
	"""
	Function to query a single word
	"""
	pattern = re.compile('[\W_]+')
	word = pattern.sub(' ',word)
	if word in full_word_index.keys():
		return [filename for filename in full_word_index[word].keys()]
	else:
		return []


def union_text_query(string, full_word_index):
	"""
	Function to query a string.
	Union based query results.
	Returns filenames in which atleast one word of the query string is present.

	query string = 'a b c'
	result = filenames with ('a' or 'b' or 'c')

	Results are ranked based on the number of occurences of the query words in the file.
	"""
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	filenames, results = [],[]
	for word in set(string.split()):
		filenames.append(single_word_query(word,full_word_index))
	filenames = set(filenames[-1]).union(*filenames)
	for filename in filenames:
		index_count = 0 
		for word in set(string.split()):
			if single_word_query(word,full_word_index):
				if filename in full_word_index[word].keys():
					index_count += len(full_word_index[word][filename][:])
		results.append([index_count, filename])
		results.sort(reverse = True)
	return results
	

def intersection_text_query(string, full_word_index):
	"""
	Function to query a string.
	Intersection based query results.
	Returns filenames in which all words of the query string are present.

	query string = 'a b c'
	result = filenames with ('a' and 'b' and 'c')

	Results are ranked based on the number of occurences of the query words in the file.

	"""
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	filenames, results = [],[]
	for word in set(string.split()):
		filenames.append(single_word_query(word,full_word_index))
	filenames = set(filenames[-1]).intersection(*filenames)
	for filename in filenames:
		index_count = 0 
		for word in set(string.split()):
			index_count += len(full_word_index[word][filename][:])
		results.append([index_count, filename])
		results.sort(reverse = True)
	return results
	

file_words = process_files()

full_file_index = get_full_file_index(file_words)

full_word_index = get_full_word_index(full_file_index)

while True:
	print "\n\n\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
	query_string = raw_input(" Enter query string: ")

	results1 = union_text_query(query_string, full_word_index)
	print "\n\n 1.Union based search results \n ----------------------------- \n"
	if results1:
		for result in results1:		
			print result
	else:
		print " Sorry...No search results..!!!! "

	results2 = intersection_text_query(query_string, full_word_index)
	print "\n\n 2.Intersection based search results \n ------------------------------------ \n"
	if results2:
		for result in results2:
			print result
	else:
		print " Sorry...No search results..!!!! "