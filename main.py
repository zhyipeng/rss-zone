from fastapi import FastAPI, HTTPException, Request, Response
from fastui import FastUI, prebuilt_html
from fastui import components as c
from starlette.responses import HTMLResponse

from core.source import FetchError
from core.templates import templates
from sources import get_sources

app = FastAPI()

srcs = get_sources()


@app.get('/')
def index():
    return HTMLResponse(prebuilt_html(title='RSS Zone'))


with open('assets/favicon.ico', 'rb') as f:
    icon = f.read()


@app.get('/favicon.ico')
async def favicon():
    return Response(content=icon, media_type='image/x-icon')


@app.get('/{key}')
async def feed(key: str, request: Request):
    src = srcs.get(key)
    if not src:
        raise HTTPException(404)

    try:
        data = await src().get_data()
    except FetchError:
        raise HTTPException(500, detail='Failed to fetch data')

    if not data:
        raise HTTPException(500, detail='Failed to fetch data')

    return templates.TemplateResponse(
        request=request,
        name='feed.html',
        context=dict(
            channel=data.channel,
            feeds=data.items,
        ),
        headers={
            'Content-Type': 'application/xml; charset=UTF-8',
            'Date': data.channel.formatted_updated,
        },
    )


@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
async def api():
    text = '\n'.join(
        [
            f'* [{s.name}](/{k}) - {s.description} [rss](/{k}) [source]({s.link})'
            for k, s in srcs.items()
        ]
    )
    return [c.Page(components=[c.Markdown(text=text)])]
