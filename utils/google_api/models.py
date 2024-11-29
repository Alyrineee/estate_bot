from estate_bot.config import SERVICE_ACCOUNT, SPREADSHEET_URL
import gspread


class GoogleSheets:
    def __init__(self):
        self.account = gspread.service_account(filename=SERVICE_ACCOUNT)
        self.spreadsheet = self.account.open_by_url(SPREADSHEET_URL)
        self.topics = {el.title: el.id for el in self.spreadsheet.worksheets()}
        self.clients = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Клиенты"),
        )
        self.requests = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Заявки"),
        )
        self.users = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Пользователи"),
        )
        self.houses = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("ЖК"),
        )


class UserCreation(GoogleSheets):
    def request_creation(self, data):
        index = len(self.requests.get_all_values()) + 1
        self.requests.update(
            f"A{index}:E{index}",
            [data],
        )

    def request_accept(self, telegram_id):
        row = self.requests.findall(telegram_id)[-1].row
        index = len(self.users.get_all_values()) + 1
        self.users.update(
            f"A{index}:E{index}",
            [self.requests.row_values(row)],
        )


class AgentRequest(GoogleSheets):
    def get_houses(self):
        return self.houses.get_all_values()[1:]

    def create_agent_request(self, data):
        index = len(self.clients.get_all_values()) + 1
        data.insert(0, index - 1)
        self.clients.update(
            f"A{index}:G{index}",
            [data],
        )


class ClientManager(GoogleSheets):
    def get_clients(self):
        return self.clients.get_all_values()[1:]

    def edit_status(self, index, data):
        self.clients.update(
            f"G{index+1}",
            [[data]],
        )

    def get_client(self, client_id):
        row = self.clients.find(client_id).row
        return self.clients.row_values(row)


class Authenticate(GoogleSheets):
    def authenticate(self, data, permission):
        row = self.users.find(str(data))
        if permission == "base" and row is None:
            return False
        elif (
            permission == "agent"
            and self.users.row_values(row.row)[4] == "Агент"
        ):
            return False
        elif (
            permission == "manager"
            and self.users.row_values(row.row)[4] == "Оформитель"
        ):
            return False

        return True
