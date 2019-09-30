import urllib2

# Nicholas Venis - 12/08/19

site = "http://cybercrime-tracker.net/all.php"
hdr = {"User-Agent": "'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

req = urllib2.Request(site,headers=hdr)


try:
    page = urllib2.urlopen(req)
    alien = page.read()
    try:
        filename = "/opt/logs/cybercrime_logs/cybercrime.log"
        with open(filename, "a+") as file:
                    file.write(alien)
                    file.close()

    except Exception as e:
        print(e)
except urllib2.HTTPError, e:
        print(e.fp.read())