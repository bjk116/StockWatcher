import db
import data
import subprocess
import enotification
# TO DO: Make ALARM_TYPES and NOTIFICATION_TYPES be populated by db of same tablenames
# TO DO: Add columns to ALARM TYPES that say PW_gt/PW_lt are of type PriceWatch and the others are of time differential type
# PW stands for Price Watch, gt is greater than, lt is less than
# inc_gt_x_over_t means increase greater than supplied x value over timespan
# hopefully you can tell what dec_gt_x_over_t stands of
ALARM_TYPES = ['PW_gt', 'PW_lt', 'inc_gt_x_over_t', 'dec_gt_x_over_t']
NOTIFICATION_TYPES = ['Laptop', 'SMS', 'Email']

class Alarm():
    """
    An alarm that is attached tto certain ticker conditions.
    """
    currentPrice = None
    def __init__(self, ticker_id, notification_type, alarm_type, price=None, differential=None):
        """
        Args: 
            ticker: str, like ETH.X or ACB or SPY, but self.ticker becomes the id of the ticker in the db
            alarm type: str - do we just want to check for a certain price to be hit or a increaes/decrease over time
            notification_type: str, how do we want to be notified when conditions are met?
            price: float - use for PW_gt or PW_lt alarm as trigger///
            increase: float, represented as a percent.  so 1.0 represents 1.0% increase
        """
        self.ticker_id, self.ticker = self.validateTicker(ticker_id)
        self.alarm_type_id, self.alarm_type = self.validateAlarmType(alarm_type)
        self.notification_type_id, self.notification_type = self.validateNotificationType(notification_type)
        # Mutual exclusion - price watch or differential watch only
        if price is not None:
            self.price = self.validatePrice(price)
            self.differential = None
        elif differential is not None:
            self.differential = self.validatedifferential(differential)
            self.price = None
        print(str(self.alarm_type_id), str(self.alarm_type))

    def validateTicker(self, ticker_id):
        # Does the ticker exist in our db?
        # This check makes some sense, we wont be keeping price records of tickers i don't want to follow
        # TODO this just reminded me - make prices foreign key on tickers make it such that the prices get deleted when the ticker is deleted on delete cascade i think
        ticker_data = db.runQuery(f"SELECT id, symbol FROM ticker WHERE id = {ticker_id}")
        try:
            return ticker_data[0]
        except IndexError as e:
            raise ValueError(f"Ticker id: {ticker_id} cannot be found in the database.  Please use a ticker that exists.")

    def validateAlarmType(self, alarm_type):
        # Not sure how I feel about this check, if its necessary, though it feels like it does.
        # Only nice thing to take away - I like the pythonic-ness of this code. at least i think its pythonic
        alarm_type_data = db.runQuery(f"SELECT id, alarm_type from alarm_types WHERE id = {alarm_type}")
        try:
            return alarm_type_data[0]
        except IndexError as e:
            raise ValueError(f"Alarm type is database has not been implemented ... yet.")

    def validateNotificationType(self, notification_type):
        notification_type_data = db.runQuery(f"SELECT id, notification_type from notification_types WHERE id = {notification_type}")
        try:
            return notification_type_data[0]
        except IndexError as e:
            raise ValueError(f"Notification type is not supported.")

    def validatePrice(self, price):
        if self.alarm_type in ALARM_TYPES[:2]:
            return price
#        raise ValueError(f"The alarm type {self.alarm_type} does not support price argument")
    
    def validatedifferential(self, differential):
        if self.alarm_type in ALARM_TYPES[2:]:
            return differential
#        raise ValueError(f"The alarm type {self.alarm_type} does not support increase argument")

    def save(self):
        """
        #TODO this seems inappropriate here, should perhaps be outside the class? Not sure.
        Saves the current alarm configuration to the database
        """
        alarm_type_id = ALARM_TYPES.index(self.alarm_type) + 1
        notification_type_id = NOTIFICATION_TYPES.index(self.notification_type) + 1
        ticker_id = self.ticker
        # TO DO: This works for now, but we should really have a db.runPrepUpdate that knows how to handle None's as nulls, datetimes, etc
        price = 'NULL' if self.price is None else self.price
        differential = 'NULL' if self.differential is None else self.price
        query = f"INSERT INTO alarms (fk_ticker_id, fk_notification_type_id, fk_alarm_type_id, price, differential) VALUES ({ticker_id}, {notification_type_id}, {alarm_type_id}, {price}, {differential})"
        print(query)
        db.runUpdateQuery(query)

    def notifyLaptop(self, message):
        print("Attempting to notify via laptop")
        subprocess.call(['notify-send', message['title'], message['subtitle']])


    def notifySMS(self, message):
        pass
    
    def notifyEmail(self, message):
        print(f"Sending an email with {message}")
    #    enotification.sendEmail(message)

    def notify(self, message):
        # TODO I think Notification should probably be its own object
        # Make a message, should be able to do it based on alarm_type and price or differential.
        # then, using same method as in checkConditions, use a dict of functions to dispatch the method in the preferred manner
        # But ultimately, this may called based on log alarms.
        mapping = {
            'Laptop':self.notifyLaptop, 
            'SMS':self.notifyEmail, 
            'Email':self.notifyEmail
        }
        try:
            self.notifyLaptop(message)
            self.notifyEmail(message)
#            mapping[self.notification_type](message)
        except Exception as e:
            print("Something happened during notification")
            print(str(e))

    def alarmActive(self):
        """
        Abstract method, needs to be implemented by the sublass
        Return:
            bool, true if alarm is on, false if it is not
        """
        pass

    def saveToDB(self):
        print(f"INSERT INTO alarm_events ()")
    
    def checkStatus(self):
        if self.alarmActive():
            # save to  alarm event
            self.saveToDB()

    def __str__(self):
        return f"Alarm of {self.alarm_type} notify by {self.notification_type} for {self.ticker} with price {self.price} or differential {self.differential}"

class LessThanAlarm(Alarm):
    alarm_id = 2
    def alarmActive(self):
        self.currentPrice = data.getCurrentPrice(self.ticker_id)
        return self.currentPrice <= self.price
            # message = {
            #     "title":f"Price of {self.ticker} is below {self.price}!",
            #     "subtitle": f"Current price is {self.currentPrice}"
            # }
    
    def afterActive(self):
        pass

class GreaterThanAlarm(Alarm):
    alarm_id = 1
    def alarmActive(self):
        self.currentPrice = data.getCurrentPrice(self.ticker_id)
        return self.currentPrice >= self.price
            # message = {
            #     "title":f"Price of {self.ticker} is above {self.price}!",
            #     "subtitle": f"Current price is {round(self.currentPrice,2)}"
            # }
            # self.notify(message)
    
    def afterActive(self):
        pass


def loadAlarms():
    """
    Loads alarm from database - perhaps this should be outside the class? 
    To do - figure out this part and the right scope
    # TODO Refactor so that malformed db entries don't ruin the entire thing, just get skipped and logged
    """
    alarms = db.runQuery("SELECT fk_ticker_id, fk_notification_type_id, fk_alarm_type_id, price, differential FROM alarms")
    print(alarms)
    return [LessThanAlarm(1, 2, 1, price=4100), GreaterThanAlarm(1, 1, 1, price=4000)]
 #   return [Alarm(ticker, notification_type_id, alarm_type_id, price=price, differential=differential) for (ticker, notification_type_id, alarm_type_id, price, differential) in alarms]

def runAlarms():
    # TODO just occured to me here the foreign key constriant shoudl be if the ticker id is deleted, the alarm should be deleted.
    # Or perhaps the alarm should have a column "deleted" that turns true.  Could be done as a trigger on the ticker table.    
    alarms = loadAlarms()
    for alarm in alarms:
        print(alarm)
        alarm.checkStatus()

if __name__ == "__main__":
    runAlarms()