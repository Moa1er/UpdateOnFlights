import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import datetime
import time

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Analyse_Heures_DOT").get_worksheet(1)

# Determine the number of days in a months
def nbDaysInMonth(year, month):
      leap = 0
      if year% 400 == 0:
         leap = 1
      elif year % 100 == 0:
         leap = 0
      elif year% 4 == 0:
         leap = 1
      if month==2:
         return 28 + leap
      list = [1,3,5,7,8,10,12]
      if month in list:
         return 31
      return 30

lastNbHoursPerMonth = 0

for boucleDateColonne in range(1):
    #for boucleDatePourLigne in range(3, 4):
    for boucleDatePourLigne in range(6):
        
        date1 = sheet.cell(3 + boucleDateColonne, 4 + boucleDatePourLigne).value
        date2 = sheet.cell(3 + boucleDateColonne, 5 + boucleDatePourLigne).value
        nbOfDays = 0
        print()
        print(date1, date2)
        # Getting the day, month and year respectivly for both date
        date1_day = int(date1[0:2])
        date1_month = int(date1[3:5])
        date1_year = int(date1[6:10])
        date2_day = int(date2[0:2])
        date2_month = int(date2[3:5])
        date2_year = int(date2[6:10])
        
        # Calcul of the nbOfDays between two dates (VERIFIED)
        if date2_year == date1_year:
            if date2_month == date1_month:
                nbOfDays = date2_day - date1_day
            else:
                for i in range(date2_month - date1_month):
                    nbOfDays += nbDaysInMonth(date1_year, date1_month + i)
                nbOfDays += (date2_day - date1_day)
        else:
            for i in range((date2_year-date1_year)*12 + date2_month - date1_month):
                if date1_month + i > 12:
                    # We change the year and so we sub 12 to the actuel month (date1_month + i)
                    nbOfDays += nbDaysInMonth(date2_year, date1_month + i - 12)
                else:
                    nbOfDays += nbDaysInMonth(date1_year, date1_month + i)
            nbOfDays += (date2_day - date1_day)

        #print ("NombreJoursPeriode", nbOfDays)
        # From where can we write data
        startingPlaceToWriteData = 18;
        # 24 means 2 years (that's how the sheet is made)
        for i in range (24):
            date = sheet.cell(2, startingPlaceToWriteData + i).value
            if (int(date[3:5]) == date1_month and int(date[6:10]) == date1_year):
                startingPlaceToWriteData += i
                break
            elif i == 23:
                sheet.update_cell(1, startingPlaceToWriteData, "erreur")
                print("Oupsi")
        
        # Part to calcul the nomber of hours per week/month
        nbHoursPerWeek = 0
        nbHoursPerMonth = 0
    
        #Getting the nbHoursForOnePeriod
        # 8 means that we jump gfrom "Phases" to "Heures Par Phases"
        nbHoursForOnePeriod = int(float(sheet.cell(3 + boucleDateColonne, 4 + boucleDatePourLigne + 8).value))
        
        # Calcul of the nbHoursPerDay (average)
        nbHoursPerDay = nbHoursForOnePeriod/nbOfDays    
        print("nbHoursPerDayMOYEN", nbHoursPerDay)
        # Calcul of the nbHoursPerWeek (average)
        nbHoursPerWeek = nbHoursPerDay * 7
        
        # Test to know if the totalForOnePeriode is equal to nbHoursForOnePeriod that we get from our data
        totalForOnePeriode = 0
        
        #There are a lot of decimal so we count them here
        restDecimal = 0
        
        # Calcul of the nbHoursPerMonth (presise per month)
        # first month
        nbHoursPerMonth = lastNbHoursPerMonth + (nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month) - date1_day + 1))
        sheet.update_cell(3 + boucleDateColonne, startingPlaceToWriteData, int(nbHoursPerMonth))
        
        restDecimal += nbHoursPerMonth - int(nbHoursPerMonth)
        #print("RESTEEEEEEEEE 111", restDecimal)
        print("NbHeures1er", nbHoursPerMonth)
        totalForOnePeriode += int(nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month) - date1_day + 1))
        
        #print("firstMonth : ", nbHoursPerMonth)
        # Months in the middle that are full
        #if date1_year == date2_year:
        #for j in range(1, date2_month - date1_month):
        for j in range(1, (12 - date1_month + date2_month) % 12):
            nbHoursPerMonth = (nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month + j)))
            sheet.update_cell(3 + boucleDateColonne, startingPlaceToWriteData + j, int(nbHoursPerMonth))
            totalForOnePeriode += int(nbHoursPerMonth)
            #print("RESTEEEEEEEEE INN", restDecimal)
            restDecimal += nbHoursPerMonth - int(nbHoursPerMonth)
            print("monthInTheMiddle : ", nbHoursPerMonth)
            
        
        # last month
        nbHoursPerMonth = (nbHoursPerDay * (date2_day - 1))
        lastNbHoursPerMonth = (nbHoursPerDay * (date2_day - 1)) + restDecimal
        
        restDecimal += nbHoursPerMonth - int(nbHoursPerMonth)
        #print("RESTEEEEEEEEE FINALL", restDecimal)
        sheet.update_cell(3 + boucleDateColonne, startingPlaceToWriteData + (abs(date2_month - date1_month)), int(nbHoursPerMonth + restDecimal))
        totalForOnePeriode += int(nbHoursPerMonth + restDecimal)
        print("lastMonth : ", nbHoursPerMonth)
        print("date_heuresPourUnePeriode", nbHoursForOnePeriod)
        print("totaleUnePeriode : ", totalForOnePeriode)
    #time.sleep(100)
