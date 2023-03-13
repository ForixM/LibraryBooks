LibraryBooks

This website acts like an online store of books.
There is an accounts feature. The client is able to create an account and to log-in in order to access to all the website
functionalities.
Each user have a personal wallet that store how much virtual money they have in the website. With their balance, they
can buy book from other users.
Talking about buying books, each user can put up books for sale in order to fill their wallet.

There are two separate menus to see the books that each user created, and the books purchased by each user.
Of course, each user are able to edit their creations and also delete them !

---

<u>Dev report:</u>

Comparing to the CA1, I have cleaned-up the code and used more appropriately django functionalities. When before, i had
used mostly function to create views and hard-coded forms, I have now used entirely used class-based views and class-based
forms. On top of that, I overrided as much as possible class-based views functions.

Compared to the CA1, I added log-in and register functionalities. Now each book can be viewed and handled according to
who bought or created them. In addition to that, a money-like philosophy have been added. Each book have a custom price,
each account have their own balance, and with the latter, book can be purchased.

Now, all pages have their own or shared .css file.