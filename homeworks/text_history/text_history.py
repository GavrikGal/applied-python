from abc import ABCMeta, abstractmethod


class TextHistory:
    def __init__(self):
        self._text_history = []
        self._text_history.append(Text(''))

    @property
    def text(self):
        return self._text_history[-1].text

    @property
    def version(self):
        return self._text_history[-1].version

    def action(self, action):
        pos = action.pos
        text = action.text
        from_version = action.from_version
        to_version = action.to_version
        if isinstance(action, InsertAction):
            if pos is None:
                new_text = self.text + text
            else:
                if pos > len(self.text) or pos < 0:
                    raise ValueError()
                new_text = self.text[:pos] + text + self.text[pos:]
            self._text_history.append(Text(new_text, to_version, action))
        return self.version

    def insert(self, text, pos=None):
        cur_version = self.version
        action = InsertAction(pos=pos, text=text, from_version=cur_version, to_version=cur_version + 1)
        self.action(action)
        return self.version


class Text:
    def __init__(self, text: str, version: int = 0, action: 'Action' = None):
        self._text = text
        self._version = version
        self._action = action

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version

    @property
    def action(self):
        return self._action

    def __repr__(self):
        return str(self._version)


class Action(metaclass=ABCMeta):
    def __init__(self, pos, text, from_version=0, to_version=None):
        self.text = text
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version

    @abstractmethod
    def apply(self, text: str) -> str:
        pass


class InsertAction(Action):
    def __init__(self, pos, text, from_version=0, to_version=None):
        super().__init__(pos, text, from_version, to_version)

    def apply(self, text: str) -> str:
        pass


class ReplaceAction(Action):
    pass


class DeleteAction(Action):
    pass
