"""Skill 抽象层（skills）。"""
from abc import ABC, abstractmethod


class Skill(ABC):
    name: str
    description: str
    required_tools: list[str]

    @abstractmethod
    def build_context(self, state: dict) -> str:
        ...

    @abstractmethod
    def run(self, state: dict) -> dict:
        ...
