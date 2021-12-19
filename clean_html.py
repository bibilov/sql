import re
import html
import sqlite3

con = sqlite3.connect('works_db')
cur = con.cursor()

# очистка полей от html
info_by_id = cur.execute("SELECT ID, skills, otherInfo FROM works;")

def clean_html(string):
	# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    tagless = re.sub('<[^<]+?>', '', string)
    return html.unescape(tagless).replace('\xa0', '')

cleaned_info = {}
for row in info_by_id:
    cl_skills = clean_html(row[1])
    cl_other = clean_html(row[2])
    cleaned_info[row[0]] = (cl_skills, cl_other)

stmt = "UPDATE works SET skills = ?, otherInfo = ? WHERE ID = ?"
for k, v in cleaned_info.items():
    skills = v[0]
    other = v[1]
    cur.execute(stmt, [skills, other, k])

con.commit()
cur.close()
con.close()