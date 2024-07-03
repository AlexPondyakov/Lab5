import os
import csv
import chardet


# Класс для представления истории посещений
class Visit:
    def __init__(self, visit_id, patient_name, doctor_name, report_reason, period):
        self.visit_id = visit_id
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.report_reason = report_reason
        self.period = int(period)  # Преобразование периода к целому числу

    def __repr__(self):
        # Метод строкового представления объекта
        return (f"{{'№ обращения': '{self.visit_id}', 'ФИО пациента': '{self.patient_name}',"
                f"'ФИО врача': '{self.doctor_name}', 'Причина обращения': '{self.report_reason}', "
                f"'Длительность': '{self.period}'}}")


# Класс для работы с файлами в директории
class FileManager:
    def __init__(self, directory_path):
        # Инициализация объекта с путем к директории и получение списка файлов
        self.directory_path = directory_path
        self.files = self._get_files()

    def _get_files(self):
        # Приватный метод для получения списка файлов в директории
        try:
            files_and_dirs = os.listdir(self.directory_path)
            files = [f for f in files_and_dirs if os.path.isfile(os.path.join(self.directory_path, f))]
            return files
        except Exception as e:
            # Обработка ошибок при получении списка файлов
            print(f"Ошибка при получении списка файлов: {e}")
            return []

    def __len__(self):
        # Перегрузка операции получения длины объекта
        return len(self.files)

    def __repr__(self):
        # Перегрузка операции строкового представления объекта
        return f"FileManager({self.directory_path})"

    def __iter__(self):
        # Перегрузка операции итерации
        self._index = 0
        return self

    def __next__(self):
        # Перегрузка операции получения следующего элемента при итерации
        if self._index < len(self.files):
            result = self.files[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
        # Перегрузка операции доступа к элементам коллекции по индексу
        return self.files[index]

    @staticmethod
    def detect_file_encoding(file_path):
        # Статический метод для определения кодировки файла
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']


# Класс для работы с данными CSV файла
class CSVData:
    def __init__(self, file_path):
        # Инициализация объекта с путем к файлу CSV
        self.file_path = file_path
        self.encoding = FileManager.detect_file_encoding(file_path)  # Определение кодировки файла
        self.data = self._read_data()  # Чтение данных из CSV файла

    def _read_data(self):
        # Приватный метод для чтения данных из CSV файла
        data = []
        try:
            with open(self.file_path, mode='r', encoding=self.encoding) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                for row in csv_reader:
                    visit = Visit(
                        visit_id=row['№ обращения'],
                        patient_name=row['ФИО пациента'],
                        doctor_name=row['ФИО врача'],
                        report_reason=row['Причина обращения'],
                        period=row['Длительность']
                    )
                    data.append(visit)
        except Exception as e:
            # Обработка ошибок при чтении файла CSV
            print(f"Ошибка при чтении файла CSV: {e}")
        return data

    def __repr__(self):
        # Перегрузка операции строкового представления объекта
        return f"CSVData({self.file_path})"

    def __getitem__(self, index):
        # Перегрузка операции доступа к элементам коллекции по индексу
        return self.data[index]

    def __iter__(self):
        # Перегрузка операции итерации
        self._index = 0
        return self

    def __next__(self):
        # Перегрузка операции получения следующего элемента при итерации
        if self._index < len(self.data):
            result = self.data[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    @staticmethod
    def sort_data_by_string_field(data, field_name):
        # Статический метод для сортировки данных по строковому полю
        try:
            return sorted(data, key=lambda x: getattr(x, field_name))
        except AttributeError:
            # Обработка ошибок, если поле не найдено
            print(f"Поле {field_name} не найдено в данных.")
            return data

    @staticmethod
    def sort_data_by_numeric_field(data, field_name):
        # Статический метод для сортировки данных по числовому полю
        try:
            return sorted(data, key=lambda x: getattr(x, field_name), reverse=True)
        except AttributeError:
            # Обработка ошибок, если поле не найдено
            print(f"Поле {field_name} не найдено в данных.")
        return data

    @staticmethod
    def filter_data_by_criteria(data, field_name, criteria):
        # Статический метод для фильтрации данных по критерию
        try:
            return [item for item in data if getattr(item, field_name) >= criteria]
        except AttributeError:
            # Обработка ошибок, если поле не найдено
            print(f"Поле {field_name} не найдено в данных.")
        return data

    def save_data(self, data):
        # Метод для сохранения данных в файл CSV
        try:
            if not data:
                print("Нет данных для сохранения.")
                return

            fieldnames = ['№ обращения', 'ФИО пациента', 'ФИО врача', 'Причина обращения', 'Длительность']
            with open(self.file_path, mode='w', encoding=self.encoding, newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for visit in data:
                    writer.writerow({
                        '№ обращения': visit.visit_id,
                        'ФИО пациента': visit.patient_name,
                        'ФИО врача': visit.doctor_name,
                        'Причина обращения': visit.report_reason,
                        'Длительность': visit.period
                    })
        except Exception as e:
            # Обработка ошибок при сохранении файла CSV
            print(f"Ошибка при сохранении файла CSV: {e}")

    def __setattr__(self, key, value):
        # Перегрузка операции установки атрибутов объекта
        # Разрешение только для определенных атрибутов
        if key in ['file_path', 'encoding', 'data', '_index']:
            self.__dict__[key] = value
        else:
            raise AttributeError(f"Attribute '{key}' is not allowed to be set")


# Класс для обработки данных
class DataProcessor:
    def __init__(self, csv_data):
        # Инициализация объекта с данными CSV
        self.csv_data = csv_data

    def process_data(self, option, criteria=None):
        # Метод для обработки данных в зависимости от выбора
        if option == '1':
            # Сортировка данных по Длительности
            return CSVData.sort_data_by_numeric_field(self.csv_data.data, 'period')
        elif option == '2':
            # Сортировка данных по ФИО пациента
            return CSVData.sort_data_by_string_field(self.csv_data.data, 'patient_name')
        elif option == '3':
            # Сортировка данных по Причине обращения
            return CSVData.sort_data_by_string_field(self.csv_data.data, 'report_reason')
        elif option == '4':
            # Фильтрация данных по Длительности с заданным критерием
            return CSVData.filter_data_by_criteria(self.csv_data.data, 'period', criteria)
        else:
            print("Некорректный выбор.")
            return self.csv_data.data

    @staticmethod
    def data_generator(data):
        # Статический метод для создания генератора данных
        for item in data:
            yield {
                '№ обращения': item.visit_id,
                'ФИО пациента': item.patient_name,
                'ФИО врача': item.doctor_name,
                'Причина обращения': item.report_reason,
                'Длительность': item.period
            }


def main():
    # Основная функция программы

    # Получение пути к директории от пользователя
    directory_path = input("Введите путь к директории: ")

    # Создание объекта FileManager для работы с файлами в указанной директории
    file_manager = FileManager(directory_path)

    # Вывод количества файлов в директории
    print(f"Количество файлов в директории: {len(file_manager)}")

    # Проверка, есть ли файлы в директории
    if len(file_manager) == 0:
        print("В данной директории нет файлов.")
        return

    # Вывод списка файлов в директории
    print("Файлы в директории:")
    for i, file in enumerate(file_manager):
        print(f"{i + 1}. {file}")

    try:
        # Запрос у пользователя выбора файла по индексу
        file_index = int(input(f"Выберите файл (1-{len(file_manager)}): ")) - 1
        # Проверка корректности введенного индекса
        if file_index < 0 or file_index >= len(file_manager):
            print("Неверный выбор файла.")
            return
    except ValueError:
        # Обработка ошибки ввода, если введено не число
        print("Неверный ввод.")
        return

    # Формирование полного пути к выбранному файлу
    file_path = os.path.join(directory_path, file_manager[file_index])

    # Создание объекта CSVData для работы с данными из CSV файла
    csv_data = CSVData(file_path)

    # Создание объекта DataProcessor для обработки данных
    processor = DataProcessor(csv_data)

    # Вывод содержимого выбранного CSV файла
    print("\nСодержимое выбранного CSV файла:")
    for visit in csv_data:
        print(visit)

    # Выбор типа обработки данных
    print("\nВыберите тип обработки данных:")
    print("1. Сортировка по Длительности")
    print("2. Сортировка по ФИО пациента")
    print("3. Сортировка по Причине обращения")
    print("4. Фильтр по Длительности")

    # Запрос выбора обработки данных у пользователя
    choice = input("Введите номер обработки: ")

    if choice == '4':
        # Если выбран фильтр по длительности, запросить критерий фильтрации
        criteria_value = int(input("Введите Длительность для фильтрации: "))
        # Обработка данных на основе выбора и критерия
        processed_data = processor.process_data(choice, criteria_value)
    else:
        # Обработка данных на основе выбора
        processed_data = processor.process_data(choice)

    # Вывод обработанных данных
    for item in processor.data_generator(processed_data):
        print(item)

    # Запрос у пользователя, нужно ли сохранить обработанные данные в файл
    save_changes = input("Хотите сохранить обработанные данные обратно в файл? (yes/no): ").lower()
    if save_changes == 'yes':
        # Сохранение изменений в файл CSV
        csv_data.save_data(processed_data)
        print("Изменения успешно сохранены.")
    else:
        print("Изменения не сохранены.")


if __name__ == "__main__":
    main()


# Изменения для git
# Второе изменение для бранчей
# Конфликт