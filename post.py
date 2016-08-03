from time import sleep
from piston.steem import Steem
import os


steem = Steem(wif=os.environ['STEEM_POSTING_KEY'])
USER = 'noisy2'
permlink = 'some-permlink-to-post'
title = 'SWP test test test test test test adsasd'

body = '''
Few sentences about translation process, description, etc.

# Content to translate

{content}

# Links

- link1
- link2

'''

file_summary = '''
## {filename}

```
{filecontent}
```

'''


proj_dir = '/home/noisy/Devel/steem-whitepaper/'

files_to_translate = [
    'whitepaper/abstract.asc',
    'whitepaper/01-introduction/1-introduction.asc',
    'whitepaper/01-introduction/sections/recognizing-contribution.asc',
]

content = ''
files = []

for filename in files_to_translate:
    with open(os.path.join(proj_dir, filename)) as f:
        filecontent = f.read()
        content += file_summary.format(filename=filename, filecontent=filecontent)
        files.append((filename, filecontent))

post_body = body.format(content=content)

print(post_body)
p = steem.post(title=title, body=post_body, permlink=permlink, author=USER, category='test')
post_id = '@{user}/{permlink}'.format(user=USER, permlink=permlink)

c = steem.get_content(post_id)

line_counter = 0
for filename, filecontent in files:
    for line in filecontent.split('\n'):
        if line and line.strip():
            line_counter += 1
            comment = '{} - ```{}```'.format(line_counter, line)
            print(comment)
            print(c.reply(comment, author=USER))
            sleep(19)

print('end')
