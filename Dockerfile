FROM certbot/certbot
RUN pip install requests
ADD createcert.sh /usr/local/bin/
ADD renewcert.sh /usr/local/bin/
ADD editdns.py /usr/local/bin/
ADD editdns.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/createcert.sh
RUN chmod +x /usr/local/bin/renewcert.sh
RUN chmod +x /usr/local/bin/editdns.sh
