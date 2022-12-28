# Network Project

Во время моей работы над ML проектом возникла проблема постоянного вылета
обучения по самым разным причинам. В основном это происходило из-за карточек, или, например,
память на процессоре во время подсчета метрик переполнялась другим процессом.
В результате, пропадало время обучения, если это происходило в нерабочее время.

Для решения этой проблемы я написал _tg-бота_, который присылает мне описание ошибки
в случае вылета.

Также, через него можно запустить заранее сконфигурированные эксперименты и просмотреть по каждому
из них текущие метрики для того, чтобы можно было постоянно иметь представление о текущем
состоянии эксперимента.

В этом репозитории находится код этого бота.

## Project Structure
* **src**: исходный код бота и код фейкового обучения (для того, чтобы не собирать _torch_ образ), 
котроый запускает конкретный экперимент в виде обычного цикла и в рандомный момент выбрасывает ошибку
для демонстрации работы бота
* **outputs**: папки с текущими метриками экспериментов (еще тут могут лежать чекпоинты)
* **launchers**: лаунчеры фейковых экспериментов
* **_bot_logs.json_**: прокси-файл для передачи описания ошибки клиенту

## Usage
В корневой директории проекта:
 ```
docker build -t tg_bot .
docker run tg_bot
 ```

Бот: _t.me/train_notifier_tester_bot_:

1. Пишем 
 ```
/start
 ```
2. Выпадает выбор: _Start_ / _Show_
3. Далее выбор размера модели: _Large_ / _Low_
4. И дальше выбор конкретного эксперимента
5. После этого заново выбор _Start_ / _Show_