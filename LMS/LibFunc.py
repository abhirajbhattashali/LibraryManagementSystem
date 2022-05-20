"""THIS IS LIBFUNCTION MODULE """
import os
import matplotlib.pyplot as plt
import pandas as pd


# File Handling Functions
def is_file_ext_csv(p):
    if '.csv' not in p:
        return False
    else:
        return True


def file_validator(path):
    if os.path.isfile(path):
        if is_file_ext_csv(path):
            return True
        else:
            print("\tFile Extension should be .csv only")
            return False
    else:
        print(f'\tNo file exists having path {path}')
        return False


def open_file():
    index_cols = ["BookNo", "IssId", 'MNo']
    table_names = ["Book_Details Table", "Issue Table", "Membership Table"]
    df_list = []
    path_list = []
    for i in range(3):
        path = input(f'\tEnter Path of file where {table_names[i]} data is to be retrieved: ')
        while True:
            validity = file_validator(path)
            if not validity:
                path = input(f'\tRe-enter Path of file where {table_names[i]} data is to be retrieved: ')
            else:
                df = pd.read_csv(path, index_col=index_cols[i])
                df_list.append(df)
                path_list.append(path)
                break
    return path_list, df_list


def create_file_dir(dir1, df1, df2, df3):
    folder = input('\tEnter name of folder: ')
    folder_path = os.path.join(dir1, folder)
    while os.path.exists(folder_path):
        print("\tA Folder already exists at the current directory by the same name , re enter name of folder: ")
        folder = input('\tRe enter name of folder: ')
        folder_path = os.path.join(dir1, folder)
    os.makedirs(folder_path)
    os.chdir(folder_path)
    file1 = input("\tEnter name of file where Book Details Table data is to be saved: ")
    while not is_file_ext_csv(file1):
        print("\tFile Extension should be .csv")
        file1 = input("\tRe-enter name of file where Book Details Table data is to be saved: ")

    file2 = input("\tEnter name of file where Book Issue Table data is to be saved:  ")
    while not is_file_ext_csv(file2):
        print("\tFile Extension should be .csv")
        file2 = input("\tRe-enter name of file where Issue Table data is to be saved: ")

    file3 = input("\tEnter name of file where Member data is to be saved:  ")
    while not is_file_ext_csv(file3):
        print("\tFile Extension should be .csv")
        file3 = input("\tRe-enter name of file where Member data is to be saved: ")

    df1.to_csv(file1, index_label="BookNo")
    df2.to_csv(file2, index_label="IssId")
    df3.to_csv(file3, index_label="MNo")
    path_list = [os.path.join(folder_path, file1), os.path.join(folder_path, file2), os.path.join(folder_path, file3)]
    return path_list


# Dataframe Display Function
def display(df):
    if df.empty:
        print("\tCan't Display Records since Dataframe is empty.")
    else:
        print("-" * 200)
        print(df)


def enter_member_details(df):
    mno = int(input('\tEnter Member No:'))
    while mno in df.index:
        print('\tA Member is already registered in the Membership table by this Member No')
        mno = int(input('\tRe-enter Member No: '))
    mname = input('\tEnter Member\'s Name: ')
    mtype = input('\tEnter type of Membership (Standard or Premium):')
    while mtype not in ['Standard', 'Premium']:
        print('\tInvalid Membership Type ')
        mtype = input('Re-enter type of Membership (Standard or Premium):')
    sec_amt = int(input('\tSecurity Amount: '))
    mdate = input('\tEnter Date of Membership :')
    mstatus = 'Ac'
    df.loc[mno, :] = [mname, mtype, sec_amt, mdate, mstatus]
    print('-' * 200)


# Membership Table Functions
def update_member_details(df, ch, mno):
    # columns=['MName', 'Type', 'Security_Amt', 'MDate', 'MStatus']
    if ch == 1:
        up_mno = int(input('\t Enter Updated Member No: '))
        while up_mno in df.index:
            print('\tA Member already exists in the Membership Table by this Member No')
            up_mno = int(input('\t Renter Updated Member No: '))
        df.rename(index={mno: up_mno}, inplace=True)
    elif ch == 2:
        up_mname = input('\tEnter Updated Member\'s Name: ')
        df.at[mno, "MName"] = up_mname
    elif ch == 3:
        up_mtype = input('\tEnter type of Membership (Standard or Premium): ')
        while up_mtype not in ['Standard', 'Premium']:
            print('\tInvalid Membership Type ')
            up_mtype = input('\tRenter type of Membership (Standard or Premium): ')
        df.at[mno, "Type"] = up_mtype
    elif ch == 4:
        up_sec_amt = int(input('\tSecurity Amount'))
        df.at[mno, 'Security_Amt'] = up_sec_amt
    elif ch == 5:
        up_mdate = input('\tEnter Date of Membership : ')
        df.at[mno, 'MDate'] = up_mdate
    elif ch == 6:
        ans = input(f'\tDo you really want to Deactivate Library Membership Status of {df.at[mno, "MName"]}')
        if ans == 'yes':
            df.at[mno, 'MStatus'] = 'NAc'
    elif ch == 7:
        df.at[mno, 'MStatus'] = 'Ac'


# Issue Table Functions


def delete_iss_records(df_iss, df_bd, issid):
    print('\t', '\tThe Issue record having Issue Id :', issid, ' of Member ', df_iss.at[issid, "MName"],
          ' have been deleted successfully.')
    df_bd.at[df_iss.at[issid, "BookNo"], "Status"] = "Available"
    df_iss.drop(issid, inplace=True)


def return_date_validator(issdate, rdate, isssep, rsep):
    issval = issdate.split(isssep)
    rval = rdate.split(rsep)
    return_date1 = rdate
    while True:
        if int(rval[2]) < int(issval[2]):
            cr_year = input('\t\tEnter correct year: ')
            rval[2] = cr_year
            return_date1 = rsep.join(rval)
        elif int(rval[2]) == int(issval[2]):
            list1 = ["day", "month"]
            for z in range(1, -1, -1):
                while int(rval[z]) < int(issval[z]):
                    if z == 0:
                        if rval[1] > issval[1]:
                            break
                    x = input('\t\tEnter correct ' + list1[z] + ": ")
                    rval[z] = x
                    return_date1 = rsep.join(rval)
                else:
                    continue
            else:
                break
    return return_date1


def calc_retaining_period(issue_date, return_date, issep, rsep):
    isval = issue_date.split(issep)
    rval = return_date.split(rsep)
    for i in range(3):
        isval[i] = int(isval[i])
        rval[i] = int(rval[i])
    month_index = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if isval[2] % 400 == 0:
        month_index[2] = 29
    if rval[1] == isval[1] and rval[2] == isval[2]:
        retaining_period = rval[0] - isval[0]
    elif rval[1] != isval[1] and rval[2] == isval[2]:
        days = 0
        for i in range(isval[1], rval[1]):
            days = days + month_index[i]
        retaining_period = days + rval[0] - isval[0]
    else:
        days = 0
        for i in range(isval[1], 12 + rval[1]):
            if i > 12:
                days = days + month_index[i - 12]
            else:
                days = days + month_index[i]
        retaining_period = days + rval[0] - isval[0]
    return retaining_period


def calc_fine(retaining_period, fine_amt):
    if retaining_period > 7:
        return (retaining_period - 7) * fine_amt
    else:
        return 0


# Book Details Table Functions
def enter_book_details(df):
    bookno = int(input('\tEnter Book No: '))
    while bookno in df.index:
        print('\tA book already exists by this Book No ')
        bookno = int(input('\tRe-enter Book No: '))

    title = input('\tEnter Book title: ')
    while title in df.Title.values:
        print('\tA book already exists by this Title ')
        title = input('\tRe-enter Book title: ')

    genre = input("\tEnter Genre of book: ")
    author = input("\tEnter Name of Author: ")
    publ = input("\tEnter Book's Publication: ")
    price = int(input("\tEnter Price: "))
    quantity = int(input("\tEnter Quantity: "))
    status = "Available"
    df.loc[bookno, :] = [title, genre, author, publ, price, quantity, status]
    print('-' * 200)


def update_book_records(df, ch, bookno):
    if ch == 1:
        new_bookno = int(input("\tEnter new bookno: "))
        while new_bookno in df.index:
            print('\tA book already exists by this Book No ')
            new_bookno = int(input('\tRenter Book No: '))
        df.rename(index={bookno: new_bookno}, inplace=True)
    elif ch == 2:
        up_btitle = input("\tEnter updated bookTitle: ")
        while up_btitle in df.Title.values:
            print('\tA book already exists by this Title ')
        up_btitle = input('\tRenter Book title: ')
        df.at[bookno, "Title"] = up_btitle
    elif ch == 3:
        up_bgenre = input("\tEnter updated Genre: ")
        df.at[bookno, "Genre"] = up_bgenre
    elif ch == 4:
        correct_author_name = input("\tEnter correct Author's Name: ")
        df.at[bookno, "Author"] = correct_author_name

    elif ch == 5:
        up_publication = input("\tEnter updated Publication ")
        df.at[bookno, "Publication"] = up_publication
    elif ch == 6:
        new_price = int(input("\tEnter updated Price: "))
        df.at[bookno, "Price"] = new_price
    elif ch == 7:
        up_quantity = int(input("\tEnter updated Quantity: "))
        df.at[bookno, "Quantity"] = up_quantity
    elif ch == 8:
        up_status = input('\tEnter Updated Status: ')
        while up_status not in ["Available", "Issued"]:
            print("Invalid Book Status")
            up_status = input('\tRenter Book Status: ')
        df.at[bookno, "Status"] = up_status


def delete_book_records(df1, b_no, df2=None):
    print('\t', 'The details of the book ', df1.at[b_no, "Title"],
          'has been removed successfully from Book Details Table.')
    df1.drop(b_no, inplace=True)
    if not df2.empty:
        for issId, no in df2["BookNo"].items():
            if no == b_no:
                df2.drop(issId, inplace=True)
            else:
                continue


def search_record(df, val):
    for col in df.columns:
        fetched_df = df[df[col] == val]
        if not fetched_df.empty:
            return fetched_df

    return


def display_pie(df):
    plt.pie(df.Quantity.values, labels=df.Title, autopct="%4.2f%%")
    plt.title('Pie Chart Representing Books Quantity Distribution')
    plt.show()


def display_hist(df):
    plt.hist(df.Price)
    plt.title('Histogram representing Frequency Distribution of Prices of Books')
    plt.xticks(ticks=df.Price)
    plt.xlabel('Prices')
    plt.ylabel("Total No of Books")
    plt.show()
