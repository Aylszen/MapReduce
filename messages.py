import enums


class Message:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.task_type = enums.TaskTypes.NONE
        self.state = enums.State.IDLE
        self.message_type = enums.MessageType.SETUP


class ResponseMessage:
    def __init__(self, response):
        self.response = response
