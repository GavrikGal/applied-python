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
        if action.pos is None:
            action.pos = len(self.text)
        pos = action.pos
        text = action.text
        from_version = action.from_version
        to_version = action.to_version
        length = action.length

        if self.version < from_version:
            raise ValueError()
        elif pos > len(self.text) or pos < 0:
            raise ValueError()

        if isinstance(action, InsertAction):
            text = self.text[:pos] + text + self.text[pos:]

        if isinstance(action, ReplaceAction):
            text = self.text[:pos] + text + self.text[pos+len(text):]

        if isinstance(action, DeleteAction):
            if pos is None or pos + length > len(self.text):
                raise ValueError()
            text = self.text[:pos] + self.text[pos+length:]

        self._text_history.append(Text(text, to_version, action))
        return self.version

    def get_actions(self, from_version=1, to_version=None):
        if to_version is None:
            to_version = self.version
        elif to_version > self.version:
            raise ValueError()
        elif from_version > to_version:
            raise ValueError()
        if from_version < 0:
            raise ValueError()
        return [text.action for text in self._text_history if from_version < text.version <= to_version]

    def insert(self, text, pos=None):
        self.action(InsertAction(pos=pos, text=text, from_version=self.version, to_version=self.version + 1))
        return self.version

    def replace(self, text, pos=None):
        self.action(ReplaceAction(pos=pos, text=text, from_version=self.version, to_version=self.version + 1))
        return self.version

    def delete(self, pos, length):
        self.action(DeleteAction(pos=pos, length=length, from_version=self.version, to_version=self.version + 1))
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
    def __init__(self, pos, text=None, from_version=0, to_version=None, length=None):
        self.text = text
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version
        self.length = length

    @abstractmethod
    def apply(self, text: str) -> str:
        pass


class InsertAction(Action):
    def apply(self, text: str) -> str:
        pass


class ReplaceAction(Action):
    def apply(self, text: str) -> str:
        pass


class DeleteAction(Action):
    def apply(self, text: str) -> str:
        pass
