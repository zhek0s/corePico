# Python3 program for the above approach

# Unix time is in seconds and
# Humar Readable Format:
# DATE:MONTH:YEAR:HOUR:MINUTES:SECONDS,
# Start of unix time:01 Jan 1970, 00:00:00

# Function to convert unix time to
# Human readable format

class Date:
    def unixTimeToHumanReadable(seconds):

        # Save the time in Human
        # readable format
        ans = ""

        # Number of days in month
        # in normal year
        daysOfMonth = [31, 28, 31, 30, 31, 30,
                       31, 31, 30, 31, 30, 31]

        (currYear, daysTillNow, extraTime,
         extraDays, index, date, month, hours,
         minutes, secondss, flag) = (0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0)

        # Calculate total days unix time T
        daysTillNow = seconds // (24 * 60 * 60)
        extraTime = seconds % (24 * 60 * 60)
        currYear = 1970

        # Calculating current year
        while (daysTillNow >= 365):
            if (currYear % 400 == 0 or
                (currYear % 4 == 0 and
                    currYear % 100 != 0)):
              if daysTillNow < 366:
                break
              daysTillNow -= 366
            else:
                daysTillNow -= 365
            currYear += 1

        # Updating extradays because it
        # will give days till previous day
        # and we have include current day
        extraDays = daysTillNow + 1

        if (currYear % 400 == 0 or
            (currYear % 4 == 0 and
                currYear % 100 != 0)):
            flag = 1

        # Calculating MONTH and DATE
        month = 0
        index = 0

        if (flag == 1):
            while (True):

                if (index == 1):
                    if (extraDays - 29 < 0):
                        break

                    month += 1
                    extraDays -= 29

                else:
                    if (extraDays - daysOfMonth[index] < 0):
                        break

                    month += 1
                    extraDays -= daysOfMonth[index]

                index += 1

        else:
            while (True):
                if (extraDays - daysOfMonth[index] < 0):
                    break

                month += 1
                extraDays -= daysOfMonth[index]
                index += 1

        # Current Month
        if (extraDays > 0):
            month += 1
            date = extraDays

        else:
            if (month == 2 and flag == 1):
                date = 29
            else:
                date = daysOfMonth[month - 1]

        # Calculating HH:MM:YYYY
        hours = extraTime // 3600
        minutes = (extraTime % 3600) // 60
        secondss = (extraTime % 3600) % 60

        #ans += str(date)
        #ans += "/"
        #ans += str(month)
        #ans += "/"
        #ans += str(currYear)
        #ans += " "
        #ans += str(hours)
        #ans += ":"
        #ans += str(minutes)
        #ans += ":"
        #ans += str(secondss)
        ans={"year":currYear,"month":month,"day":date,"hour":hours,"minute":minutes,"seconds":secondss}
        
        # Return the time
        return ans
    
    def convertMonthToValue(month):
        table={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
        return table[month]
    
    def unixTimeToValParcer(time):
        dat=time.split(":")
        return dat[0],dat[1]
    
    def biggerDate(dat,datL):
        if(int(dat["year"])<int(datL["year"])):
            return False
            if(int(dat["month"])<int(datL["month"])):
                return False
            else:
                if(int(dat["date"])<int(datL["date"])):
                    return False
                else:
                    if(int(dat["hour"])<int(datL["hour"])):
                        return False
                    else:
                        if(int(dat["minute"])<=int(datL["minute"])):
                            return False
                        else:
                            return True
    
    def niceDateFromDat(dat):
        ans="Time: "
        ans += str(dat["year"])
        ans += "/"
        ans += str(dat["month"])
        ans += "/"
        ans += str(dat["date"])
        ans += " "
        ans += str(dat["hour"])
        ans += ":"
        ans += str(dat["minute"])
        return ans
    
# Driver code
if __name__ == "__main__":

    # Given unix time
    T = 1683807671

    # Function call to convert unix
    # time to human read able
    ans = unixTimeToHumanReadable(T)

    # Print time in format
    # DD:MM:YYYY:HH:MM:SS
    print(ans)