import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import datetime
import time

# Basic setup to access the google sheet
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

# Init of some variables (data starts at ligne 3)
ligne = 3
boucleDateLigne = 3

# While there isn't any empty ligne
while(sheet.cell(ligne, 1).value != ""):
    # print("boucleDateLigne", boucleDateLigne)
    # print("ligne", ligne)
    
    #If there is a ligne, look if checked true
    if sheet.cell(ligne, 1).value == "TRUE":
        
        # Reinitilisation of the lastNbHoursPerMonth when we change the ligne
        lastNbHoursPerMonth = 0
        for boucleDateColonne in range(6):
            
            # 4 and 5 bc pre-defined place of the date in the array
            date1 = sheet.cell(boucleDateLigne, 4 + boucleDateColonne).value
            date2 = sheet.cell(boucleDateLigne, 5 + boucleDateColonne).value
            nbOfDays = 0
            # print()
            # print(date1, date2)
            
            # Getting the day, month and year respectivly for both dates
            date1_day = int(date1[0:2])
            date1_month = int(date1[3:5])
            date1_year = int(date1[6:10])
            date2_day = int(date2[0:2])
            date2_month = int(date2[3:5])
            date2_year = int(date2[6:10])
            
            # Calcul of the nbOfDays between two dates
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

            # print ("NombreJoursPeriode", nbOfDays)
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
                    print("Please Update the size of your calendar")
            
            # Part to calcul the nomber of hours per week/month
            nbHoursPerWeek = 0
            nbHoursPerMonth = 0
        
            #Getting the nbHoursForOnePeriod
            # 8 means that we jump gfrom "Phases" to "Heures Par Phases"
            nbHoursForOnePeriod = int(float(sheet.cell(boucleDateLigne, 4 + boucleDateColonne + 8).value))
            # print("nbHoursForOnePeriod", nbHoursForOnePeriod)
            
            # Calcul of the nbHoursPerDay (average)
            nbHoursPerDay = nbHoursForOnePeriod / nbOfDays    
            # print("nbHoursPerDayMOYEN", nbHoursPerDay)
            
            # Calcul of the nbHoursPerWeek (average)
            nbHoursPerWeek = nbHoursPerDay * 7
            
            # Test to know if the totalForOnePeriode is equal to nbHoursForOnePeriod that we get from our data
            totalForOnePeriode = 0
            
            #There are a lot of decimal so we count them here
            restDecimal = 0
            
            # Calcul of the nbHoursPerMonth (presise per month)
            # first month
            # if else bc if there is only one month, we want to stop here
            # print("Donnée du dernier mois: ", lastNbHoursPerMonth)
            if(date1_month == date2_month and date1_year == date2_year):
                nbHoursPerMonth = int(lastNbHoursPerMonth + nbHoursPerDay * nbOfDays)
                restDecimal += (lastNbHoursPerMonth + nbHoursPerDay * nbOfDays) - int(nbHoursPerMonth)
                nbHoursPerMonth += round(restDecimal)
                sheet.update_cell(boucleDateLigne, startingPlaceToWriteData, nbHoursPerMonth)
                lastNbHoursPerMonth += nbHoursPerMonth
                
            else:
                nbHoursPerMonth = int(lastNbHoursPerMonth + nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month) - date1_day + 1))
                sheet.update_cell(boucleDateLigne, startingPlaceToWriteData, int(nbHoursPerMonth))
            
                restDecimal += lastNbHoursPerMonth + (nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month) - date1_day + 1)) - int(nbHoursPerMonth)
                totalForOnePeriode += int(nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month) - date1_day + 1))
                # print()
                # print("NbHeuresFirstMonth: ", nbHoursPerMonth)
                # print("RestePremierMois: ", restDecimal)
                # print("totaleActuel : ", totalForOnePeriode)
                
                # Months in the middle that are full
                #for j in range(1, date2_month - date1_month):
                for j in range(1, (12 - date1_month + date2_month) % 12):
                    if(date1_month + j > 12):
                        nbHoursPerMonth = int(nbHoursPerDay * (nbDaysInMonth(date2_year, (date1_month + j) % 12)))
                        restDecimal += nbHoursPerDay * (nbDaysInMonth(date2_year, (date1_month + j) % 12)) - int(nbHoursPerMonth)
                    else:
                        nbHoursPerMonth = int(nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month + j)))
                        restDecimal += nbHoursPerDay * (nbDaysInMonth(date1_year, date1_month + j)) - int(nbHoursPerMonth)
                    
                    sheet.update_cell(boucleDateLigne, startingPlaceToWriteData + j, int(nbHoursPerMonth))
                    totalForOnePeriode += int(nbHoursPerMonth)
                    # print()
                    # print("monthInTheMiddle: ", nbHoursPerMonth)
                    # print("ResteMoisMilieu: ", restDecimal)
                    # print("totaleActuel: ", totalForOnePeriode)
                
                # In case the date is 01/xx/xx so that it adds the rest to the value before 
                if int(nbHoursPerDay * (date2_day - 1)) == 0:
                    nbHoursPerMonth += round(restDecimal);
                    sheet.update_cell(boucleDateLigne, startingPlaceToWriteData + ((12 - date1_month + date2_month) % 12 - 1), nbHoursPerMonth)
                    lastNbHoursPerMonth = 0
                    
                # last month
                else:
                    nbHoursPerMonth = int(nbHoursPerDay * (date2_day - 1))
                    restDecimal += nbHoursPerDay * (date2_day - 1) - int(nbHoursPerMonth)
                    nbHoursPerMonth += round(restDecimal);
                
                    sheet.update_cell(boucleDateLigne, startingPlaceToWriteData + ((12 - date1_month + date2_month) % 12), nbHoursPerMonth)
                    lastNbHoursPerMonth = nbHoursPerMonth
                
            totalForOnePeriode += nbHoursPerMonth
            # print()
            # print("lastMonth: ", nbHoursPerMonth - round(restDecimal))
            # print("ResteDernierMois: ", restDecimal)
            # print("date_heuresPourUnePeriode: ", nbHoursForOnePeriod)
            # print("totaleUnePeriode: ", totalForOnePeriode)
        time.sleep(50)
    ligne += 1
    boucleDateLigne += 1
    # print()
    # print()
    # print()
    # print("CHANGEMENT LIGNE")