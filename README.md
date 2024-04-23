**<h1> RedSky is the simple Framework to build ASGI Application </h1>**
**<h2> You can use APIRouter to implement endpoints </h2>**
```python
from redsky import APIRouter

router = APIRouter(prefix='/prefix')

@router.get(path='/json')
async def json_ping():
    return JsonRespose(status_code=200, body='pong')


@router.get(path='/html')
async def html_ping():
    return HtmlRespose(status_code=200, body='<h1> pong </h1>')
```
**<h2> Do not forget include routers into the app</h2>**
```python
app: RedSky
app.include_router(router)
```
**<h2> Use JsonResponse, HtmlResponse or response from another Framework <br>
JsonResponse.body waiting for ```string``` or ```dict``` <br>
HtmlResponse.body waiting for valid ```html```</h2>**
```python
from redsky.responses import JsonResponse, HtmlResponse
```
**<h2> You can set or delete cookie </h2>**
```python
response.set_cookie('key', 'value', http_only=True, max_age=123)
response.delete_cookie('test')
```
**<h2> To pass request object in your function just declare request param in signature with redsky.request.Request hint<br>
To pass path params just declare it </h2>**

```python
from redsky.request import Request


@rotuer.get('/{param_1}/{param_2}}')
async def ping(
        request: Request,
        param_1: str,
        param_2: str,
):
    print(request)
    print(param_1)
    print(param_2)
```

**<h2> You need asgi server to run application, e.g uvicorn </h2>**

```python
import uvicorn
from redsky import RedSky

app = RedSky()
uvicorn.run(app, host='0.0.0.0', port=8000)
```
