"""Simple memory store for user preferences and reminders."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class MemoryEntry:
    content: str
    created_at: str


@dataclass
class MemoryStore:
    path: Path
    enabled: bool = True
    _entries: List[MemoryEntry] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.enabled:
            self._entries = self._load_entries()

    def _load_entries(self) -> List[MemoryEntry]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        entries: List[MemoryEntry] = []
        for item in data.get("entries", []):
            if "content" in item and "created_at" in item:
                entries.append(MemoryEntry(item["content"], item["created_at"]))
        return entries

    def add_entry(self, content: str) -> None:
        if not self.enabled:
            return
        entry = MemoryEntry(content=content, created_at=datetime.utcnow().isoformat())
        self._entries.append(entry)
        self._persist()

    def clear(self) -> None:
        if not self.enabled:
            return
        self._entries = []
        self._persist()

    def list_entries(self) -> List[MemoryEntry]:
        return list(self._entries)

    def _persist(self) -> None:
        if not self.enabled:
            return
        payload = {"entries": [entry.__dict__ for entry in self._entries]}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def format_memory_summary(memory: MemoryStore) -> str:
    if not memory.enabled:
        return ""
    count = len(memory.list_entries())
    if count == 0:
        return ""
    return f"Memory loaded: {count} saved note(s)."
