### мой вариант
class MyQueue:

    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x: int) -> None:
        self.stack_in.append(x)

    def pop(self) -> int:
        self.peek()
        return self.stack_out.pop()

    def peek(self) -> int:
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out[-1]

    def empty(self) -> bool:
        return not self.stack_in and not self.stack_out

### Оценка сложности
    ## Пусть (n) – количество элементов в очереди.
    ## Временная сложность
        # push(), empty() – O(1);
        # pop(), peek() – O(1) (амортизированно).
        # Амортизированная сложность операций pop() и peek() составляет O(1), 
        # потому что каждый элемент перемещается из одного стека в другой 
        # не более одного раза за всё время работы очереди. 
        # При отдельном вызове перенос может занять O(n).
    ## Пространственная сложность: O(n), поскольку два стека вместе хранят все элементы очереди.


### вариант агента
'''class MyQueue:

    def __init__(self):
        # Стек для добавления элементов
        self.stack_in = []
        # Стек для извлечения элементов
        self.stack_out = []

    def push(self, x: int) -> None:
        # Просто добавляем в стек ввода
        self.stack_in.append(x)

    def pop(self) -> int:
        # Сначала гарантируем, что в stack_out есть элементы
        self._move_elements()
        # Извлекаем с вершины стека вывода (это будет начало очереди)
        return self.stack_out.pop()

    def peek(self) -> int:
        # Гарантируем наличие элементов в stack_out
        self._move_elements()
        # Возвращаем верхний элемент стека вывода
        return self.stack_out[-1]

    def empty(self) -> bool:
        # Очередь пуста, если оба стека пусты
        return not self.stack_in and not self.stack_out

    def _move_elements(self) -> None:
        # Вспомогательный метод для перекладывания элементов из одного стека в другой
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())'''

# Тестирование примера из условия
if __name__ == "__main__":
    myQueue = MyQueue()
    myQueue.push(1)
    myQueue.push(2)
    print(f"Peek: {myQueue.peek()}") # Ожидается: 1
    print(f"Pop: {myQueue.pop()}")   # Ожидается: 1
    print(f"Empty: {myQueue.empty()}") # Ожидается: False


### Оценка сложности решения:
    ## Временная сложность (Time Complexity):
        # push: O(1) — всегда константное время.
        # pop: амортизированное O(1). В худшем случае (когда stack_out пуст) потребуется O(n), 
        #   чтобы переложить элементы, но каждый элемент перекладывается между стеками ровно один раз за все время своего пребывания в очереди.
        # peek: амортизированное O(1) — аналогично pop.
        # empty: O(1).
    ## Пространственная сложность (Space Complexity):
        # O(n), где n — количество элементов в очереди, так как нам нужно хранить все элементы в двух стеках.
