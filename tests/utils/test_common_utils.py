# -*- coding: utf-8 -*-

from itertools import count

import pytest
from hypothesis import given, strategies as st
from typing import Any

from pyutilities.utils.common_utils import get_value_safely, myself
from pyutilities.utils.common_utils import add_kv_2_dict, dict_2_csv, is_empty
from pyutilities.utils.common_utils import build_variations_list, RUS_CHARS, ENG_CHARS, NUM_CHARS, SPEC_CHARS


def test_myself():
    # TODO: implement test!
    pass


@pytest.fixture
def mock_chars(monkeypatch):
    """Фикстура для подмены глобальных списков символов на предсказуемые тестовые данные."""
    test_rus = ["А"]
    test_eng = ["A"]
    test_num = ["1"]
    test_spec = ["*"]

    # Подменяем глобальные переменные в модуле, где объявлена функция
    monkeypatch.setattr("pyutilities.utils.common_utils.RUS_CHARS", test_rus)
    monkeypatch.setattr("pyutilities.utils.common_utils.ENG_CHARS", test_eng)
    monkeypatch.setattr("pyutilities.utils.common_utils.NUM_CHARS", test_num)
    monkeypatch.setattr("pyutilities.utils.common_utils.SPEC_CHARS", test_spec)

    return test_rus, test_eng, test_num, test_spec


def test_build_variations_structure_and_order(mock_chars):
    """Проверяет правильность составления комбинаций и их очередность."""
    result = build_variations_list()

    # При RUS+ENG+NUM = ["А", "A", "1"] и SPEC = ["*"]
    # Ожидаем комбинации для каждой пары (letter1, letter2):
    # сначала "letter1 + letter2", затем "letter1 + * + letter2"
    expected = [
        "АА", "А*А", "АA", "А*A", "А1", "А*1",
        "AА", "A*А", "AA", "A*A", "A1", "A*1",
        "1А", "1*А", "1A", "1*A", "11", "1*1"
    ]

    assert result == expected


def test_build_variations_empty_spec_chars(monkeypatch):
    """Проверяет поведение функции, если список спецсимволов пуст."""
    monkeypatch.setattr("pyutilities.utils.common_utils.RUS_CHARS", ["A"])
    monkeypatch.setattr("pyutilities.utils.common_utils.ENG_CHARS", [])
    monkeypatch.setattr("pyutilities.utils.common_utils.NUM_CHARS", [])
    monkeypatch.setattr("pyutilities.utils.common_utils.SPEC_CHARS", [])  # Пустые спецсимволы

    result = build_variations_list()

    # Ожидаем только комбинации из двух букв без спецсимволов внутри
    assert result == ["AA"]


def test_build_variations_all_globals_empty(monkeypatch):
    """Проверяет, что при отсутствии базовых символов возвращается пустой список."""
    monkeypatch.setattr("pyutilities.utils.common_utils.RUS_CHARS", [])
    monkeypatch.setattr("pyutilities.utils.common_utils.ENG_CHARS", [])
    monkeypatch.setattr("pyutilities.utils.common_utils.NUM_CHARS", [])
    monkeypatch.setattr("pyutilities.utils.common_utils.SPEC_CHARS", ["*", "#"])

    result = build_variations_list()
    assert result == []


non_whitespace_char = st.characters(blacklist_categories=('Zs', 'Zl', 'Zp')) \
    .filter(lambda c: not c.isspace())
char_list = st.lists(st.text(alphabet=non_whitespace_char, min_size=1, max_size=1),
                     min_size=0, max_size=5, unique=True)


@given(rus=char_list, eng=char_list, num=char_list, spec=char_list)
def test_hypothesis_variations_math_invariants(rus, eng, num, spec):
    """Проверяет математические инварианты размера списка при любых входящих наборах."""

    # Создаем изолированный объект MonkeyPatch вручную, без фикстур pytest
    with pytest.MonkeyPatch.context() as m:
        m.setattr("pyutilities.utils.common_utils.RUS_CHARS", rus)  # Укажите ваш правильный путь к модулю
        m.setattr("pyutilities.utils.common_utils.ENG_CHARS", eng)
        m.setattr("pyutilities.utils.common_utils.NUM_CHARS", num)
        m.setattr("pyutilities.utils.common_utils.SPEC_CHARS", spec)

        result = build_variations_list()

        total_base_chars = len(rus) + len(eng) + len(num)
        total_spec_chars = len(spec)

        # Формула точной длины результирующего списка
        expected_length = (total_base_chars ** 2) * (1 + total_spec_chars)

        assert len(result) == expected_length

        # Дополнительная проверка структуры комбинаций
        for variation in result:
            assert len(variation) in (2, 3)


def test_add_kv_2_dict():
    # TODO: implement test!
    pass


def test_dict_2_csv():
    # TODO: implement test!
    pass


@pytest.fixture(name='data_dictionary')
def dictionary():
    yield {"key1": "str_val1", "key2": 100}


def test_get_value_safely(data_dictionary):

    assert get_value_safely(data_dictionary, "key1", "zzz") == "str_val1"
    assert get_value_safely(data_dictionary, "key2", "zzz") == 100
    assert get_value_safely(data_dictionary, "key3", "zzz") == "zzz"
    assert get_value_safely(data_dictionary, "key4", 500) == 500


@pytest.mark.parametrize("data_dict, key, default, expected", [({}, "key1", 500, 500),
                                                               (None, "key2", "asdf", "asdf")])
def test_get_value_safely_empty_dict(data_dict, key, default, expected):

    assert get_value_safely(data_dict, key, default) == expected


@pytest.mark.parametrize(
    "empty_value",
    [
        None,
        "",
        " ",          # Одиночный пробел
        "   ",        # Несколько пробелов
        "\t\n  \r",   # Табуляции и переносы строк тоже считаются пустыми
        [],
        {},
        set(),
        (),
        range(0),
    ],
)
def test_is_empty_returns_true_for_empty_values(empty_value: Any):
    """Проверка всех пустых контейнеров, строк с пробелами и None."""
    assert is_empty(empty_value) is True


@pytest.mark.parametrize(
    "non_empty_value",
    [
        " a ",        # Есть значащий символ, окруженный пробелами
        "hello",
        [1],
        {"key": "value"},
        {None},       # Множество с элементом None не пустое
        (0,),
        range(1),
        0,            # Числа не являются пустыми
        0.0,
        False,        # Булевы значения не являются пустыми
        True,
    ],
)
def test_is_empty_returns_false_for_non_empty_values(non_empty_value: Any):
    """Проверка объектов, которые не должны считаться пустыми."""
    assert is_empty(non_empty_value) is False


def test_is_empty_custom_object():
    """Проверка пользовательского объекта без определенной длины."""
    class CustomObject:
        pass

    assert is_empty(CustomObject()) is False


# Генерируем строки, которые гарантированно содержат хотя бы один непробельный символ
non_whitespace_text = st.text(
    alphabet=st.characters(
        blacklist_categories=('Zs', 'Zl', 'Zp')
    ).filter(lambda c: not c.isspace()),
    min_size=1
)


@given(non_whitespace_text)
def test_hypothesis_non_empty_strings(s: str):
    """Строка, содержащая хотя бы один видимый символ, не должна быть пустой."""
    # Окружаем пробелами для усложнения теста
    complex_string = f"  {s}  "
    assert is_empty(complex_string) is False


@given(st.integers() | st.floats(allow_nan=False) | st.booleans())
def test_hypothesis_primitives_never_empty(val: int | float | bool):
    """Числа и булевы значения никогда не бывают пустыми."""
    assert is_empty(val) is False


@given(st.lists(st.one_of(st.integers(), st.text(), st.booleans()), min_size=1))
def test_hypothesis_non_empty_lists(lst: list[Any]):
    """Любой список, содержащий хотя бы один элемент, не пустой."""
    assert is_empty(lst) is False
