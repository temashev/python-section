import enum
from dataclasses import dataclass
from abc import ABC, abstractmethod


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class BaseParser(ABC):
    @abstractmethod
    def parse(self, message: JsonMessage) -> ParsedMessage:
        pass


class TelegramParser(BaseParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        ## TODO: логика парсинга из Telegram
        return ParsedMessage()


class SlackParser(BaseParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        ## TODO: логика парсинга из Slack
        return ParsedMessage()


class MattermostParser(BaseParser):
    def parse(self, message: JsonMessage) -> ParsedMessage:
        ## TODO: логика парсинга из Mattermost
        return ParsedMessage()


class ParserFactory:
    parsers = {
        MessageType.TELEGRAM: TelegramParser,
        MessageType.SLACK: SlackParser,
        MessageType.MATTERMOST: MattermostParser
    }

    @classmethod
    def get_parser(cls, message_type: MessageType) -> BaseParser:
        parser_class = cls.parsers.get(message_type)
        if parser_class is None:
            raise ValueError(f'Неизвестный тип {message_type}')

        return parser_class()
