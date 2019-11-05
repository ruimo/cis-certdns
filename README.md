# cis-certdns
Create or renew SSL certificate with Lets Encrypt in IBM Cloud Internet Service(CIS) environment. Since it uses DNS-01 authentication, you do not need to execute this tool on your web server.

## Prerequisite
Install Docker.

## Environment variable

| Name | Description |
-|-
| CRN | CRN (*1) |
| ZONE_ID | Domain ID (*1) |
| API_KEY | API key (*2) |
| EMAIL | Admin email for Lets Encrypt (-m parameter for certbot) |
| HOST_NAME | Host name part for your certificate |
| DOMAIN | Domain name part for your certificate |

(*1) You can obtain CRN and Domain ID in web dash board of CIS.

(*2) You can obtain API keyin the following way:
1. Go to IBM Cloud web site.
1. Navigate Manage => Access(IAM)
1. Click on Users located left side.
1. Click on your account.
1. Goto API keys.
1. Click on 'Create an IBM Cloud API key' to obtain API key. 

## Creating certificate

Invoke createcert.sh

Example:

    $ docker run -v /etc/letsencrypt:/etc/letsencrypt -e CRN=$CRN -e ZONE_ID=$DOMAIN_ID -e EMAIL='YOUR EMAIL' -e HOST_NAME='www' -e DOMAIN='yourdomain.com' -e API_KEY=$API_KEY --rm ruimo/cis-certdns createcert.sh --staging

This creates SSL certificate for site 'www.yourdmain.com'. Your SSL certificate will be stored in /etc/letsencrypt. You can specify arguments to createcert.sh. They will be simply passed to certbot command. Since '--staging' is specified in this case, certbot will create certificate for staging.

## Wildcard certificate

You can create wildcard certification. Specify '*' for hostname and argument --server https://acme-v02.api.letsencrypt.org/directory.

Example:

    $ docker run -v /etc/letsencrypt:/etc/letsencrypt -e CRN=$CRN -e ZONE_ID=$DOMAIN_ID -e EMAIL='YOUR EMAIL' -e HOST_NAME='*' -e DOMAIN='yourdomain.com' -e API_KEY=$API_KEY --rm ruimo/cis-certdns createcert.sh --server https://acme-v02.api.letsencrypt.org/directory --staging

This create SSL certificate for site '*.yourdomain.com'. Your SSL certificate will be stored in /etc/letsencrypt. As same as before, '--staging' is specified to let certbot create certificate for staging.

## Renewing certificate

Invoke renewcert.sh

Example:

    $ docker run -v /etc/letsencrypt:/etc/letsencrypt -e CRN=$CRN -e ZONE_ID=$DOMAIN_ID -e EMAIL='YOUR MAIL ADDRESS' -e HOST_NAME='www' -e DOMAIN='yourdomain.com' -e API_KEY=$API_KEY --rm ruimo/cis-certdns renewcert.sh --staging --renew-by-default

Example(Wildcard):

    $ docker run -v /etc/letsencrypt:/etc/letsencrypt -e CRN=$CRN -e ZONE_ID=$DOMAIN_ID -e EMAIL='YOUR MAIL ADDRESS' -e HOST_NAME='*' -e DOMAIN='yourdomain.com' -e API_KEY=$API_KEY --rm ruimo/cis-certdns renewcert.sh --server https://acme-v02.api.letsencrypt.org/directory --staging --renew-by-default

This renews all certificates under /etc/letsencrypt. You can specify arguments to renewcert.sh. They will be simply passed to certbot command. Since '--staging' is specified in this case, certbot will create certificate for staging. The '--renew-by-default' 
force certbot to renew certificate always.

Once certbot renewed the certificate, it creates zero length flag file /etc/letsencrypt/certcreated. So you can check this file afterward to determine if you need to update existing certificates (such as reloading web servers).

## Logging

If you encounter any problems, try take a log by specifying -v /tmp/cis-certdns:/var/log/cis-certdns. Log will be stored in /tmp/cis-certdns in this case.
