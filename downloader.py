#!/usr/bin/python2.7
import requests


def main():
    url = 'https://s3.amazonaws.com/pydemo/test.zip'
    for cnt in range(4):
        session = requests.Session()
        print "getting %d..." % cnt
        r = session.get(url, stream=True)
        with open('/tmp/%d-test.zip' % cnt, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # filter out keep-alive new chunks
                if chunk:
                    f.write(chunk)
                    f.flush()

if __name__ == '__main__':
    main()
