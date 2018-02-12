import csv #Python has a nice CSV package that will do the real heavy lifting

# CSV Reader class with one class method that converts a CSV to a 2D list and returns it
# input is the filename(+extension) of the csv to read
# WARNING - don't use this on CSVs that are ridiculously large (like 100s of megabytes or more)
class CsvReader:
    def csv_to_list(name):
        reader = csv.reader(open(name)) #open the CSV file from disk and make a CSV reader object
        out = []
        for row in reader: #loop once over the CSV contents and append each row to list
            out.append(row)
        return out

# CSV Writer class to write information to a CSV and save to disk
class CsvWriter:
    def __init__(self):
        self.name = None
        self.csv = None
        self.num_columns = None
        self.writer = None

    # Open a new CSV file on disk with the given name and write the header as the first row
    def open_csv(self, name, header):
        if self.name != None:
            print('CSV is already open!')
            return
        if type(header) != type([]) or len(header) == 0:
            print('Header must be list of strings!')
            return
        if name[-4:] != '.csv': #if the desired filename doesn't end in '.csv', add it to the name
            name = name + '.csv'
        self.name = name
        self.num_columns = len(header)
        self.csv = open(self.name, 'w') #open a new CSV file on disk
        self.writer = csv.writer(self.csv)
        self.writer.writerow(header) #write header as first row

    # Every time you want to add a row to the CSV you've opened, you can call this method
    def add_row(self, row):
        if self.name == None:
            print('No CSV currently open!')
            return
        if type(row) != type([]) or len(row) != self.num_columns:
            print('Row must be same size as header! Header has ' + str(self.num_columns) + ' columns!')
            return
        self.writer.writerow(row) #write row in CSV

    # Close CSV file once done and reset the CsvWriter class instance for use on the next task
    def close_csv(self):
        if self.name == None:
            print('No CSV currenly open!')
            return
        self.csv.close() #close CSV file on disk
        self.__init__()
        print('CSV closed')
