# Finder - музыкальный помощник.

##  Введение

В нынешнее время достаточно много различных музыкальных сервисов, что не может не радовать, но порой из-за этого сложно с кем-то поделиться своей музыкой. Приложение Finder поможет вам лего найти вашу любимую музыку в других сервисах и поделиться ей с другими.

## Дорожная карта проект
- [X] Сбор API различных музыкальных сервисов
- [X] Внедрение API в приложение
- [X] Создание удобно Web-UI
  
## Описание предлагаемого решения

>![](https://i.ibb.co/W2SpD7b/2022-07-20-193640.png)  
Шаг 1. Заходим на главную страничку и вводим в поисковой строке название песни(желательно с автором) или же вставляем ссылку с популярного источника.  

>![](https://i.ibb.co/KDqKbWq/2022-07-20-195247.png)  
Шаг 2. Получаем название найденной песни а так-же список платформ на которых она есть.

>![](https://i.ibb.co/pWk625L/2022-07-20-195206.png)
При желание можем "Лайкнуть" песню что бы добавить ее в наш плей лист. Но для этого нужно будет создать свой аккаунт.


## Оценка результатов и перспективы
Создание MVP данного проекта отвечает запланированным результатам ее работы.  

Как следствие, необходимо расширить количество платформ с которыми умеет взаимодействовать приложение. Так же требуется улучшение UI. По итогу можно будет залить данные проект на хостинг и пользоваться им как полноценным сайтом.

# Установка и запуск

Скачать проект
```bash
$ git clone https://github.com/OverHome/Finder.git
$ cd Finder
```
Установить нужные библиотеки
```bash 
$ pip install -r requirements.txt
```
Запустить приложение
```bash 
$ python main.py
```

Запустится Web-Приложение на адресе:
```
http://127.0.0.1:5000
```