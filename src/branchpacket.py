import json
from enum import Enum

class BranchStatus(Enum):
    UNUSED_1 =              100
    OK =                    200
    UNUSED_2 =              300
    REQUEST_FAILURE =       400
    INTERNAL_SERVER_ERROR = 500
    UNUSED_3 =              600

class BranchRequest():
    
    @staticmethod
    def from_json(json_str: str):
        try:
            json_obj = json.loads(json_str)
        except Exception as ex:
            raise TypeError("Not a valid BranchPacket")

        try:
            command = json_obj["command"]
            payload = json_obj["payload"]
            return BranchRequest(command, payload)
        except KeyError:
            raise TypeError("Not a valid BranchPacket")

    def __init__(self, command, payload):
        self.command: str = command
        self.payload: any = payload
    
    def as_dict(self) -> dict:
        return {
            "command": self.command,
            "payload": self.payload
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

class BranchResponse():

    @staticmethod
    def from_json(json_str: str):
        try:
            json_obj = json.loads(json_str)
        except Exception as ex:
            raise TypeError("Not a valid BranchPacket")
        
        try:
            statuscode = json_obj["statuscode"]
            payload = json_obj["payload"]
            return BranchResponse(BranchStatus(statuscode), payload)
        except KeyError:
            raise TypeError("Not a valid BranchPacket")

    def __init__(self, statuscode: BranchStatus, payload):
        if(not isinstance(statuscode, BranchStatus)):
            raise TypeError("Statuscode is not a BranchStatus object")

        self.statuscode: BranchStatus = statuscode
        self.payload: any = payload
    
    def as_dict(self) -> dict:
        return {
                "statuscode": self.statuscode.value,
                "payload": self.payload
        }

    def as_json(self) -> str:
        return json.dumps(self.as_dict())
