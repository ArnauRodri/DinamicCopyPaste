import pyperclip as pc
import os


NO_OUTPUT_COMMAND: str = ' > /dev/null 2>&1'
DIR: str = './stored/'
CLEAR_COMMAND: str = 'rm ' + DIR + '*' + NO_OUTPUT_COMMAND
HEADER: str = DIR + 'dcp_stored_'
DELETE_FILE_COMMAND: str = 'rm ' + HEADER


def clear_stored() -> None:
    os.system(CLEAR_COMMAND)


class Stored:
    _store_id: int
    _empty: bool
    text: str

    def __init__(self, store_id: int) -> None:
        self._store_id = store_id
        self._empty = True
        self.text = ""

    def _read_file(self) -> None:
        with open(self.get_id(), 'r') as store_file:
            self.text = store_file.read()

    def _write_file(self) -> None:
        with open(self.get_id(), 'w') as store_file:
            store_file.write(self.text)

    def delete_file(self) -> None:
        os.system(DELETE_FILE_COMMAND + str(self._store_id) + NO_OUTPUT_COMMAND)

    def get_id(self) -> str:
        return HEADER + str(self._store_id)

    def _stored_to_paperclip(self) -> None:
        pc.copy(self.text)

    def _paperclip_to_stored(self) -> None:
        self.text = pc.paste()

    def update(self, text: str) -> None:
        self.text = text

    def load(self) -> None:
        if not self.is_empty():
            self._read_file()
            self._stored_to_paperclip()

    def unload(self) -> None:
        self._paperclip_to_stored()
        self._write_file()
        self._empty = False

    def is_empty(self) -> bool:
        return self._empty


class WindowLogic:
    _serial_id: int
    _current_stored_index: int
    stored_array: list[Stored]

    def __init__(self) -> None:
        self._serial_id = 0
        self.stored_array = []
        self._current_stored_index = 0

    def next_stored(self) -> None:
        if self._current_stored_index < len(self.stored_array):
            self._current_stored_index += 1

    def previous_stored(self) -> None:
        if self._current_stored_index > 0:
            self._current_stored_index -= 1

    def add_stored(self) -> None:
        self.stored_array.append(Stored(self._serial_id))
        self._serial_id += 1

    def is_on_add(self) -> bool:
        return self._current_stored_index == len(self.stored_array)

    def get_stored(self) -> Stored:
        return self.stored_array[self._current_stored_index]

    def remove(self) -> None:
        tmp_stored = self.get_stored()
        if not tmp_stored.is_empty():
            tmp_stored.load()
            tmp_stored.delete_file()
        self.stored_array.remove(tmp_stored)
    
    def get_index(self):
        return self._current_stored_index
