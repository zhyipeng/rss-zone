from starlette.templating import Jinja2Templates

from core.setting import settings

templates = Jinja2Templates(directory=settings.TEMPLATE_PATH)
