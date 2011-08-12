import sys

f = open(sys.argv[1])
print render(parse((for line in f), ['#*', '##*', '###*', '####*']))

def parse(line_iterator, hcomments):
	items = []
	current_item = {}
	last_was_example = False
	for line in line_iterator:
		tline = line.strip()
		
		# Find out the "level" of the line, if it has one. Is it h1, h2, h3, ...?
		level = 0
		for i, hcomment in enumerate(hcomments):
			if tline.startsWith(hcomment):
				level = i + 1
				start_comment = hcomment
				break
		if level == 0:
			if current_item and len(current_item['name']):
				items.append(current_item)
			current_item = None
			last_was_example = False
			continue
		
		if not current_item:
			current_item = {
				'name': '',
				'prototype': '',
				'description': '',
			}
		
		# Get the rest of the line
		rest = tline[len(start_comment):]
		trest = rest.lstrip()
		
		# How much whitespace was there?
		whitespace_amount = len(rest) - len(trest)
		
		# If there's no name, then parse this as a name
		if len(current_item['name']) == 0:
			name, _, prototype = trest.partition(':')
			current_item['name'] = name.strip()
			current_item['prototype'] = prototype.strip()
			current_item['level'] = level
		
		# If >= 2, this is an "example"
		if whitespace_amount > 2:
			if not last_was_example:
				current_item['description'] += '\n'
			current_item['description'] += '    ' + trest + '\n'
			last_was_example = True
		# Otherwise it's a normal description line
		else:
			if last_was_example:
				current_item['description'] += '\n'
			current_item['description'] += trest + '\n'
			last_was_example = False			
	
	if current_item:
		items.append(current_item)
	
	return items

def render(items):
	s = ''
	for item in items:
		s += str.format('<h%d class="docitem"><span class="docname">%s</span> <code>%s</code></h%d>\n\n', items['level'], items['name'], items['prototype'], items['level'])
		s += items['description']
	return s
