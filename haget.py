import urllib2

# Nicholas Venis - 13/04/19

site = "https://www.hybrid-analysis.com/feed?json"
hdr = {"User-Agent": "'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

req = urllib2.Request(site,headers=hdr)


try:
    page = urllib2.urlopen(req)
    json = page.read()
    json = json.split("\n",3)[3]
    json = json[:-2]
    try:
        filename = "~/opt/logs/haanalysis_logs/halog.log"
        with open(filename, "a+") as file:
                    file.write(json)
                    file.close()

    except Exception as e:
        print(e)
except urllib2.HTTPError, e:
        print(e.fp.read())

