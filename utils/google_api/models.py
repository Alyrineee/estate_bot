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
        self.users = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("Пользователи"),
        )
        self.houses = self.spreadsheet.get_worksheet_by_id(
            self.topics.get("ЖК"),
        )


class UserCreation(GoogleSheets):
    def request_creation(self, data):
        index = len(self.users.get_all_values()) + 1
        self.users.update(
            f"A{index}:F{index}",
            [data],
        )

    def request_accept(self, telegram_id, status):
        row = self.users.find(telegram_id).row
        self.users.update(
            f"F{row}",
            [[status]],
        )


class AgentRequest(GoogleSheets):
    def get_houses(self):
        return self.houses.get_all_values()[1:]

    def check_number(self, number):
        number = "7" + number.replace("+", "")[1:]
        if self.clients.find(number):
            return False

        return True

    def get_house(self, house_id):
        row = self.houses.find(house_id).row
        return self.houses.row_values(row)

    def create_agent_request(self, data):
        index = len(self.clients.get_all_values()) + 1
        data.insert(0, index - 1)
        data[2] = "7" + data[2].replace("+", "")[1:]
        self.clients.update(
            f"A{index}:H{index}",
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

    def get_unverifed_clients(self):
        unverified_clients = self.clients.findall("Ожидает ответа")
        return [
            self.clients.row_values(cell.row) for cell in unverified_clients
        ]

    def get_managers(self):
        managers = self.users.findall("Оформитель")
        return [self.users.row_values(cell.row) for cell in managers]

    def get_client(self, client_id):
        row = self.clients.find(client_id).row
        return self.clients.row_values(row)


class Authenticate(GoogleSheets):
    def authenticate(self, data, permission):
        row = self.users.find(str(data))
        if permission == "base" and row is None:
            return False

        clean_data = self.users.row_values(row.row)
        if (
            permission == "agent"
            and clean_data[4] == "Агент"
            and clean_data[5] == "Активирован"
        ):
            return False
        elif (
            permission == "manager"
            and self.users.row_values(row.row)[4] == "Оформитель"
            and clean_data[5] == "Активирован"
        ):
            return False

        return True


class AdminManager(GoogleSheets):
    def get_users(self):
        return self.users.get_all_values()[1:]

    def get_clients(self):
        return self.clients.get_all_values()[1:]

    def get_client(self, client_id):
        row = self.clients.find(client_id).row
        return self.clients.row_values(row)

    def get_user(self, user_id):
        row = self.users.find(user_id).row
        return self.users.row_values(row)

    def get_houses(self):
        return self.houses.get_all_values()[1:]

    def get_house(self, house_id):
        row = self.houses.find(house_id).row
        return self.houses.row_values(row)

    def edit_house(self, index, data):
        if not index:
            index = len(self.houses.get_all_values())
            self.houses.update(
                f"A{index}:C{index}",
                [[index]],
            )
        self.houses.update(
            f"B{index}:C{index}",
            [data],
        )

    def delete_house(self, index):
        row = self.houses.find(index).row
        self.houses.delete_rows(row)
