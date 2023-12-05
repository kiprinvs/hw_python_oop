from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает информацию о тренировке"""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.MINUTES_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_COEFF_1 = 0.035
    CALORIES_COEFF_2 = 0.029
    SPEED_IN_MS = 0.278
    HEIGHT_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: int):
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_COEFF_1 * self.weight
                + (
                    self.get_mean_speed() * self.SPEED_IN_MS
                )**2
                / (
                    self.height / self.HEIGHT_IN_M
                )
                * self.CALORIES_COEFF_2 * self.weight
            )
            * self.duration * self.MINUTES_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_COEFF_1 = 1.1
    CALORIES_COEFF_2 = 2.0

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.get_mean_speed() + self.CALORIES_COEFF_1
            )
            * self.CALORIES_COEFF_2 * self.weight * self.duration
        )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict[str, type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if workout_type not in workout:
        raise ValueError(f'Тренировка {workout_type} не поддерживается.')
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Главная функция."""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
