# Тест-кейс для тестирования API управления сущностями
## Название тест-кейса
### Проверка основных операций CRUD для API управления сущностями
## Описание
Данный тест-кейс проверяет основные операции создания, чтения, обновления и удаления сущностей через API.
## Предусловия

Тестовое окружение настроено и доступно
API-клиент инициализирован и готов к работе
Подготовлены тестовые данные (json_data, json_data_for_patch)
Фикстуры pytest настроены (api_client, json_data, created_entity_id, json_data_for_patch)

## Шаги и ожидаемые результаты
### Тест 1: Создание сущности
### Шаги:

Отправить запрос на создание сущности с тестовыми данными
Проверить, что возвращен корректный ID сущности
Получить созданную сущность по ID
Сравнить полученные данные с исходными тестовыми данными
Удалить созданную сущность (очистка)
Ожидаемые результаты:

API возвращает числовой ID для созданной сущности
Статус-код получения сущности равен 200
Данные полученной сущности (без полей ID) совпадают с исходными тестовыми данными

### Тест 2: Удаление сущности
### Шаги:

Удалить сущность с заданным ID
Попытаться получить удаленную сущность
Ожидаемые результаты:

Статус-код удаления равен 204
При попытке получить удаленную сущность возвращается статус-код, отличный от 200, или возникает исключение

### Тест 3: Получение сущности по ID
### Шаги:

Получить сущность по заданному ID
Проверить корректность полученных данных
Ожидаемые результаты:

Статус-код получения сущности равен 200
Данные полученной сущности (без полей ID) совпадают с исходными тестовыми данными

### Тест 4: Получение списка всех сущностей
### Шаги:

Получить список всех сущностей
Проверить, что созданная тестовая сущность присутствует в списке
Ожидаемые результаты:

Статус-код получения списка равен 200
В списке найдена созданная тестовая сущность

### Тест 5: Обновление сущности
### Шаги:

Обновить сущность с заданным ID, используя данные для патча
Получить обновленную сущность
Проверить, что данные сущности обновились корректно
Ожидаемые результаты:

Статус-код обновления равен 204
Данные полученной сущности (без полей ID) совпадают с данными для патча

### Постусловия

Все созданные в ходе тестирования сущности удалены
Тестовое окружение приведено в исходное состояние
### Приоритет
Критический (для тестов создания, обновления и удаления)
Нормальный (для тестов получения)Автоматизация
Тест полностью автоматизирован с использованием pytest и Allure для отчетности.
Дополнительная информация

Тест использует Pydantic-модели для валидации данных
Allure используется для создания подробных отчетов о выполнении тестов
Тест включает в себя очистку созданных данных для предотвращения загрязнения тестовой среды




# Тест-кейсы для управления клиентами в банковском проекте

## Тест-кейс 1: Добавление нового клиента

**ID**: TC-CM-001  
**Название**: Проверка успешного добавления нового клиента в систему  
**Приоритет**: Высокий  
**Серьезность**: Критическая

### Предусловия:

-   Банковское приложение доступно
-   Пользователь имеет привилегии менеджера

### Шаги тестирования:

1.  Перейти на страницу менеджера
2.  Нажать на опцию "Добавить клиента"
3.  Сгенерировать случайные данные клиента:
    -   Имя на основе почтового индекса
    -   Фамилия (значение по умолчанию)
    -   Случайный почтовый индекс
4.  Заполнить форму клиента сгенерированными данными
5.  Проверить, что поля формы отображают правильные данные
6.  Отправить форму клиента
7.  Проверить сообщение в уведомлении

### Ожидаемые результаты:

-   Форма должна принять все введенные значения
-   После отправки должно появиться уведомление с сообщением "Customer added successfully" (Клиент успешно добавлен)
-   Новый клиент должен быть добавлен в систему

### Постусловия:

-   Клиент доступен в списке клиентов

----------

## Тест-кейс 2: Сортировка списка клиентов

**ID**: TC-CM-002  
**Название**: Проверка возможности сортировки клиентов по имени  
**Приоритет**: Средний  
**Серьезность**: Нормальная

### Предусловия:

-   Банковское приложение доступно
-   Пользователь имеет привилегии менеджера
-   В системе существует как минимум один клиент

### Шаги тестирования:

1.  Перейти на страницу менеджера
2.  Добавить нового клиента с сгенерированными данными (следуя шагам из TC-CM-001)
3.  Нажать на опцию "Клиенты" для просмотра списка клиентов
4.  Нажать на заголовок столбца "Имя" для сортировки клиентов по имени
5.  Проверить, что клиенты отсортированы в порядке убывания

### Ожидаемые результаты:

-   Список клиентов должен быть отсортирован по имени в порядке убывания
-   Порядок сортировки должен быть правильно применен

### Постусловия:

-   Список клиентов остается отсортированным, пока не будет выбран другой вариант сортировки

----------

## Тест-кейс 3: Удаление клиента со средней длиной имени

**ID**: TC-CM-003  
**Название**: Проверка возможности удаления клиентов со средней длиной имени  
**Приоритет**: Средний  
**Серьезность**: Нормальная

### Предусловия:

-   Банковское приложение доступно
-   Пользователь имеет привилегии менеджера
-   В системе существует несколько клиентов с разной длиной имен

### Шаги тестирования:

1.  Перейти на страницу менеджера
2.  Добавить нового клиента с сгенерированными данными (следуя шагам из TC-CM-001)
3.  Нажать на опцию "Клиенты" для просмотра списка клиентов
4.  Отсортировать клиентов по имени в порядке убывания
5.  Рассчитать среднюю длину имен клиентов
6.  Удалить клиента, длина имени которого близка к средней длине
7.  Проверить, что удаленный клиент больше не отображаются в списке

### Ожидаемые результаты:

-   Система должна определить клиентов со средней длиной имени
-   Выбранные клиенты должны быть успешно удалены
-   Список клиентов должен обновиться, отражая удаления
-   Удаленные клиенты больше не должны отображаться в списке

### Постусловия:

-   Список клиентов обновлен и содержит оставшихся клиентов
-   Удаленные клиенты окончательно удалены из системы
