import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

cert_pattern = re.compile(r'(<!-- Certificates Column -->\s*<div id="certificates">.*?\n        </div>\n)', re.DOTALL)
hack_pattern = re.compile(r'(<!-- Hackathons Column -->\s*<div id="hackathons">.*?\n        </div>\n)', re.DOTALL)

cert_match = cert_pattern.search(content)
hack_match = hack_pattern.search(content)

if cert_match and hack_match:
    cert_text = cert_match.group(1)
    hack_text = hack_match.group(1)
    
    content = content.replace(cert_text, '___CERT_PLACEHOLDER___')
    content = content.replace(hack_text, cert_text)
    content = content.replace('___CERT_PLACEHOLDER___', hack_text)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Swapped successfully')
else:
    print('Could not find one of the sections.')
