#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector
from mysql.connector import Error,connection
import configparser


# ### Creating a database

# In[ ]:


#establishing the connection
conn = mysql.connector.connect(user='*******', password='********', host='127.0.0.1')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Dropping database ebookstore if already exists.
cursor.execute("DROP database IF EXISTS ebookstore")

#Preparing query to create a database
sql = "CREATE database ebookstore";

#Creating a database
cursor.execute(sql)

#Closing the connection
conn.close()


# ### Creating a Table

# In[ ]:



conn = mysql.connector.connect(user='*******', password='********', host='127.0.0.1', database='ebookstore')

cursor = conn.cursor()

#Dropping books table if already exists.
cursor.execute("DROP TABLE IF EXISTS books")

#Creating table as per requirement
query ='''CREATE TABLE books(Id int PRIMARY KEY AUTO_INCREMENT, Title TEXT,Author TEXT,Qty int)'''
cursor.execute(query)

#Creating a query to insert data into the table. Initial Id=3001, it will auto_incremented.
first_book = (3001,'A Tale of Two Cities','Charles Dickens',30)
cursor.execute('''INSERT INTO books(Id,Title,Author,Qty) VALUES(%s,%s,%s,%s)''',first_book)
conn.commit()

#Adding more books into the table. Id=NULL means the book Id is auto incremented whenever a new book is added to the table
bookstore = [('''Harry Potter and the Philosopher's Stone''','J.Kk Rowling',40),
             ('The Lion, the Witch and the Wardrobe','C.S. Lewis',25),
             ('The Lord of the Rings','J.R.R Tolkien',37),
             ('Alice Wonderland','Lewis Carroll',12)]

cursor.executemany('''INSERT INTO books(Id,Title,Author,Qty) VALUES(NULL,%s,%s,%s)''',bookstore)
conn.commit()

#Closing the connection
conn.close()


# ### The BookStore class contains all the user options

# In[42]:


class BookStore:
    def __init__(self):
        '''Connect to the database and enable the user menu.'''

        self.conn = mysql.connector.connect(user='*******', password='********', host='127.0.0.1',database='ebookstore')
        self.cursor = self.conn.cursor()
        
        if self.conn.is_connected():
            print('Connected to the Ebookstore database.\n')
            
    def addBook(self,title,author,qty):
        '''Adds the book to the ebookstore database'''
        try:       
            adding_query = '''INSERT INTO books(Id,Title,Author,Qty) VALUES(NULL,%s,%s,%s)'''
            data = (title,author,qty)
            self.cursor.execute(adding_query,data)
            self.conn.commit()
            
            self.cursor.execute('''SELECT * FROM books WHERE title=%s''',(title,))
            print('The information on the book you just added is as follows: ')
            print(self.cursor.fetchone())
            
        except Error as error:
            print(error)
    
    def updateBook(self,Id):
        '''Updates information on a particular Id of the book'''
        try:    
            #Showing the current info on the selected book to be updated
            self.cursor.execute('''SELECT * FROM books WHERE Id = %s''',(Id,))
        
            print("The current information on the selected book is as follows: ")
            print(self.cursor.fetchone())
            print('\n')
        
            #What should be updated?
            selection = 0 #Initiates the option to be selected.
            while (selection !=4):
                selection = int(input('Please enter the number corresponding to what you would like to change:\n'
                                  +'1. Title\n'+'2.Author\n'+'3.Quantity\n'+'4. No more updates\n'))
            
                if selection ==1:
                    Title = input("Please enter the new book title: ")
                    self.cursor.execute('''UPDATE books SET Title=%s WHERE Id=%s;''',(Title,Id))
                    self.conn.commit()
                
                elif selection ==2:
                    Author = input('''Please enter the new Author's name: ''')
                    self.cursor.execute('''UPDATE books SET Author=%s WHERE Id=%s''',(Author,Id))
                    self.conn.commit()
                
                elif selection ==3:
                    Qty = int(input("Please enter the new quantity of the selected book: "))
                    self.cursor.execute('''UPDATE books SET Qty=%s WHERE Id=%s''',(Qty,Id))
                    self.conn.commit()
                
                elif selection ==4:
                    print("No more changes to be made.\n")
                    break
                else:
                    print("Invalid Option. Please try again....\n")
                
            #Print the updated info on the selected book.
            self.cursor.execute('''SELECT * FROM books WHERE Id=%s''',(Id,))
            print('The updated information on the selected book is as follows: ')
            print(self.cursor.fetchone())
        
         
        except Error as error:
            print('Error: ',error)
            
    def deleteBook(self,Id):
        '''Deletes a book from the database'''
        query = '''DELETE FROM books WHERE Id=%s '''
    
        try:
            #execute the query
            self.cursor = conn.cursor()
            self.cursor.execute(query,(Id,))
            self.conn.commit()
        
        except Error as e:
            print(e)
        
    def searchBook(self,Id=0,Title="",Author=""):
        '''Searches a book in the database'''
        query = '''SELECT * FROM books WHERE Id=%s or Title=%s or Author=%s'''
        try:
            self.cursor.execute(query,(Id,Title,Author))
            #Print the results of your search
            print('Results from search: ')
            print(self.cursor.fetchone())
        
        except Error as error:
            print('Error: ',error)
    
book = BookStore()
#Closing the database and Cursor connections 
if book.conn is not None and book.conn.is_connected():
    book.conn.close()  
    book.cursor.close()


# ### The user_menu() function allows the user to pick any option of their choice, using the options they have from the BookStore class.

# In[44]:


def user_menu():
    '''User menu that allows the user to either add a book to a database, 
    Update information about the book already in the databse,Delete books from the database 
    and/or search for a book from the database.
    '''
    
    book = BookStore() 
    
    user_choice = int(input('Please select the number corresponding to what you would like to do: \n'
                            +'1.Enter book \n'
                            +'2.Update book\n'
                            +'3.Delete book \n'
                            +'4.Search book\n'
                            +'0.Exit the program \n'))
    
    if user_choice ==1:
        print('Enter the title of the book you would like to add to the databse. ')
        title = input('What is the title of the book you are adding to the database? \n')
        author = input('Who is the author of the book you are adding to the database? \n')
        qty = int(input('How many books of this title are present on our ebookstore? \n'))
        print(book.addBook(title,author,qty))
        print('\n')
        
    elif user_choice ==2:
        Id = int(input('What is the Id of the book you would like to update? '))       
        print(book.updateBook(Id))
        print('\n')
        
    elif user_choice ==3:
        Id = int(input('What is the Id of the book you would like to delete? '))
        print(book.deleteBook(Id))
        print('\n')
        
    elif user_choice ==4:
        Id_title_author = input('Please enter an Id and/or title and/or author of the book you are searching.')
        print(book.searchBook(Id_title_author))
        
    elif user_choice == 0:
        print('Thank you for using our bookstore. Stay safe....')
        
    else:
        print('Invalid option selected. Please try again.....')
    
    


# In[48]:


if __name__=='__main__':
    user_menu()


# In[ ]:




