import csv

def convert_csv(filename):
    with open(filename+'.csv', "rt", encoding='utf-8') as f:
        reader = csv.reader(f)
        output_file = open(filename+'.txt', 'wb')
        next(reader, None)

        for row in reader:
            row_str = row[1]
            output_file.write(row_str.encode('utf-8'))

        output_file.close()

def convert_files():
    convert_csv('posts')
    convert_csv('comments')