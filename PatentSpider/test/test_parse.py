import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

# sample patent
target_url = "http://patft.uspto.gov//netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=50&f=G&l=50&co1=AND&d=PTXT&s1=H01L.CPCL.&OS=CPCL/H01L&RS=CPCL/H01L"
t1_url = "http://patft.uspto.gov//netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=41&f=G&l=50&co1=AND&d=PTXT&s1=H01L.CPCL.&OS=CPCL/H01L&RS=CPCL/H01L"
t2 = "http://patft.uspto.gov//netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=/netahtml/PTO/search-bool.html&r=48&f=G&l=50&co1=AND&d=PTXT&s1=H01L.CPCL.&OS=CPCL/H01L&RS=CPCL/H01L%27"
t3 = "http://patft.uspto.gov//netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=/netahtml/PTO/search-bool.html&r=41&f=G&l=50&co1=AND&d=PTXT&s1=H01L.CPCL.&OS=CPCL/H01L&RS=CPCL/H01L%27,"
t4 = "http://patft.uspto.gov//netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=/netahtml/PTO/search-bool.html&r=45&f=G&l=50&co1=AND&d=PTXT&s1=H01L.CPCL.&OS=CPCL/H01L&RS=CPCL/H01L%27,"
ua = UserAgent()
headers = {
    "user-agent": ua.random
}


def parse_patent_claims(url):
    print("start...")
    res = requests.get(url, headers=headers)
    source = clean_html(res.content.decode(res.encoding))
    tree = etree.HTML(source)
    text_path = "//body//br | //body//hr | //body//center//b//i | //body//center//b | //body//p"
    text_nodes = tree.xpath(text_path)
    # grab text from br that contains claims, start from "Claim" and end at "Description"
    claims = []
    abstract = ""
    description = ""
    start = False
    for i, br_hr in enumerate(text_nodes):
        if br_hr.text == "Abstract":
            start = True  # next one
        if start and br_hr.tag == "p":
            abstract = br_hr.text.strip()
            break
    start = False
    for i, br_hr in enumerate(text_nodes):
        if br_hr.text == "Claims":
            start = True  # there is one horizontal line after Claims
            text_nodes.pop(i + 1)  # remove that hrs
            text_nodes.pop(i + 2)  # remove the "what is claimed" string
        elif start and br_hr.tail:
            claims.append(br_hr.tail.strip())
            # if we get a horizontal line we terminate
            if br_hr.tag == 'hr':
                break
    # collect descriptions
    start = False
    for i, br_hr in enumerate(text_nodes[i+1:]):
        if br_hr.text == "Description":
            start = True
            text_nodes.pop(i + 1)  # remove that hrs
        elif start and br_hr.tail:
            description += br_hr.tail
    print("The abstract of this patent are: \n")
    print(abstract)
    print("The patent claims of this patent are:")
    for i in claims:
        print(i)
    print("The Descriptions of this patent are: \n")
    print(description)
    return claims


parse_patent_claims(t4)
