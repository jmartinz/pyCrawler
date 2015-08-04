import re
from bs4 import BeautifulSoup

data = """
<html>
    <head>
        <title>My Sample Page</title>
        <script>
        $.ajax({
            type: "POST",
            url: 'http://www.example.com',
            data: {
                email:'abc@g.com',
                phone:'9999999999',
                name:'XYZ'
                'viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:enlaceExpediente_0',
                'TIPO_LICITACION':'0',
                'ACTION_NAME_PARAM':'SourceAction',
                'idLicitacion':'39470418'
            }
        });
        </script>
    </head>
    <body>
        <h1>What a wonderful world</h1>
    </body>
</html>
"""

soup = BeautifulSoup(data)
script = soup.find('script')

pattern = re.compile("'(\w+)':'(.*?)'") 
fields = dict(re.findall(pattern, script.text))
#print fields['email'], fields['phone'], fields['name']
print re.findall(pattern, script.text)
