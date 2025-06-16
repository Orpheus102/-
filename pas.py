import time
import random
import matplotlib.pyplot as plt
from typing import List, Union, Callable

class HeapSort:
    """Класс для реализации пирамидальной сортировки с расширенной функциональностью"""
    
    def __init__(self, 
                 data: List[Union[int, float, str]], 
                 reverse: bool = False,
                 key: Callable = None):
        """
        Инициализация объекта сортировки
        :param data: Сортируемый массив
        :param reverse: Флаг обратной сортировки
        :param key: Функция ключа для сортировки
        """
        self.original_data = data.copy()
        self.data = data.copy()
        self.reverse = reverse
        self.key = key if key else lambda x: x
        self.comparisons = 0
        self.swaps = 0
        self.steps = []

    def _heapify(self, n: int, i: int) -> None:
        """Внутренний метод для поддержания свойства кучи"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Сравнение с левым потомком
        if left < n:
            self.comparisons += 1
            if (self.key(self.data[left]) > self.key(self.data[largest])) ^ self.reverse:
                largest = left

        # Сравнение с правым потомком
        if right < n:
            self.comparisons += 1
            if (self.key(self.data[right]) > self.key(self.data[largest])) ^ self.reverse:
                largest = right

        # Если наибольший элемент не корень
        if largest != i:
            self.swaps += 1
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.steps.append(self.data.copy())
            self._heapify(n, largest)

    def _build_heap(self) -> None:
        """Построение начальной кучи"""
        n = len(self.data)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(n, i)

    def sort(self) -> List[Union[int, float, str]]:
        """Основной метод сортировки"""
        start_time = time.time()
        self._build_heap()
        
        n = len(self.data)
        for i in range(n-1, 0, -1):
            self.data[0], self.data[i] = self.data[i], self.data[0]
            self.steps.append(self.data.copy())
            self._heapify(i, 0)
        
        self.execution_time = time.time() - start_time
        return self.data

    def analyze(self) -> dict:
        """Анализ производительности"""
        return {
            'data_size': len(self.data),
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'time': self.execution_time,
            'steps': len(self.steps)
        }

    def visualize(self, step: int = None) -> None:
        """Визуализация процесса сортировки"""
        plt.figure(figsize=(10, 6))
        if step is not None and step < len(self.steps):
            plt.bar(range(len(self.steps[step])), self.steps[step])
            plt.title(f'Шаг сортировки: {step}')
        else:
            plt.bar(range(len(self.data)), self.data)
            plt.title('Отсортированный массив')
        plt.xlabel('Индекс')
        plt.ylabel('Значение')
        plt.show()

def test_performance(data_sizes: List[int] = [100, 1000, 10000]) -> None:
    """Тестирование производительности на разных размерах данных"""
    results = []
    for size in data_sizes:
        data = [random.randint(0, 1000) for _ in range(size)]
        sorter = HeapSort(data)
        sorter.sort()
        stats = sorter.analyze()
        results.append(stats)
        print(f"Размер данных: {size}")
        print(f"Сравнения: {stats['comparisons']}")
        print(f"Обмены: {stats['swaps']}")
        print(f"Время: {stats['time']:.6f} сек")
        print("----------------------------------")
    
    # Визуализация результатов
    plt.plot(data_sizes, [r['time'] for r in results])
    plt.xlabel('Размер данных')
    plt.ylabel('Время (сек)')
    plt.title('Производительность пирамидальной сортировки')
    plt.show()

# Пример использования
if __name__ == "__main__":
    # Тестовые данные
    data_types = {
        'integers': [4, 10, 3, 5, 1],
        'floats': [5.2, 1.1, 3.7, 2.4, 0.5],
        'strings': ['banana', 'apple', 'orange', 'grape', 'kiwi'],
        'large_dataset': [random.randint(0, 500) for _ in range(50)]
    }

    # Сортировка разных типов данных
    for dtype, data in data_types.items():
        print(f"\nСортировка данных типа: {dtype}")
        sorter = HeapSort(data)
        sorted_data = sorter.sort()
        print(f"Исходные данные: {data}")
        print(f"Отсортированные данные: {sorted_data}")
        sorter.visualize()
    
    # Тестирование производительности
    test_performance()