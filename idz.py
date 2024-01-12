import tabulate
import sqlite3
# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("db/store.sqlite")
# открываем файл с дампом базой двнных
f_damp = open('db/store.db','r', encoding ='utf-8-sig') # читаем данные из файла
damp = f_damp.read()
# закрываем файл с дампом
f_damp.close()
# запускаем запросы
con.executescript(damp)
# сохраняем информацию в базе данных
con.commit()
# создаем курсор
cursor = con.cursor()

# 1
# Вывести названия, авторов и цену тех книг, которые относятся 
# к жанру Роман, и их цена больше 300 и меньше 600 рублей.
cursor.execute("""
            SELECT title,name_author, price
            FROM book
            JOIN author ON author.author_id = book.author_id
            JOIN genre ON genre.genre_id = book.genre_id
            WHERE 300 < price AND price < 600 ;  
            """)
res = tabulate.tabulate(cursor.fetchall())
print("Задание 1\n"+res + "\n")

# 2
# Вывести фамилии клиентов, (без повторений) в заказах которых есть хотя бы одна книга,
# заказанная в двух и более экземплярах. 
# Информацию отсортировать по фамилии клиентов в алфавитном порядке.
cursor.execute("""
            SELECT DISTINCT name_client 
            FROM client
            JOIN buy ON client.client_id = buy.client_id
            WHERE buy_id IN(
                SELECT buy_id 
                FROM buy_book
                GROUP BY book_id
                HAVING COUNT(buy_id) > 1)
            ORDER BY name_client;
            """)
res = tabulate.tabulate(cursor.fetchall())
print("Задание 2\n"+res + "\n")

# 3
# Вывести название книг и их авторов, заказанных самыми активными покупателями. 
# Самыми активными считать покупателей, которые сделали заказ на максимальную сумму 
# по сравнению с другими заказами.
cursor.execute("""
            SELECT title,
                name_author
            FROM book
            JOIN buy_book ON buy_book.book_id = book.book_id
            JOIN buy ON buy.buy_id = buy_book.buy_id
            JOIN author ON author.author_id = book.author_id
            GROUP BY buy_book.buy_id
            HAVING MAX(buy_book.amount * book.price);
            """)
res = tabulate.tabulate(cursor.fetchall())
print("Задание 3\n"+res + "\n") 

# 4
# Создать таблицу good_order, в которую включить книги и их авторов, 
# а также количество экземпляров книг, которое нужно заказать. 
# Количество экземпляров указать такое, чтобы на складе (после получения книг) 
# было одинаковое количество книг каждого автора, равное максимальному
# количеству книг этого автора. Последний столбец назвать Заказ. 
# Если количество заказываемой книги равно 0, эту книгу в таблицу не включать.
cursor.executescript("""
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
               """)
con.commit()
cursor.execute("""
            SELECT * FROM good_order;
               """)
res = tabulate.tabulate(cursor.fetchall())
print("Задание 4\n"+res + "\n")  

# Вывести автора, стоимость книги, имеющейся в наличии в магазине, а также стоимость книг каждого автора с "накоплением".
# Столбцы назвать Автор, Книга, Стоимость, Стоимость_с_накоплением. Информацию отсортировать по фамилии автора в обратном
# алфавитном порядке, а затем по возрастанию стоимости.
# Пояснение. Стоимость "с накоплением" означает, что в текущей строке выводится сумма стоимостей книг всех предыдущих
# строк этого столбца и текущей строки.
#Примечание. Для решения задания № 5 использовать оконные функции.
cursor.executescript("""
            
               """)
con.commit()
cursor.execute("""
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
               """)
res = tabulate.tabulate(cursor.fetchall())
print("Задание 5\n"+res + "\n")  
# закрываем соединение с базой
con.close()