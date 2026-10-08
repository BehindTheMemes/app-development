### Вариант агента

#1 Перебор
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        Подход: Перебор (Brute Force)
        Временная сложность: O(n^2) - два вложенных цикла обходят список.
        Пространственная сложность: O(1) - дополнительная память не используется.
        """
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

#2 HashMap
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """
        Подход: Хеш-таблица (Словарь)
        Временная сложность: O(n) - один проход по списку.
        Пространственная сложность: O(n) - для хранения словаря.
        """
        prev_map = {} # значение : индекс
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prev_map:
                return [prev_map[diff], i]
            prev_map[n] = i
        return []

### Мой вариант

#1 Перебор
"Сложность: время O(n²), память O(1)"
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

#2 HashMap
"Сложность: время O(n), память O(n)"
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}  # значение -> индекс
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []

### Вывод-сравнение:
"HashMap выигрывает, потому что вместо перебора всех пар за O(n²) "
"мы за один проход ищем дополнение target − x за O(1), получая O(n) по времени. "
"Тратим на это O(n) дополнительной памяти, то есть меняем память на скорость."