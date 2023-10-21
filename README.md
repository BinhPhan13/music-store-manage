USTH ICT 2023 Advanced Programming with Python
=====================================================

Group 3 - DS: 
- Phan Thanh Bình BI12 - 059
- Trần Thế Trung BI12 - 452
- Trần Minh Trung BA11 - 093
- Châu Phan Phương Mai BI12 - 263
- Vũ Quỳnh Anh BI12 - 019

TOPIC 48: Music Store Management System
=====================================================

Note: change your resolution to 1366 x 768
Feature Introduction:
- Login: Enter correct admin name (Admin) and password(1234).
- Homepage: The total number of users, songs, categories, singers can be automatically updated 
- Userpage:
    + Show/Hide
    + Add (Note: user's id will be automatically created for a new user)
    + Update
    + Search: search by user's properties, can search by the range of user's year of birth (example: 2000_2003)
- Song Page:
    + Show/Hide
    + Add (Note: song's id will be automatically created for a new song)
    + Update
    + Search: search by song's properties, can search by the range of price and/or quantity
    + Delete
- Categoriy + Singer Page: filter the song of a chosen category/singer. Can choose multiple categories/singers
- Bill:
    + User Page (Button: Search,Confirm): choose one user to add bill
    + Second Page:
        _ Song table:
            * Search song:
            * Back: back to the user page to reselect user
            * Add: choose song to add to the cart
        _ Cart table:
            * Delete: delete a chosen song inside cart
            * Finish: Click finish to see the total price, the data will be pushed into the database
- Sale page:
    + Show the information of the added bills: user's id, user's name. song's id,song's name,date on which the user 
    purchased the music,price
    + If you want to know more about the details of the user and song, you can click the row of the table. 
    + Search: userid, songid, time(can search by range)
- Report:
    + Plot user gender, user age distribution (pie chart)
    + Plot top 10 users who have spent the most, top 10 highest earning songs(bar chart)
    + Plot the revenue of the last 5 days that have bills. 
