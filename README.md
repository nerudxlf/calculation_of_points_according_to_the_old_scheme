# Программа для расчета баллов по схеме ОмГТУ 2020.

На входе используются таблицы, распределенные по квартилям из выгрузок WoS(w1.xlsx, w2.xlsx, w3.xlsx, w4.xlsx, w_none.xlsx) и Scopus(s1.xlsx, s2.xlsx, s3.xlsx, s4.xlsx, s_none.xlsx), за 2020 год

На выходе получается 8 таблиц со статьями, распределенные по баллам (70, 50, 30, 25, 18, 15, 9, 7)

Программа считает сумму баллов по всем статьями и выводит ее на экран

Используется библиотека pandas

Алгоритм программы:

total=0

1. *Построить общую таблицу All по всем публикациям WoS и Scopus (Названия, авторы, журнал)*

2. *Создать 70.xls по совпадениям названий в таблице All и w1, удалить из All все строки с совпадениями по w1
total = total + w1.count * 70 // число строк 70*

3. *Создать 50.xls по совпадениям "Title" в таблице All(после удаления это соответствует P1) и w2, удалить из All все строки с совпадениями по w2
total = total + w2.count * 50*

4. *Добавить в 50.xls по совпадения по "Title" из All в s1 публикации, удалить из All все строки с совпадениями по s1
total = total + s1.count * 50*

5. *Создать 30.xls по совпадениям "Title" в таблице All и s2, удалить из All все строки с совпадениями по s2
total = total + s2.count * 30*

6. *Создать 25.xls по совпадениям "Title" в таблице All и w3, удалить из All все строки с совпадениями по w3
total = total + w3.count * 25*

7. *Создать 18.xls по совпадениям "Title" в таблице All и w4, удалить из All все строки с совпадениями по w4
total = total + w4.count * 18*

8. *Создать 15.xls по совпадениям "Title" в таблице All и s3, удалить из All все строки с совпадениями по s3
total = total + s3.count * 15*

9. *Создать 9.xls по совпадениям "Title" в таблице All и s4, удалить из All все строки с совпадениями по s4
total = total + s4.count * 9*

10. *Создать 7.xls из оставшегося в таблице All
total = total + All.count * 7*

11. *Вывести: total*


Ссылки на проекты по разбиению публикаций по квартилям WoS(w1.xlsx, w2.xlsx, w3.xlsx, w4.xlsx, w_none.xlsx) и Scopus(s1.xlsx, s2.xlsx, s3.xlsx, s4.xlsx, s_none.xlsx)

Из Scopus: https://github.com/nerudxlf/get_affilietions_and_names_from_scopus

Из WoS: https://github.com/nerudxlf/getting_quartiles_wos
