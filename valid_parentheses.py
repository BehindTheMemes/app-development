# мой вариант
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        pairs = {')': '(', ']': '[', '}': '{'}

        for char in s:
            if char in pairs.values():
                stack.append(char)
            else:
                if not stack or stack.pop() != pairs[char]:
                    return False

        return len(stack) == 0

### Оценка сложности (n - длина строки s):
    # Временная сложность: (O(n)), поскольку каждый символ обрабатывается не более одного раза.
    # Пространственная сложность: (O(n)) в худшем случае, поскольку стек может хранить до (n/2) открывающих скобок.
### Почему именно стек?
    # Стек работает по принципу LIFO (Last In, First Out) — последним пришёл, первым вышел.
    # Это соответствует правилам вложенности скобок: последняя открытая скобка должна закрыться первой.


### вариант агента
'''class Solution:
    def isValid(self, s: str) -> bool:
        # Словарь соответствия закрывающих скобок открывающим
        bracket_map = {")": "(", "}": "{", "]": "["}
        stack = []

        for char in s:
            # Если символ является закрывающей скобкой
            if char in bracket_map:
                # Извлекаем верхний элемент стека, если он не пуст, иначе используем заглушку
                top_element = stack.pop() if stack else '#'
                
                # Проверяем, соответствует ли открывающая скобка текущей закрывающей
                if bracket_map[char] != top_element:
                    return False
            else:
                # Если символ открывающая скобка, добавляем её в стек
                stack.append(char)

        # Строка валидна, если в стеке не осталось не закрытых скобок
        return not stack'''

# Тесты
if __name__ == "__main__":
    sol = Solution()
    print(f"Example 1: {sol.isValid('()')} (Expected: True)")
    print(f"Example 2: {sol.isValid('()[]{}')} (Expected: True)")
    print(f"Example 3: {sol.isValid('(]')} (Expected: False)")
    print(f"Example 4: {sol.isValid('([])')} (Expected: True)")
    print(f"Example 5: {sol.isValid('([)]')} (Expected: False)")


### Оценка сложности:
# 1. **Временная сложность: $O(n)$**, где $n$ — длина строки. Мы проходим по строке один раз, а операции со стеком (`push` и `pop`) выполняются за константное время $O(1)$.
# 2. **Пространственная сложность: $O(n)$**. В худшем случае (например, если строка состоит только из открывающих скобок `(((((`), нам придется сохранить все символы в стеке.

