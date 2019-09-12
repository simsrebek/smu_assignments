#SMU Boot Camp
#Rebekah Vinson
#PyBank
#09_11_2019 



#Create dependencies - import csv and os
import csv
import os


#Create lists to store data
dates = []
profit = []


#Define OS Path //Updated OS path as it was tesed against a copy of budgt_data_csv: budget_data_1.csv. Will push both datasets.
Budget_data_2 = os.path.join("/Users/Bek/Resources/Results","budget_data.csv")


#Open file and skip header
with open(Budget_data_2,'r') as Budget_data_2:
     csvreader = csv.reader(Budget_data_2)
     csv_header = next(csvreader)


#Read each row
     for row in csvreader:
       #dates and profit lists are used in greatest increase/decrease change in profit
       dates.append(row[0])
       profit.append(row[1])

                       
#Find number of months in data set
total_of_months = len(dates)


#Find sum of profit
total_profit = 0
p = 0
for p in range(total_of_months):
  total_profit = total_profit + int(profit[p])

  
#Find change in profit per month
monthly_prof_chng = []
c = 0
m = 0
for c in range (0, total_of_months):
  if c == 0:
    monthly_prof_chng.append(0)
  else: 
    monthly_prof_chng.append(int(profit[c])-int(profit[m]))
    m = m+1 

    
#Find average change in monthly profit
sum_monthly_prof_chng = 0
s = 0 
for s in range(total_of_months):
  sum_monthly_prof_chng = sum_monthly_prof_chng + int(monthly_prof_chng[s])
average_monthly_prof_chng = int(sum_monthly_prof_chng)/int(total_of_months - 1)


#Find max profit change
max_profit_change = max(monthly_prof_chng)
max_index = monthly_prof_chng.index(max_profit_change)
max_date = dates[max_index]


#Find min profit change
min_profit_change = min(monthly_prof_chng)
min_index = monthly_prof_chng.index(min_profit_change)
min_date = dates[min_index]


# Set variable for output file
output_file = os.path.join("Financial_Analysis.txt")


# Write updated data to text file with new line
with open(output_file, "w", newline='') as txtfile:
    txtfile.write("---------------------\n")
    txtfile.write("Financial Analysis  \n")
    txtfile.write("----------------------\n")
    txtfile.write("Total Months: " + str(total_of_months) + "\n")
    txtfile.write("Total Revenue: $" + str(total_profit) + "\n")
    txtfile.write("Average Change: $" + str(round(average_monthly_prof_chng,2)) + "\n")
    txtfile.write("Greatest Increase in Revenue: " + str(max_date) + " $(" + str(max_profit_change) + ")" "\n")
    txtfile.write("Greatest Decrease in Revenue: " + str(min_date) + " $(" + str(min_profit_change) + ")" "\n")  
  
     
#Print Results to terminal
print("----------------------")    
print("Financial Analysis  ")
print("----------------------")
print("Total Months: " + str(total_of_months))
print("Total Revenue: $" + str(total_profit))
print("Average Change: $" + str(round(average_monthly_prof_chng,2)))
print("Greatest Increase in Revenue: " + str(max_date) + " $(" + str(max_profit_change) +")")
print("Greatest Decrease in Revenue: " + str(min_date) + " $(" + str(min_profit_change) +")")

