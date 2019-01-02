import shelve

class User:
    def __init__(self):
        self.problem = ''
        self.description = ''
        self.location = ''
        self.date = ''
        self.status = 'pending'


    def get_problem(self):
        return self.problem

    def get_description(self):
        return self.description

    def get_location(self):
        return self.location

    def get_date(self):
        return self.date

    def get_status(self):
        return self.status

    def create_request(problem, description, location,date):
        problems = shelve.open('problems')
        p = User()
        p.problem = problem
        p.description = description
        p.location = location
        p.date = date
        problems[problem] = p