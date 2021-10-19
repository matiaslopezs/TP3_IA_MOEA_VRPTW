class ClientData(object):
    def __init__(self, client_number, x, y, demand, ready_time, due_date, service_time):
        self.client_number = client_number
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time