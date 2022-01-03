#Item-Based Collaborative Filtering

#Importing the library
import pandas as pd

pd.set_option('display.max_columns', None)

#Loading the Data Set
book = pd.read_csv('book/Books.csv',low_memory=False)
rating = pd.read_csv('book/Ratings.csv',low_memory=False)
users = pd.read_csv('book/Users.csv',low_memory=False)

df1=book.merge(rating,how="left", on="ISBN")
df_=df1.merge(users,how="left", on="User-ID")

df=df_.copy()
df.head()

#Preparation of the Data Set

#Size of dataset
df.shape

#Deleting missing observations in the dataset
df.info()
df.dropna(inplace=True)

#Converting User-ID and Age variable types to int
df['User-ID'] = df['User-ID'].astype('int')
df['Age'] = df['Age'].astype('int')

#Author of The Da Vinci Code written in two different ways
df["Book-Author"]=df["Book-Author"].astype("string")
df["Book-Author"]=df["Book-Author"].str.replace("DAN BROWN","Dan Brown")

#Author of Dreamcatcher book correcting incorrect entries
df["Book-Author"]=df["Book-Author"].str.replace("Audrey Osofsky","Stephen King")
df["Book-Author"]=df["Book-Author"].str.replace("Dinah McCall","Stephen King")

#Extracting Image URL from dataset
df.drop(columns=["Image-URL-S","Image-URL-M"],inplace=True)

#Removing books with zero ratings from the data set
df=df[df["Book-Rating"]>0]
df["Book-Rating"].describe()

#Unique reader count
df["User-ID"].nunique()

#Unique number of books
df["Book-Title"].nunique()

#We found how many books users read
df.groupby('User-ID')['Book-Title'].agg('count').sort_values()

#How many times have we read which book?
book_counts = pd.DataFrame(df["Book-Title"].value_counts())

#Most read books
book_counts.sort_values("Book-Title", ascending=False)

#We named the books with less than 100 reads as rare books.
rare_book = book_counts[book_counts["Book-Title"] <= 100].index

#Number of rarely read books
rare_book.nunique()

#By removing the rare books from the dataset, we found the widely read books
common_book = df[~df["Book-Title"].isin(rare_book)]
common_book.head()

#User-Book matrix
user_book_df = common_book.pivot_table(index=["User-ID"], columns=["Book-Title"], values="Book-Rating")
user_book_df


#We chose a book
book_name="The Da Vinci Code"

#We found the points given to the book
book_name=user_book_df[book_name]
book_name.sort_values(ascending=False)

user_book_df.corrwith(book_name).sort_values(ascending=False).head()

rec_book=user_book_df.corrwith(book_name).sort_values(ascending=False).head()
rec_book_list=list(rec_book.index)

rec_book_list

# ['The Da Vinci Code',
#  'The Divine Secrets of the Ya-Ya Sisterhood: A Novel',
#  "Ender's Game (Ender Wiggins Saga (Paperback))",
#  "Where the Heart Is (Oprah's Book Club (Paperback))",
#   'Dreamcatcher']

#Authors of 5 books we recommend
df_author=df[["Book-Title","Book-Author"]]
df_author.head()

df1 = df_author.loc[df_author["Book-Title"].isin(rec_book_list)]

df2=df1.drop_duplicates(subset=["Book-Author","Book-Author"], keep="first")
df2
df2.shape












