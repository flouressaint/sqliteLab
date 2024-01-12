SELECT title,
    name_author
FROM book
    JOIN buy_book ON buy_book.book_id = book.book_id
    JOIN buy ON buy.buy_id = buy_book.buy_id
    JOIN author ON author.author_id = book.author_id
GROUP BY buy_book.buy_id
HAVING MAX(buy_book.amount * book.price);
--  4
--  Создать таблицу good_order, в которую включить книги и их авторов, 
--  а также количество экземпляров книг, которое нужно заказать. 
--  Количество экземпляров указать такое, чтобы на складе (после получения книг) 
--  было одинаковое количество книг каждого автора, равное максимальному
--  количеству книг этого автора. Последний столбец назвать Заказ. 
--  Если количество заказываемой книги равно 0, эту книгу в таблицу не включать.
DROP TABLE IF EXISTS good_order;
CREATE TABLE good_order (
    title VARCHAR(255),
    name_author VARCHAR(255),
    "Заказ" INTEGER
);
INSERT INTO good_order (title, name_author, "Заказ")
SELECT title,
    name_author,
    max_amount.amount - (book.amount - buy_book.amount) AS "Заказ"
FROM book
    JOIN author ON author.author_id = book.author_id
    JOIN buy_book ON buy_book.book_id = book.book_id
    JOIN (
        SELECT author_id,
            MAX(book.amount) as amount
        FROM book
        GROUP BY author_id
    ) AS max_amount ON max_amount.author_id = author.author_id
WHERE max_amount.amount - (book.amount - buy_book.amount) > 0;
SELECT *
FROM good_order;
--  Вывести автора, стоимость книги, имеющейся в наличии в магазине, а также стоимость книг каждого автора с "накоплением".
--  Столбцы назвать Автор, Книга, Стоимость, Стоимость_с_накоплением. Информацию отсортировать по фамилии автора в обратном
--  алфавитном порядке, а затем по возрастанию стоимости.
--  Пояснение. Стоимость "с накоплением" означает, что в текущей строке выводится сумма стоимостей книг всех предыдущих
--  строк этого столбца и текущей строки.
-- Примечание. Для решения задания № 5 использовать оконные функции.
SELECT name_author AS "Автор",
    title AS "Книга",
    price AS "Стоимость",
    COAlESCE(
        lag(price) over (
            PARTITION BY name_author
            ORDER BY name_author DESC,
                price
        ),
        0
    ) + price AS "Стоимость_с_накоплением"
FROM book
    JOIN author ON author.author_id = book.author_id
WHERE book.amount > 0;