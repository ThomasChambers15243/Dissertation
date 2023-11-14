# def TEST(s):
#
#     mapping = {')': '(', '}': '{', ']': '['}
#     stack = []
#     for char in s:
#         if char in mapping:
#             if not stack or stack[-1] != mapping[char]:
#                 return False
#             stack.pop()
#         else:
#             stack.append(char)
#
#     return len(stack) == 0
import csv
import json
import datetime

def payPalCalc(name):

    with open("Download.CSV") as cFile:
        cReader = csv.DictReader(cFile, delimiter=',')
        total: float =0
        paymentRecord = {}
        for row in cReader:
            if row["Name"] == "Emmanuel Okonkwo":
                day = row['ï»¿"Date"'][0:2]
                mounth = row['ï»¿"Date"'][3:5]
                year = row['ï»¿"Date"'][6:]
                if (int(year) < 2023 ):
                    total+=float(row["Gross"])
                    paymentRecord[row["Transaction ID"]] = {
                        "Date" : row['ï»¿"Date"'],
                        "Time": row["Time"],
                        "Type": row["Type"],
                        "From Email Address": row["From Email Address"],
                        "Amount": row["Gross"]
                    }
                    print(paymentRecord[row["Transaction ID"]])
                elif (int(mounth) < 4):
                    total+=float(row["Gross"])
                    paymentRecord[row["Transaction ID"]] = {
                        "Date" : row['ï»¿"Date"'],
                        "Time": row["Time"],
                        "Type": row["Type"],
                        "From Email Address": row["From Email Address"],
                        "Amount": row["Gross"]
                    }
                    print(paymentRecord[row["Transaction ID"]])
                elif (int(day) <= 5 and int(mounth) < 4):
                    total+=float(row["Gross"])
                    paymentRecord[row["Transaction ID"]] = {
                        "Date" : row['ï»¿"Date"'],
                        "Time": row["Time"],
                        "Type": row["Type"],
                        "From Email Address": row["From Email Address"],
                        "Amount": row["Gross"]
                    }
                    print(paymentRecord[row["Transaction ID"]])
        #with open()
        print(total)
        title = "TriconeXPaypalDate_ForTaxYear_6thApril_22--5thApril_23" + str(datetime.date.today())
        '''
        with open(title, 'w') as fp:
            json.dump(paymentRecord, fp)
        '''
        #for key,value in paymentRecord.items():
            #print(value)

    InterestPayments = []

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    payPalCalc('PyCharm')