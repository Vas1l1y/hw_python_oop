from typing import List, Type, Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:0.3f} ч.; '
               'Дистанция: {distance:0.3f} км; '
               'Ср. скорость: {speed:0.3f} км/ч; '
               'Потрачено ккал: {calories:0.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float
        speed = (self.get_distance() / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.'
                                  % (type(self).__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_cal_run1: int = 18
    coeff_cal_run2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minute: float = self.duration * self.HOUR_IN_MIN
        calories: float
        calories = ((self.coeff_cal_run1 * self.get_mean_speed()
                    - self.coeff_cal_run2) * self.weight
                    / self.M_IN_KM * duration_minute)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_cal_walk_1: float = 0.035
    coeff_cal_walk_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> float:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minute: float = self.duration * self.HOUR_IN_MIN
        calories = (self.coeff_cal_walk_1 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * self.coeff_cal_walk_2 * self.weight) * duration_minute
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_cal_swim_1: float = 1.1
    coeff_cal_swim_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories_swim: float
        spent_calories_swim = ((self.get_mean_speed() + self.coeff_cal_swim_1)
                               * self.coeff_cal_swim_2 * self.weight)
        return spent_calories_swim


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return (training_type_dict[workout_type](*data))
    except KeyError:
        raise ValueError('Неверный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

<<<<<<< HEAD

def test_Training_show_training_info(monkeypatch):
    training = homework.Training(*[720, 1, 80])
    assert hasattr(training, 'show_training_info'), (
        'Создайте метод `show_training_info` в классе `Training`.'
    )

    def mock_get_spent_calories():
        return 100
    monkeypatch.setattr(
        training,
        'get_spent_calories',
        mock_get_spent_calories
    )
    result = training.show_training_info()
    assert result.__class__.__name__ == 'InfoMessage', (
        'Метод `show_training_info` класса `Training` '
        'должен возвращать объект класса `InfoMessage`.'
    )


def test_Swimming():
    assert hasattr(homework, 'Swimming'), 'Создайте класс `Swimming`'
    assert inspect.isclass(homework.Swimming), (
        'Проверьте, что `Swimming` - это класс.'
    )
    assert issubclass(homework.Swimming, homework.Training), (
        'Класс `Swimming` должен наследоваться от класса `Training`.'
    )
    swimming = homework.Swimming
    swimming_signature = inspect.signature(swimming)
    swimming_signature_list = list(swimming_signature.parameters)
    for param in ['action', 'duration', 'weight', 'length_pool', 'count_pool']:
        assert param in swimming_signature_list, (
            'У метода `__init__` класса `Swimming` '
            f' должен быть параметр {param}.'
        )
    assert 'LEN_STEP' in list(swimming.__dict__), (
        'Задайте атрибут `LEN_STEP` в классе `Swimming`'
    )
    assert swimming.LEN_STEP == 1.38, (
        'Длина гребка в классе `Swimming` должна быть равна 1.38'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 1.0),
    ([420, 4, 20, 42, 4], 0.042),
    ([1206, 12, 6, 12, 6], 0.005999999999999999),
])
def test_Swimming_get_mean(input_data, expected):
    swimming = homework.Swimming(*input_data)
    result = swimming.get_mean_speed()
    assert result == expected, (
        'Переопределите метод `get_mean_speed` в классе `Swimming`. '
        'Проверьте формулу подсчёта средней скорости в классе `Swimming`'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 336.0),
    ([420, 4, 20, 42, 4], 45.68000000000001),
    ([1206, 12, 6, 12, 6], 13.272000000000002),
])
def test_Swimming_get_spent_calories(input_data, expected):
    swimming = homework.Swimming(*input_data)
    result = swimming.get_spent_calories()
    assert type(result) == float, (
        'Переопределите метод `get_spent_calories` в классе `Swimming`.'
    )
    assert result == expected, (
        'Проверьте формулу расчёта потраченных калорий в классе `Swimming`'
    )


def test_SportsWalking():
    assert hasattr(homework, 'SportsWalking'), 'Создайте класс `SportsWalking`'
    assert inspect.isclass(homework.SportsWalking), (
        'Проверьте, что  `SportsWalking` - это класс.'
    )
    assert issubclass(homework.SportsWalking, homework.Training), (
        'Класс `SportsWalking` должен наследоваться от класса `Training`.'
    )
    sports_walking = homework.SportsWalking
    sports_walking_signature = inspect.signature(sports_walking)
    sports_walking_signature_list = list(sports_walking_signature.parameters)
    for param in ['action', 'duration', 'weight', 'height']:
        assert param in sports_walking_signature_list, (
            'У метода `__init__` класса `SportsWalking` '
            f'должен быть параметр {param}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75, 180], 157.50000000000003),
    ([420, 4, 20, 42], 168.00000000000003),
    ([1206, 12, 6, 12], 151.20000000000002),
])
def test_SportsWalking_get_spent_calories(input_data, expected):
    sports_walking = homework.SportsWalking(*input_data)
    result = sports_walking.get_spent_calories()
    assert type(result) == float, (
        'Переопределите метод `get_spent_calories` в классе `SportsWalking`.'
    )
    assert result == expected, (
        'Проверьте формулу подсчёта потраченных '
        'калорий в классе `SportsWalking`'
    )


def test_Running():
    assert hasattr(homework, 'Running'), 'Создайте класс `Running`'
    assert inspect.isclass(homework.Running), (
        'Проверьте, что `Running` - это класс.'
    )
    assert issubclass(homework.Running, homework.Training), (
        'Класс `Running` должен наследоваться от класса `Training`.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 383.85),
    ([420, 4, 20], -90.1032),
    ([1206, 12, 6], -81.32032799999999),
])
def test_Running_get_spent_calories(input_data, expected):
    running = homework.Running(*input_data)
    assert hasattr(running, 'get_spent_calories'), (
        'Создайте метод `get_spent_calories` в классе `Running`.'
    )
    result = running.get_spent_calories()
    assert type(result) == float, (
        'Переопределите метод `get_spent_calories` в классе `Running`.'
    )
    assert result == expected, (
        'Проверьте формулу расчёта потраченных калорий в классе `Running`'
    )


def test_main():
    assert hasattr(homework, 'main'), (
        'Создайте главную функцию программы с именем `main`.'
    )
    assert callable(homework.main), 'Проверьте, что `main` - это функция.'
    assert isinstance(homework.main, types.FunctionType), (
        'Проверьте, что `main` - это функция.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (['SWM', [720, 1, 80, 25, 40]], [
        'Тип тренировки: Swimming; '
        'Длительность: 1.000 ч.; '
        'Дистанция: 0.994 км; '
        'Ср. скорость: 1.000 км/ч; '
        'Потрачено ккал: 336.000.'
    ]),
    (['RUN', [1206, 12, 6]], [
        'Тип тренировки: Running; '
        'Длительность: 12.000 ч.; '
        'Дистанция: 0.784 км; '
        'Ср. скорость: 0.065 км/ч; '
        'Потрачено ккал: -81.320.'
    ]),
    (['WLK', [9000, 1, 75, 180]], [
        'Тип тренировки: SportsWalking; '
        'Длительность: 1.000 ч.; '
        'Дистанция: 5.850 км; '
        'Ср. скорость: 5.850 км/ч; '
        'Потрачено ккал: 157.500.'
    ])
])
def test_main_output(input_data, expected):
    with Capturing() as get_message_output:
        training = homework.read_package(*input_data)
        homework.main(training)
    assert get_message_output == expected, (
        'Метод `main` должен печатать результат в консоль.\n'
    )
=======
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
>>>>>>> 7a581169b34a89313d0518ac1ff10e1027fcb8ac
