# Программа для расчета баллов по текущей схеме.

На входе используются таблицы, распределенные по квартилям из выгрузок WoS и Scopus:

w1.xlsx, w2.xlsx, w3.xlsx, w4.xlsx, w_none.xlsx, s1.xlsx, s2.xlsx, s3.xlsx, s4.xlsx, s_none.xlsx

На выходе получается 8 таблиц со статьями, распределенные по баллам (70, 50, 30, 25, 18, 15, 9, 7)

Программа считает сумму баллов по всем статьями и выводит ее на экран

Используется библиотека pandas

Алгоритм программы:

total=0

1. *Построить общую таблицу All (Названия, авторы, журнал)*

2. *Создать 70.xls по совпадениями названий в таблице All и W1, удалить из All все строки с совпадениями по W1
total = total + W1.count 70 // число строк 70*

3. *Создать 50.xls по совпадениями "Title" в таблице All(после удаления это соответствует P1) и W2 , удалить из All все строки с совпадениями по W2
total = total + W2.count * 50*

4. *Добавить в 50.xls по совпадению по "Title" из All в S1 публикации, удалить из All все строки с совпадениями по S1
total = total + S1.count * 50*

5. *Создать 30.xls по совпадениями "Title" в таблице All и S2, удалить из All все строки с совпадениями по S2
total = total + S2.count * 30*

6. *Создать 25.xls по совпадениями "Title" в таблице All и W3, удалить из All все строки с совпадениями по W3
total = total + W3.count * 25*

7. *Создать 18.xls по совпадениями "Title" в таблице All и W4, удалить из All все строки с совпадениями по W4
total = total + W4.count * 18*

8. *Создать 15.xls по совпадениями "Title" в таблице All и S3, удалить из All все строки с совпадениями по S3
total = total + S3.count * 15*

9. *Создать 9.xls по совпадениями "Title" в таблице All и S4, удалить из All все строки с совпадениями по S4
total = total + S4.count * 9*

10. *Создать 7.xls из оставшегося в таблице All
total = total + All.count * 7*

11. *Вывести: total*


Ссылкы на проекты с получением квартилей

Из Scopus: https://github.com/nerudxlf/get_affilietions_and_names_from_scopus

Из WoS: https://github.com/nerudxlf/getting_quartiles_wos
