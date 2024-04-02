# BibelBarn

Website for a library

Planned pages
    Guests:
    -   Home
    -   Books
    -   Rooms
    -   Login/Register
    Users:
    -   Home
    -   Books
    -   Rooms
    -   Profile
    Admin:
    - Books
    - Users
    - ???
    - ???

Planned features:

- Login/Register User ( using javascript for pwd req)
- Rent Book + How many availible + if unavailible
- Book rooms
  Bonus Features
- Upload Profile Image
- Bio
- Show what books they have and how long they have left of it
- Contact support?
- Security?
- Have a queue you can enter for a book?
- Admin page, with overview of users, ability to delete users.




STRUKTUR FRA DB FAG:

1. **BookID → Title, AuthorID, AuthorName, Genre, Publisher, ISBN, ReturnDate, FineAmount**
   * The BookID uniquely determines all other attributes in the table.
2. **AuthorID → AuthorName**
   * The AuthorID uniquely determines the AuthorName.
3. **BorrowerID → BorrowerName**
   * The BorrowerID uniquely determines the BorrowerName.
4. **ISBN → Title**
   * The ISBN uniquely determines the Title.
5. **BookID, BorrowerID → ReturnDate, FineAmount**
   * The combination of BookID and BorrowerID uniquely determines the ReturnDate and FineAmount.
