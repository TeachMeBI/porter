curl --request POST 'http://localhost:11451/api/v2/delete?org=business&bucket=inteligence' \
  --header 'Authorization: Token xjfCw89Dk_9fjzvPv604PAj2IEofmnJ7v_l4XcS374jPV_TCJMhxaOJzfYyd5q6W93WUbOUJb8bSGLeZ1EkMaw==' \
  --header 'Content-Type: application/json' \
  --data '{
    "start": "2023-03-01T00:00:00Z",
    "stop": "2023-11-14T00:00:00Z"
  }'
