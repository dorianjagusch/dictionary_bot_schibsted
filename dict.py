

cs_acronyms = {
    'CS' : 'Computer Science',
    'OOP' : 'Object-Oriented',
    'IDE' : 'Integrated Development Environment',
    'API' : 'Application Programming Interface',
    'DBMS' : 'Database Management System',
    'GUI' : 'Graphical User Interface',
    'HTTP': 'Hypertext Transfer Protocol',
    'SQL' : 'Structured Query Langage',
    'JVM' : 'Java Virtual Machine',
    'PEP' : 'Python Enhancement Proposoal' 
} 
text = "Hallo API its me"
#if (text[0] == '`' and text[-1] == '`'):
words = text.split(' ')
for word in words:
    if word in cs_acronyms:
        answer = "{word}: {cs_acronyms[word]}"
for word in words:
        if word in cs_acronyms:
            word[0] == '`' and word[-1] == '`'
            textupdate = words
client.chat_update(channel=channel_id, text=textupdate)
client.chat_postMessage(channel=channel_id, text=answer)
        #print(f"{word}: {cs_acronyms[word]}")
#    if word not in cs_acronyms:
 #       print("Acronym not found, would you like to add it to the dictionary?")