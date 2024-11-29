from estate_bot.config import SERVICE_ACCOUNT, SPREADSHEET_URL
import gspread


class GoogleSheets:
    def __init__(self):
        self.account = gspread.service_account(filename=SERVICE_ACCOUNT)
        self.spreadsheet = self.account.open_by_url(SPREADSHEET_URL)
        self.topics = {el.title: el.id for el in self.spreadsheet.worksheets()}


class UserCreation(GoogleSheets):
    def __init__(self):
        super().__init__()
        self.requests = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Заявки"),
        )
        self.users = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Пользователи"),
        )

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
    def __init__(self):
        super().__init__()
        self.clients = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Клиенты"),
        )
        self.houses = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("ЖК"),
        )

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
    def __init__(self):
        super().__init__()
        self.clients = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Клиенты"),
        )

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
