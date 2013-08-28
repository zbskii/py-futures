#!/usr/bin/python2.7
import futures
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession


def main():
    url = 'https://s3.amazonaws.com/pydemo/test.zip'
    async_downloads = []
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=4))
    for cnt in range(4):
        print "getting %d..." % cnt

        def cb(sess, resp, n=cnt):
            fn = '/tmp/%d-test-futures.zip' % n
            print "writing %s" % fn
            write_part(fn, resp)
            return "done with %s" % fn
        s = session.get(url,
                        stream=True,
                        timeout=10,  #!
                        background_callback=cb)

        async_downloads.append(s)
    for f in futures.as_completed(async_downloads):
        exp = f.exception()
        if exp is not None:
            raise exp
        print f.result()


def write_part(download_name, response):
        with open(download_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                # filter out keep-alive new chunks
                if chunk:
                    f.write(chunk)
                    f.flush()


if __name__ == '__main__':
    main()
