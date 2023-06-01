
class CountingException(Exception):
    """
     * Class CountingException
     * Basic exception thrown in Counting processing
    """
    def __init__(self, message: str, code: int = 0, *args, **kwargs):
        self._message = message
        self._code = code
        super().__init__(*args)

    def get_message(self) -> str:
        return self._message

    def get_code(self) -> int:
        return self._code

    def __str__(self):
        return self.get_message()
