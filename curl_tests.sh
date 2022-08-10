set -eux

# man curl
#
#   -i, --include
#          (HTTP) Include the HTTP-header in the  output.  The  HTTP-header
#          includes  things  like  server-name, date of the document, HTTP-
#          version and more...
#

curl 127.0.0.1:5000/acc/api/v1.0/invoices


#curl 127.0.0.1:5000/acc/api/v1.0/invoices/123
curl 127.0.0.1:5000/acc/api/v1.0/invoices/123
#non standard: plural



# causes error:
curl -i -H "Content-Type: application/json" -X POST -d '{"who":12}' http://localhost:5000/acc/api/v1.0/invoices


#should show error 400. Invalid invoice.
curl -i -H "Content-Type: application/json" -X POST -d '{"who":"12"}' http://localhost:5000/acc/api/v1.0/invoices

curl -i -H "Content-Type: application/json" -X POST -d '{"who":4, "amount":33}' http://localhost:5000/acc/api/v1.0/invoices

# Why -H, -x, -d. All have to be there. (includeing -i?)

curl 127.0.0.1:5000/acc/api/v1.0/invoices
