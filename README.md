# JwtAuthentication

1.To register user
endpoint : http://127.0.0.1:8000/api/register/
data:
{
  "name":"Ram",
  "email":"ram@gmail.com",
  "phone_number":"9841839087",
  "password":"saugat"
}
2.To login
endpoint : http://127.0.0.1:8000/api/login/
data: 
{
  "phone_number":"9841839087",
  "password":"saugat"
}
3. To get new access token
endpoint:http://127.0.0.1:8000/api/refresh/
  data:
  {
  "refresh":"Your refresh token"
  }
4.get user from acess token
endpoint: http://127.0.0.1:8000/api/user/
data:
{
  "access": "your access token"
}
