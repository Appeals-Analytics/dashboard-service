from api.dashboard import DashboardApi
from api.messages import MessagesApi
from api.files import FilesApi


class ApiClient(DashboardApi, MessagesApi, FilesApi):
  pass


__all__ = ["ApiClient"]
