from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os
from datetime import datetime
from decimal import Decimal
from typing import List, Dict


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Чтение индекса моделей
        models_index_path = os.path.join(
            self.root_directory_path,
            'models_index.txt'
            )
        try:
            with open(models_index_path, 'r', encoding='utf-8') as f:
                models_index = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            models_index = []

        # Добавление новой модели
        models_index.append(model.index())
        with open(models_index_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(models_index))

        # Запись данных модели
        models_path = os.path.join(self.root_directory_path, 'models.txt')
        formatted = f'{model.id};{model.name};{model.brand}'
        with open(models_path, 'a', encoding='utf-8') as f:
            f.write(formatted.ljust(500) + '\n')
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        # Чтение индекса автомобилей
        cars_index_path = os.path.join(
            self.root_directory_path,
            'cars_index.txt'
            )
        try:
            with open(cars_index_path, 'r', encoding='utf-8') as f:
                cars_index = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            cars_index = []

        # Добавление нового автомобиля
        cars_index.append(car.vin)
        with open(cars_index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cars_index))

        # Запись данных автомобиля
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        formatted = (
            f'{car.vin};'
            f'{car.model};'
            f'{car.price};'
            f'{car.date_start.strftime("%Y-%m-%d %H:%M:%S")};'
            f'{car.status.value}'
        )
        with open(cars_path, 'a', encoding='utf-8') as f:
            f.write(formatted.ljust(500) + '\n')
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        # Чтение индекса продаж
        sales_index_path = os.path.join(
            self.root_directory_path,
            'sales_index.txt'
            )
        try:
            with open(sales_index_path, 'r', encoding='utf-8') as f:
                sales_index = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            sales_index = []

        # Добавление новой продажи
        sales_index.append(sale.sales_number)
        with open(sales_index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sales_index))

        # Запись данных продажи
        sales_path = os.path.join(self.root_directory_path, 'sales.txt')
        formatted = (
            f'{sale.sales_number};'
            f'{sale.car_vin};'
            f'{sale.sales_date.strftime("%Y-%m-%d %H:%M:%S")};'
            f'{sale.cost}'
        )
        formatted = formatted[:500]
        with open(sales_path, 'a', encoding='utf-8') as f:
            f.write(formatted.ljust(500) + '\n')

        # Обновление статуса автомобиля
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        cars_index_path = os.path.join(
            self.root_directory_path,
            'cars_index.txt'
            )
        with open(cars_index_path, 'r', encoding='utf-8') as f:
            cars_index = [line.strip() for line in f if line.strip()]
        car_line = cars_index.index(sale.car_vin)
        with open(cars_path, 'r+', encoding='utf-8') as f:
            f.seek(car_line * 501)
            line = f.read(500).strip()
            parts = line.split(';')
            car = Car(
                vin=parts[0],
                model=int(parts[1]),
                price=Decimal(parts[2]),
                date_start=datetime.strptime(parts[3], "%Y-%m-%d %H:%M:%S"),
                status=CarStatus(parts[4])
            )
            car.status = CarStatus.sold
            updated_line = (
                f'{car.vin};'
                f'{car.model};'
                f'{car.price};'
                f'{car.date_start.strftime("%Y-%m-%d %H:%M:%S")};'
                f'{car.status.value}'
            )
            f.seek(car_line * 502)
            f.write(updated_line.ljust(500) + '\n')
        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> List[Car]:
        result = []
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        with open(cars_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                parts = line.split(';')
                car = Car(
                    vin=parts[0],
                    model=int(parts[1]),
                    price=Decimal(parts[2]),
                    date_start=datetime.strptime(
                        parts[3],
                        "%Y-%m-%d %H:%M:%S"
                        ),
                    status=CarStatus(parts[4])
                )
                if car.status == status:
                    result.append(car)
        return result

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        models_path = os.path.join(self.root_directory_path, 'models.txt')
        sales_path = os.path.join(self.root_directory_path, 'sales.txt')
        cars_index_path = os.path.join(
            self.root_directory_path,
            'cars_index.txt'
            )
        models_index_path = os.path.join(
            self.root_directory_path,
            'models_index.txt')
        try:
            # Ищем позицию автомобиля по VIN в индексе
            with open(cars_index_path, 'r', encoding='utf-8') as f:
                cars_index = [line.strip() for line in f if line.strip()]
            car_line = cars_index.index(vin)

            # Читаем запись об автомобиле
            with open(cars_path, 'r', encoding='utf-8') as f:
                f.seek(car_line * 501)
                line = f.read(500).strip()
                parts = line.split(';')
                car = Car(
                    vin=parts[0],
                    model=int(parts[1]),
                    price=Decimal(parts[2]),
                    date_start=datetime.strptime(
                        parts[3],
                        "%Y-%m-%d %H:%M:%S"
                        ),
                    status=CarStatus(parts[4])
                )

            # Получаем информацию о модели
            with open(models_index_path, 'r', encoding='utf-8') as f:
                models_index = [line.strip() for line in f if line.strip()]
            model_line = models_index.index(str(car.model))
            with open(models_path, 'r', encoding='utf-8') as f:
                f.seek(model_line * 501)
                model_line_str = f.read(500).strip()
                model_parts = model_line_str.split(';')
                model = Model(
                    id=int(model_parts[0]),
                    name=model_parts[1],
                    brand=model_parts[2]
                )

            # Ищем информацию о продаже
            sales_date = None
            sales_cost = None
            if car.status == CarStatus.sold:
                with open(sales_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        sale_parts = line.split(';')
                        if sale_parts[1] == vin:
                            sales_date = datetime.fromisoformat(sale_parts[2])
                            sales_cost = Decimal(sale_parts[3])
                            break

            # Формируем полный объект
            return CarFullInfo(
                vin=car.vin,
                car_model_name=model.name,
                car_model_brand=model.brand,
                price=car.price,
                date_start=car.date_start,
                status=car.status,
                sales_date=sales_date,
                sales_cost=sales_cost
            )
        except (ValueError, FileNotFoundError):
            return None

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        cars_index_path = os.path.join(
            self.root_directory_path,
            'cars_index.txt'
            )
        with open(cars_index_path, 'r', encoding='utf-8') as f:
            cars_index = [line.strip() for line in f if line.strip()]

        # 1. Находим позицию и читаем запись
        car_line = cars_index.index(vin)
        with open(cars_path, 'r', encoding='utf-8') as f:
            f.seek(car_line * 501)
            line = f.read(500).strip()
            parts = line.split(';')
            car = Car(
                vin=parts[0],
                model=int(parts[1]),
                price=Decimal(parts[2]),
                date_start=datetime.strptime(parts[3], "%Y-%m-%d %H:%M:%S"),
                status=CarStatus(parts[4])
            )
        car.vin = new_vin
        # 2. Перезаписываем запись в файле
        updated_line = (
            f'{car.vin};'
            f'{car.model};'
            f'{car.price};'
            f'{car.date_start.strftime("%Y-%m-%d %H:%M:%S")};'
            f'{car.status.value}'
        )
        with open(cars_path, 'r+', encoding='utf-8') as f:
            f.seek(car_line * 501)
            f.write(updated_line.ljust(500) + '\n')

        # 3. Обновляем индекс
        cars_index[car_line] = new_vin
        with open(cars_index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cars_index))
        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        sales_path = os.path.join(self.root_directory_path, 'sales.txt')
        sales_index_path = os.path.join(
            self.root_directory_path,
            'sales_index.txt'
            )
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        cars_index_path = os.path.join(
            self.root_directory_path,
            'cars_index.txt'
            )

        # 1. Ищем продажу по sales_number
        with open(sales_index_path, 'r', encoding='utf-8') as f:
            sales_index = [line.strip() for line in f if line.strip()]
        sale_line = sales_index.index(sales_number)

        # 2. Читаем запись о продаже
        with open(sales_path, 'r', encoding='utf-8') as f:
            f.seek(sale_line * 501)
            line = f.read(500).strip()
            sale_parts = line.split(';')
            sale = Sale(
                sales_number=sale_parts[0],
                car_vin=sale_parts[1],
                sales_date=datetime.strptime(
                    sale_parts[2],
                    "%Y-%m-%d %H:%M:%S"
                    ),
                cost=Decimal(sale_parts[3])
            )

        # 3. Находим и обновляем автомобиль
        with open(cars_index_path, 'r', encoding='utf-8') as f:
            cars_index = [line.strip() for line in f if line.strip()]
        car_line = cars_index.index(sale.car_vin)
        with open(cars_path, 'r+', encoding='utf-8') as f:
            f.seek(car_line * 501)
            car_line_str = f.read(500).strip()
            car_parts = car_line_str.split(';')
            car = Car(
                vin=car_parts[0],
                model=int(car_parts[1]),
                price=Decimal(car_parts[2]),
                date_start=datetime.strptime(
                    car_parts[3],
                    "%Y-%m-%d %H:%M:%S"
                    ),
                status=CarStatus(car_parts[4])
            )
            car.status = CarStatus.available
            updated_car_line = (
                f'{car.vin};'
                f'{car.model};'
                f'{car.price};'
                f'{car.date_start.strftime("%Y-%m-%d %H:%M:%S")};'
                f'{car.status.value}'
                )
            updated_car_line = updated_car_line[:500]
            f.seek(car_line * 501)
            f.write(updated_car_line.ljust(500) + '\n')

        # 4. Помечаем продажу как удалённую
        marked_line = line.rstrip('\n') + ';deleted'
        with open(sales_path, 'r+', encoding='utf-8') as f:
            f.seek(sale_line * 501)
            f.write(marked_line.ljust(500) + '\n')
        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        sales_count: Dict[int, int] = {}
        model_avg_prices: Dict[int, Decimal] = {}
        sales_path = os.path.join(self.root_directory_path, 'sales.txt')
        cars_path = os.path.join(self.root_directory_path, 'cars.txt')
        models_path = os.path.join(self.root_directory_path, 'models.txt')
        cars_index_path = os.path.join(
            self.root_directory_path,
            'cars_index.txt'
            )
        models_index_path = os.path.join(
            self.root_directory_path,
            'models_index.txt'
            )

        # Считаем количество продаж по моделям
        with open(sales_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                sale_parts = line.split(';')
                car_vin = sale_parts[1]

                # Находим модель автомобиля
                with open(cars_index_path, 'r', encoding='utf-8') as cf:
                    cars_index = [cl.strip() for cl in cf if cl.strip()]
                car_line = cars_index.index(car_vin)
                with open(cars_path, 'r', encoding='utf-8') as cf:
                    cf.seek(car_line * 501)
                    car_line_str = cf.read(500).strip()
                    car_parts = car_line_str.split(';')
                    model_id = int(car_parts[1])
                sales_count[model_id] = sales_count.get(model_id, 0) + 1

        # Считаем среднюю цену по моделям
        with open(cars_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                car_parts = line.split(';')
                model_id = int(car_parts[1])
                price = Decimal(car_parts[2])
                if model_id not in model_avg_prices:
                    model_avg_prices[model_id] = Decimal('0')
                model_avg_prices[model_id] += price

        # Подсчитываем количество автомобилей по моделям для усреднения
        model_counts: Dict[int, int] = {}
        with open(cars_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                car_parts = line.split(';')
                model_id = int(car_parts[1])
                model_counts[model_id] = model_counts.get(model_id, 0) + 1

        # Вычисляем средние цены
        for model_id in model_avg_prices:
            count = model_counts.get(model_id, 0)
            if count > 0:
                model_avg_prices[model_id] /= count

        # Сортируем модели: сначала по количеству продаж, затем по средней цене
        sorted_models = sorted(
            sales_count.items(),
            key=lambda x: (-x[1], -model_avg_prices.get(x[0], Decimal('0')))
        )

        # Формируем топ‑3
        top_3 = sorted_models[:3]
        result = []
        for model_id, count in top_3:
            # Получаем информацию о модели
            with open(models_index_path, 'r', encoding='utf-8') as mf:
                models_index = [ml.strip() for ml in mf if ml.strip()]
            model_line = models_index.index(str(model_id))
            with open(models_path, 'r', encoding='utf-8') as mf:
                mf.seek(model_line * 501)
                model_line_str = mf.read(500).strip()
                model_parts = model_line_str.split(';')
                model = Model(
                    id=int(model_parts[0]),
                    name=model_parts[1],
                    brand=model_parts[2]
                )
            result.append(ModelSaleStats(
                car_model_name=model.name,
                brand=model.brand,
                sales_number=count
            ))
        return result
