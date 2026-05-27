"""
gale_shapley.py

An implementation of the Gale-Shapley algorithm (also known as the Deferred Acceptance
algorithm) for solving the Stable Matching Problem.

This script implements a student-proposing version of the algorithm, matching a list
of 8 students to 8 universities based on their respective preference lists.

Algorithm Overview:
    The Gale-Shapley algorithm guarantees that:
    1. A stable matching is always found.
    2. The matching is student-optimal (since students make the proposals).
    3. The matching is university-pessimal.
    
    A matching is stable if there is no blocking pair (i.e., no student and university
    who would both prefer each other over their current matches).
"""

# Define the sets of participating entities
students = ["Andreas", "Maria", "Giorgos", "Eleni", "Nikos", "Sofia", "Petros", "Anna"]
universities = ["MIT", "Stanford", "Harvard", "Berkeley", "Caltech", "Princeton", "Yale", "Columbia"]

# Student preference lists: Ordered from most preferred (index 0) to least preferred.
# For example, Andreas prefers MIT the most, then Stanford, ..., and Columbia the least.
student_pref = {
    "Andreas": ["MIT", "Stanford", "Harvard", "Berkeley", "Caltech", "Princeton", "Yale", "Columbia"],
    "Maria": ["Harvard", "MIT", "Stanford", "Yale", "Princeton", "Berkeley", "Columbia", "Caltech"],
    "Giorgos": ["Stanford", "Berkeley", "MIT", "Harvard", "Columbia", "Caltech", "Princeton", "Yale"],
    "Eleni": ["Princeton", "Yale", "Harvard", "MIT", "Stanford", "Columbia", "Berkeley", "Caltech"],
    "Nikos": ["Berkeley", "Stanford", "MIT", "Caltech", "Harvard", "Princeton", "Yale", "Columbia"],
    "Sofia": ["Yale", "Harvard", "Princeton", "MIT", "Stanford", "Berkeley", "Columbia", "Caltech"],
    "Petros": ["Columbia", "Caltech", "Berkeley", "Stanford", "MIT", "Harvard", "Princeton", "Yale"],
    "Anna": ["Caltech", "Columbia", "Yale", "Princeton", "Harvard", "MIT", "Stanford", "Berkeley"]
}

# University preference lists: Ordered from most preferred (index 0) to least preferred.
# For example, MIT prefers Andreas the most, then Maria, ..., and Anna the least.
uni_pref = {
    "MIT": ["Andreas", "Maria", "Giorgos", "Sofia", "Nikos", "Eleni", "Petros", "Anna"],
    "Stanford": ["Giorgos", "Andreas", "Maria", "Nikos", "Sofia", "Eleni", "Anna", "Petros"],
    "Harvard": ["Maria", "Sofia", "Eleni", "Andreas", "Giorgos", "Anna", "Nikos", "Petros"],
    "Berkeley": ["Giorgos", "Nikos", "Andreas", "Petros", "Maria", "Sofia", "Eleni", "Anna"],
    "Caltech": ["Anna", "Petros", "Nikos", "Giorgos", "Andreas", "Maria", "Sofia", "Eleni"],
    "Princeton": ["Eleni", "Sofia", "Maria", "Andreas", "Nikos", "Giorgos", "Anna", "Petros"],
    "Yale": ["Sofia", "Maria", "Eleni", "Anna", "Andreas", "Giorgos", "Nikos", "Petros"],
    "Columbia": ["Petros", "Anna", "Maria", "Giorgos", "Sofia", "Andreas", "Nikos", "Eleni"]
}

def print_preferences():
    """
    Prints the preference tables for both students and universities in a readable format.
    """
    print("STUDENTS' PREFERENCES")
    for student in students:
        print(student, ":", student_pref[student])
    
    print("\nUNIVERSITIES' PREFERENCES")
    for university in universities:
        print(university, ":", uni_pref[university])
    print()

def prefers_new_student(university, new_student, current_student):
    """
    Determines whether a university prefers a new proposing student over its current matched student.
    
    Parameters:
        university (str): The university performing the comparison.
        new_student (str): The student proposing to the university.
        current_student (str): The student currently matched with the university.
        
    Returns:
        bool: True if the university prefers new_student over current_student, False otherwise.
              Lower index in the preference list means higher preference.
    """
    pref_list = uni_pref[university]
    # In python list.index(x) returns the position of x. 
    # A smaller index indicates a higher position/preference on the university's list.
    return pref_list.index(new_student) < pref_list.index(current_student)

def print_matches(matches):
    """
    Prints the current state of matches between universities and students.
    
    Parameters:
        matches (dict): A dictionary mapping universities to their currently matched students.
    """
    print("Current matches:")
    for university in matches:
        print(university, "-", matches[university])
    print()

def gale_shapley():
    """
    Executes the Gale-Shapley algorithm to find a stable matching between students and universities.
    
    The algorithm operates as follows:
    1. Initialize all students as free.
    2. While there is at least one free student who hasn't proposed to all universities:
       a. The student proposes to their highest-ranked university to which they haven't proposed yet.
       b. If the university is free, it accepts the proposal (forming a tentative match).
       c. If the university is already matched:
          i. It compares the proposing student with its current partner.
          ii. If it prefers the new student, it accepts them and rejects the current partner.
              The rejected partner becomes free again.
          iii. If it prefers the current partner, it rejects the new student. The new student remains free.
    3. The algorithm terminates when all students are matched or have exhausted their preference lists.
    """
    # Create a queue of students who are currently unmatched/free
    free_students = students.copy()
    
    # Dictionary to keep track of matched pairs: {university: student}
    matches = {}
    
    # Dictionary to keep track of the next university index a student should propose to.
    # next_choice[student] represents the index in student_pref[student] of the next university to propose to.
    next_choice = {}
    for student in students:
        next_choice[student] = 0
        
    step = 1
    rejections = 0
    
    # Continue proposing as long as there is a free student who has not proposed to all universities.
    while len(free_students) > 0:
        # Get the first free student from our list/queue
        student = free_students[0]
        
        # Determine the next university on this student's preference list
        university = student_pref[student][next_choice[student]]
        # Increment the counter for this student so they propose to their next choice next time if rejected
        next_choice[student] += 1
        
        print("Step", step)
        print(student, "proposes to", university)
        
        # Case 1: The university is currently free / unmatched
        if university not in matches:
            # The university accepts the proposal tentatively
            matches[university] = student
            # The student is no longer free, so remove them from the free students queue
            free_students.pop(0)
            print(university, "accepts", student)
            
        # Case 2: The university is already matched to another student
        else:
            current_student = matches[university]
            
            # Check if the university prefers the new student over its current match
            if prefers_new_student(university, student, current_student):
                # The university accepts the new student
                matches[university] = student
                # The new student is no longer free
                free_students.pop(0)
                # The previously matched student is now rejected and becomes free again
                free_students.append(current_student)
                rejections += 1
                print(university, "accepts", student)
                print(current_student, "is rejected")
            else:
                # The university rejects the proposing student; they remain in the free list (at the front)
                # and will propose to their next preference in the next iteration.
                rejections += 1
                print(university, "rejects", student)
                
        # Output current matching state for tracing purposes
        print_matches(matches)
        step += 1
        
    # Print the final output summarizing the results
    print("FINAL STABLE MATCHING")
    for student in students:
        for university in matches:
            if matches[university] == student:
                print(student, "-", university)
                
    # Check if every student and university has been matched
    if len(matches) == len(students):
        print("Perfect Matching: Yes")
    else:
        print("Perfect Matching: No")
        
    print("Total Rejections:", rejections)

if __name__ == "__main__":
    # Print initial setup configuration
    print_preferences()
    # Execute the algorithm
    gale_shapley()
