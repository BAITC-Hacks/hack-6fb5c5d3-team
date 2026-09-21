"""Терминальный FAQ-бот для репетиции."""

from pathlib import Path
import re


FAQ_FILE = Path(__file__).with_name("faq.txt")
STOP_WORDS = {
    "а", "в", "во", "и", "к", "на", "о", "об", "по", "с", "со", "что", "это",
    "ли", "мне", "для", "про", "нужен", "нужна", "будет", "есть", "как", "какая",
    "какие", "куда", "когда", "сколько",
}
WORD_STEMS = {
    "репетиция": "репетиц",
    "репетиции": "репетиц",
    "команда": "команд",
    "команды": "команд",
    "команде": "команд",
    "трек": "трек",
    "треки": "трек",
    "приз": "приз",
    "призы": "приз",
    "призах": "приз",
    "работа": "работ",
    "работу": "работ",
    "работы": "работ",
}


def words(text: str) -> set[str]:
    """Возвращает значимые слова в нижнем регистре."""
    return {
        WORD_STEMS.get(word, word)
        for word in re.findall(r"[а-яёa-z0-9-]+", text.lower())
        if word not in STOP_WORDS and len(word) > 1
    }


def load_faq(filename: Path) -> list[tuple[str, str]]:
    """Читает пары «Вопрос/Ответ» из faq.txt."""
    pairs: list[tuple[str, str]] = []
    question = None

    for line in filename.read_text(encoding="utf-8").splitlines():
        if line.startswith("Вопрос: "):
            question = line.removeprefix("Вопрос: ").strip()
        elif line.startswith("Ответ: ") and question:
            pairs.append((question, line.removeprefix("Ответ: ").strip()))
            question = None

    return pairs


def find_answer(user_question: str, faq: list[tuple[str, str]]) -> str | None:
    """Находит FAQ-вопрос с наибольшим пересечением ключевых слов."""
    query_words = words(user_question)
    if not query_words:
        return None

    best_score = 0
    best_answer = None
    for question, answer in faq:
        score = len(query_words & words(question))
        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer


def main() -> None:
    faq = load_faq(FAQ_FILE)
    print("FAQ-бот репетиции. Задайте вопрос или напишите «выход».")

    while True:
        user_question = input("> ").strip()
        if user_question.lower() in {"выход", "exit", "quit"}:
            print("До встречи!")
            break
        if not user_question:
            print("Напишите вопрос.")
            continue

        answer = find_answer(user_question, faq)
        print(answer if answer else "не знаю")


if __name__ == "__main__":
    main()
