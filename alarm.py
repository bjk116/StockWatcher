import db

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
    def __init__(self, ticker, alarm_type, notification_type, price=None, differential=None):
        """
        Args: 
            ticker: str, like ETH.X or ACB or SPY, but self.ticker becomes the id of the ticker in the db
            alarm type: str - do we just want to check for a certain price to be hit or a increaes/decrease over time
            notification_type: str, how do we want to be notified when conditions are met?
            price: float - use for PW_gt or PW_lt alarm as trigger///
            increase: float, represented as a percent.  so 1.0 represents 1.0% increase
        """
        self.ticker = self.validateTicker(ticker)
        self.alarm_type = self.validateAlarmType(alarm_type)
        self.notification_type = self.validateNotificationType(notification_type)
        # Mutual exclusion - price watch or differential watch only
        if price is not None:
            self.price = self.validatePrice(price)
            self.differential = None
        elif differential is not None:
            self.differential = self.validatedifferential(differential)
            self.price = None
    
    def validateTicker(self, ticker):
        # Does the ticker exist in our db?
        try:
            ticker_id = db.runScalarQuery(f"SELECT id FROM ticker WHERE symbol = '{ticker}'")
            return ticker_id
        except IndexError as e:
            # We get IndexErrors when we run db.runScalarQuery and get not results - not sure if it would be better to handle on db
            # Side or what.  Perhaps a custom error gets passed back, like NoResultError or something? not sure.
            raise ValueError(f"Ticker {symbol} is setup in our application and therefore we cannot set an alarm on it")

    def validateAlarmType(self, alarm_type):
        if alarm_type not in ALARM_TYPES:
            raise ValueError(f"Selected alarm type {alarm_type} is not supported")
        return alarm_type

    def validateNotificationType(self, notification_type):
        if notification_type not in NOTIFICATION_TYPES:
            raise ValueError(f"{notification_type} is not a supported notification type")
        return notification_type
    
    def validatePrice(self, price):
        if self.alarm_type in ALARM_TYPES[:2]:
            return price
        raise ValueError(f"The alarm type {self.alarm_type} does not support price argument")
    
    def validatedifferential(self, differential):
        if self.alarm_type in ALARM_TYPES[2:]:
            return differential
        raise ValueError(f"The alarm type {self.alarm_type} does not support increase argument")

    def save(self):
        """
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

    def load(self):
        """
        Loads alarm from database - perhaps this should be outside the class? 
        To do - figure out this part and the right scope
        """
        pass

    def notify(self, message):
        pass
    
    def notifyLaptop(self):
        pass
    
    def notifySMS(self):
        pass
    
    def notifyEmail(self):
        pass