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
        pass

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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_run1: int = 18
        coeff_cal_run2: int = 20
        duration_minute: float = self.duration * 60
        calories: float
        calories = ((coeff_cal_run1 * self.get_mean_speed()
                    - coeff_cal_run2) * self.weight
                    / self.M_IN_KM * duration_minute)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
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
        coeff_cal_walk_1: float = 0.035
        coeff_cal_walk_2: float = 0.029
        duration_minute: float = self.duration * 60
        calories = (coeff_cal_walk_1 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * coeff_cal_walk_2 * self.weight) * duration_minute
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM = 1000
    LEN_STEP = 1.38

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
        LEN_STEP = 1.38
        M_IN_KM = 1000
        distance: float
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_swim_1: float = 1.1
        coeff_cal_swim_2: int = 2
        spent_calories_swim: float
        spent_calories_swim = ((self.get_mean_speed() + coeff_cal_swim_1)
                               * coeff_cal_swim_2 * self.weight)
        return spent_calories_swim


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return(training_type_dict[workout_type](*data))


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

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
