import csv
import sys


def main():

    # TODO: Check for command-line usage
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    filename_database = sys.argv[1]
    database = []
    with open(filename_database) as f:
        reader = csv.DictReader(f)
        for row in reader:
            database.append(row)
        fieldnames = reader.fieldnames
    fieldnames.remove("name")

    # TODO: Read DNA sequence file into a variable
    filename_sequence = sys.argv[2]
    sequence = []
    with open(filename_sequence) as f:
        reader = csv.reader(f)
        for str in reader:
            sequence.append(str)

    # TODO: Find longest match of each STR in DNA sequence
    # Create a dictionary with key-value pairs for saving the counts
    person = {}
    # Loop for going throught every STR and find the longest STR count
    for str in fieldnames:
        person[str] = longest_match(sequence[0][0], str)

    # TODO: Check database for matching profiles
    # Loop for going through every person of the database
    for row in database:
        n = 0
        for str in row.items():
            if str[0] == 'name':
                continue
            elif person[str[0]] == int(str[1]):
                n += 1
                if n == len(person):
                    print(row['name'])
                    sys.exit(0)
                continue
            else:
                break
    print("No match")
    sys.exit(1)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
