import datetime

class machine:
    def __init__(self, machine_name='COUNTER'):
        self.__machine_name = machine_name
        self.__lens_per_hour = self.set_hour_dict()


    @property
    def machine_name(self):
        return self.__machine_name


    @machine_name.setter
    def machine_name(self, machine_name):
        self.__machine_name = machine_name


    @property
    def lens_per_hour(self):
        return self.__lens_per_hour


    def define_lens_per_hour(self, hour, amount):
        self.__lens_per_hour[hour] = amount


    def add_lens_per_hour(self, hour, amount):
        self.__lens_per_hour[hour] = self.__lens_per_hour[hour] + int(amount)

    def set_hour_dict(self):
        hour_dict = {}
        for i in range(24):
            hour_dict[f'{i:02d}:00'] = 0
        return hour_dict


class breakage:
    def __init__(self, job, 
                type, 
                job_date, 
                production_date, 
                breakage_date, 
                breakage_resp, 
                client_id, 
                client, 
                client_job, 
                breakage_amount, 
                blank_code, 
                blank_model, 
                base, 
                add, 
                seller, 
                last_cost, 
                breakage_motive, 
                alias, 
                sector):
        self.__job = job
        self.__type = type
        self.__job_date = datetime.datetime.strptime(job_date, '%d/%m/%Y')
        self.__production_date = datetime.datetime.strptime(production_date, '%d/%m/%Y')
        self.__breakage_date = datetime.datetime.strptime(breakage_date, '%d/%m/%Y H%:%m:%s')
        self.__breakage_resp = breakage_resp
        self.__cliend_id = client_id
        self.__client = client
        self.__client_job = client_job
        self.__breakage_amount = breakage_amount
        self.__blank_code = blank_code
        self.__blank_model = blank_model
        self.__base = base
        self.__add = add
        self.__seller = seller
        self.__last_cost = last_cost
        self.__breakage_motive = breakage_motive
        self.__alias = alias
        self.__sector = sector


    @property
    def job(self):
        return self.__job


    @property
    def type(self):
        return self.__type


    @property
    def job_date(self):
        return self.__job_date


    @property
    def production_date(self):
        return self.__production_date


    @property
    def breagage_date(self):
        return self.__breakage_date


    @property
    def breakage_resp(self):
        return self.__breakage_resp


    @property
    def client_id(self):
        return self.__cliend_id


    @property
    def client(self):
        return self.__client


    @property
    def client_job(self):
        return self.__client_job


    @property
    def breakage_amount(self):
        return self.__breakage_amount


    @property
    def blank_code(self):
        return self.__blank_code


    @property
    def blank_model(self):
        return self.__blank_model


    @property
    def base(self):
        return self.__base


    @property
    def add(self):
        return self.__add

    @property
    def seller(self):
        return self.__seller
    

    @property
    def last_cost(self):
        return self.__last_cost


    @property
    def breakage_motive(self):
        return self.__breakage_motive


    @property
    def alias(self):
        return self.__alias


    @property
    def sector(self):
        return self.__sector