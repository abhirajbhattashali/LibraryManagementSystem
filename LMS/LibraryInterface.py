from LMS import LibFunc
import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print('-' * 200)
print('\tLibrary Management System')
print('-' * 200)

Book_Details = pd.DataFrame(columns=["Title", 'Genre', 'Author', 'Publication', 'Price', 'Quantity', 'Status'], dtype='object')
Issue_records = pd.DataFrame(columns=["BookNo", 'Title', 'Mem_No', 'MName', 'Issue_date', 'Return_date',
                                      'DaysLate', 'Fine'], dtype='object')
Membership_records = pd.DataFrame(columns=['MName', 'Type', 'Security_Amt', 'MDate', 'MStatus'], dtype='object')

# File IO Operation (File Handling)

print('\t1. Create Folder')
print('\t2. Open File')
file_ch = int(input('\tEnter your choice: '))
print('-' * 200)
while True:
    if file_ch == 1:
        dir1 = input('\tEnter Name of Directory: ')
        file_exists=os.path.isdir(dir1)

        while not file_exists:
            print(f'\t{dir1} Directory does not exists.')
            dir1 = input('\tRe-enter Name of Directory: ')
        else:
            if file_exists:
                print("A Directory Already exists")
            path_list = LibFunc.create_file_dir(dir1, Book_Details, Issue_records, Membership_records)
            path_bd, path_iss, pathm = path_list
            print('-' * 200)
        break
    elif file_ch == 2:
        values = LibFunc.open_file()
        path_list = values[0]
        path_bd, path_iss, pathm = path_list
        df_list = values[1]
        Book_Details = df_list[0]
        Issue_records = df_list[1]
        Membership_records = df_list[2]
        print('-' * 200)
        break
    else:
        print("\tInvalid Choice!")
        print('-' * 200)
        file_ch = int(input('\tRe-enter your choice'))

# Main Menu start here
while True:
    print("\t1. Enter Details")
    print("\t2. Update Records")
    print("\t3. Delete Records")
    print("\t4. View Tables")
    print("\t5. View Statistics")
    print("\t6. Search")
    print("\t7. Exit")
    ch = int(input('\tEnter your choice (1 to 6): '))
    print('-' * 200)
    if ch == 1:
        print('\t1. Enter Book_Details Table Details: ')
        print('\t2. Enter Membership Details: ')
        print('\t3. Enter Book Issue Details: ')
        print('\t4. Press any other number to exit')
        enter_ch = int(input('\tEnter your choice: '))
        for i in range(1, 4):
            if enter_ch == 1:
                LibFunc.enter_book_details(Book_Details)
                break
            elif enter_ch == 2:
                LibFunc.enter_member_details(Membership_records)
                break
            elif enter_ch == 3:
                print('\t1. Issue a Book: ')
                print('\t2. Return a Book: ')
                print("\t3. Press any other number to exit")
                issue_choice = int(input('\tEnter your choice (1 to 2): '))
                retaining_period = 0
                ndayslate = 0
                fine = 0
                fine_amt = 2
                if issue_choice == 1:
                    if len(Issue_records) == 0:
                        Issue_Id = int(input('\t\tEnter First Issue ID: '))
                    else:
                        Issue_Id = Issue_records.index.max() + 1

                    MNo = int(input('\t\tEnter Member No: '))
                    if MNo not in Membership_records.index:
                        print('\t\tNo Member is registered in the Membership Table having MemberNo: ', MNo)
                        print('-' * 200)
                        break
                    elif Membership_records.at[MNo, "MStatus"] != 'Ac':
                        print('\t\t', 'Member', Membership_records.at[MNo, "MName"], "having Member No:", MNo,
                              "is not an Active Member")
                        print('-' * 200)
                        break
                    else:
                        mem_name = Membership_records.at[MNo, 'MName']
                    bookno = int(input('\t\tEnter Book No: '))
                    if bookno not in Book_Details.index:
                        print('\t\tNo Book is registered in the Book Book_Details  Table having Book No: ', bookno)
                        print('-' * 200)
                        break
                    if Book_Details.at[bookno, 'Status'] == "Issued":
                        print('\t\t', "Book ", Book_Details.at[bookno, "Title"], " is already issued")
                        print('-' * 200)
                        break
                    return_date = None
                    # Date Format : dd-mm-yyyy
                    issue_date = input('\t\tEnter Date of Issue: (Format dd-mm-yyyy) ')
                    iss_sep = ''
                    for ch in issue_date:
                        if not ch.isdigit():
                            iss_sep = ch
                            break
                    title = Book_Details.at[bookno, "Title"]
                    Book_Details.at[bookno, "Status"] = "Issued"
                    Issue_records.at[Issue_Id, :] = [bookno, title, MNo, mem_name, issue_date, return_date, ndayslate,
                                                     fine]
                    print('-' * 200)
                    break
                elif issue_choice == 2:
                    Issue_Id = int(input('\t\tEnter Issue Id of the Book: '))
                    if Issue_Id in Issue_records.index:
                        issue_date = Issue_records.at[Issue_Id, "Issue_date"]
                        iss_sep = ''
                        for ch in issue_date:
                            if not ch.isdigit():
                                iss_sep = ch
                                break
                        return_date = input('\t\tEnter Date of Return: (Format dd-mm-yyyy) ')
                        rsep = ''
                        for ch in return_date:
                            if not ch.isdigit():
                                rsep = ch
                                break

                        # Return Date validation
                        return_date = LibFunc.return_date_validator(issue_date, return_date, iss_sep, rsep)
                        Book_Details.at[Issue_records.at[Issue_Id, "BookNo"], 'Status'] = "Available"

                        # Fine Calculation
                        retaining_period = LibFunc.calc_retaining_period(issue_date, return_date, iss_sep, rsep)
                        if retaining_period > 7:
                            ndayslate = retaining_period - 7
                        fine = 'Rs ' + str(LibFunc.calc_fine(retaining_period, fine_amt))
                        Issue_records.loc[Issue_Id, 'Return_date':'Fine'] = [return_date, ndayslate, fine]
                        print('-' * 200)
                        break
                    else:
                        print('\t\tNo record exists in the Issue Table having Issue Id:', Issue_Id)
                        print('-' * 200)
                else:
                    print('-' * 200)
                    break

            else:
                print('-' * 200)
                break
    elif ch == 2:
        print('\t1. Update Book_Details Table Records')
        print('\t2. Update Membership Records')
        print("\t3. Press any other number to exit")
        table_ch = int(input('\tEnter your choice: (1 to 2)'))
        if table_ch == 1:
            if Book_Details.empty:
                print("\tBook Details Table is empty , can't update records without entering.")
            else:
                bookno = int(input('\tEnter bookno of the book whose details is to be updated: '))
                if bookno in Book_Details.index:
                    print("\t1. \tUpdate Book Number: ")
                    print("\t2. \tUpdate Book Title: ")
                    print("\t3. \tUpdate Book Genre: ")
                    print("\t4. \tUpdate Author's Name: ")
                    print("\t5. \tUpdate Author's Publication: ")
                    print("\t6. \tUpdate Price: ")
                    print("\t7. \tUpdate Quantity: ")
                    print("\t8. \tUpdate Status: ")
                    print("\t9. \tPress any other number to exit")
                    update_ch = int(input('\tEnter your choice (1 to 8): '))
                    if update_ch in range(1, 9):
                        LibFunc.update_book_records(Book_Details, update_ch, bookno)
                else:
                    print('\t', "No record found in the Book_Details Table  having Book No:", bookno)

        elif table_ch == 2:
            if Membership_records.empty:
                print("\t Membership Table is empty , can't update records without entering.")
            else:
                MNo = int(input('\tEnter Member No of member whose record is to be updated'))
                # ['MNo', 'MName', 'Type', 'Security_Amt', 'MDate', 'MStatus'])
                if MNo in Membership_records.index:
                    print("\t1. \tUpdate Member Number: ")
                    print("\t2. \tUpdate Member Name: ")
                    print("\t3. \tUpdate Member Type: ")
                    print("\t4. \tUpdate Security Amount: ")
                    print("\t5. \tUpdate Date of Membership: ")
                    print("\t6. \tDeactivate Library Membership ")
                    print("\t7. \tReactivate Library Membership ")
                    print("\t8. \tPress any other no to exit")
                    update_ch = int(input('\tEnter your choice (1 to 7): '))
                    if update_ch in range(1, 8):
                        LibFunc.update_member_details(Membership_records, update_ch, MNo)

                else:
                    print('\t', "No record found in the Membership Table having Member No ", MNo)

        print('-' * 200)
    elif ch == 3:
        print('\t1. Delete Book_Details Table records ')
        print('\t2. Delete Issue Table records ')
        print("\t3. Press any other number to exit")
        del_ch = int(input("\tEnter your choice 1 to 2: "))
        if del_ch == 1:
            if Book_Details.empty:
                print("\tBook_Details Table is empty , can't delete records without entering.")

            else:
                bookno = int(input('\tEnter Book No of the book whose record is to be deleted: '))
                if bookno in Book_Details.index:
                    if bookno in Issue_records["BookNo"].values:
                        LibFunc.delete_book_records(Book_Details, bookno, Issue_records)

                    else:
                        LibFunc.delete_book_records(Book_Details, bookno)

                else:
                    print('\t', "No record found in the Book Details Table having Book No: ", bookno)
        elif del_ch == 2:
            if Issue_records.empty:
                print("\tIssue Table is empty , can't delete records without entering.")

            else:
                IssId = int(input('\tEnter Issue Id of the book whose record is to be deleted: '))
                if IssId in Issue_records.index:
                    LibFunc.delete_iss_records(Issue_records, Book_Details, IssId)
                else:
                    print('\t', "No record found  in the Issue Table having Issue Id:", IssId)
        print("-" * 200)

    elif ch == 4:
        print('\t1. View Book_Details Table')
        print('\t2. View Issue Table')
        print('\t3. View Membership Table')
        print("\t4. Press any other number to exit")
        disp_ch = int(input('\tEnter your choice (1 to 3): '))
        print('-' * 200)
        if disp_ch == 1:
            LibFunc.display(Book_Details)
        elif disp_ch == 2:
            LibFunc.display(Issue_records)
        elif disp_ch == 3:
            LibFunc.display(Membership_records)
        print('-' * 200)
    elif ch == 5:
        if Book_Details.empty:
            print("\tBook Details Table is Empty, can't display Statistics")
        else:

            print('\t1. View Pie Chart')
            print('\t2. View Histogram')
            print("\t3. Press any other number to exit")
            stat_ch = int(input('\tEnter your choice (1 to 4): '))
            if stat_ch == 1:
                LibFunc.display_pie(Book_Details)
            elif stat_ch == 2:
                LibFunc.display_hist(Book_Details)

        print('-' * 200)
    elif ch==6:
        print('\t1. Search Book_Details Table')
        print('\t2. Search Issue Table')
        print('\t3. Search Membership Table')
        print("\t4. Enter any other number to exit")
        seach_ch = int(input('\tEnter your choice (1 to 3): '))
        res = None
        print('-' * 200)
        if seach_ch == 1:
            val = input('\tEnter value to be searched in the table: ')
            res=LibFunc.search_record(Book_Details,val)
        elif seach_ch==2:
            val = input('\tEnter value to be searched in the table: ')
            res=LibFunc.search_record(Issue_records,val)
        elif seach_ch==3:
            val = input('\tEnter value to be searched in the table: ')
            res = LibFunc.search_record(Membership_records,val)
        else:
            pass
        if res is None:
            print('\tNo matching record found!')
        else:
            print(res)
        print('-'*200)

    elif ch == 7:
        break
    else:
        print("\tIncorrect choice!")
    print('-' * 200)

Book_Details.to_csv(path_bd, index_label="BookNo")
Issue_records.to_csv(path_iss, index_label="IssId")
Membership_records.to_csv(pathm, index_label="MNo")
