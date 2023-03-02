
#Name: Haitian Zhou
#ID#: 83281491

def load_resume(file):
    """
    Read the file and return it as a list based on lines in the file.
    """
    #open file in the read only mode and get the context
    with open(file, 'r') as my_file:
        content = []
        for line in my_file:
            line = line.strip()
            content.append(line)
    return content

def detect_name(line):
    """
    Detect the name on the first line of the file and return it, if it is invalid(first letter should be in upper case), return Invalid Name.
    The function takes one parameter as the first line of the file.
    """
    name = 'Invalid Name'

    #if the first letter of the name is not upper case, consider it as an invalid name
    if line[0].isupper(): 
        name = line

    return name
    

def detect_email(text):
    """
    Detect and return the email address by looking for a line that has the @ character.  
    A valid email should follow rules that:
        1. last four characters of the email need to be either '.com' or '.edu'. 
        2. The email contains a lowercase English character after the @. 
        3.There should be no digits or numbers in the email address.  
    if an email if invalid, consider it as missing
    """

    #find email from text and remove '\n'
    email = ''      
    for line in text:
        if '@' in line or '.at.' in line:
            email = line[:-1] 

     # if no '@' or '.at.' found, return missing 
    if email == '': 
        return ''
    
    for i in range(len(email)):
         #no numbers allows in a valid email
        if email[i].isnumeric():
            return '' 

        #if no lower case character after @, return missing
        elif (email[i] == '@' or email[i] == '.at.') and not email[i + 1].islower():
            return ''  
    return email
        

def detect_course(text):
    """
    Detect and return the courses as a list by looking for the word “Courses” in the  list and then extract the line that contains that word.  
    """
    courses = []
    for line in text:
        if "Courses" in line:
            courses = line.split(',')
    for i in range(len(courses)):
        if i == 0:
            #remove Courses: in the first element
            course = courses[0].split(':') 

            #remove non alphabet chr 
            for j in range(len(course[1])):
                if course[1][j].isalpha(): 
                    courses[0] = course[1][j:] 
                    break

        #remove '\n' at the end of line
        elif i == len(courses) - 1:
            courses[i] = courses[i][:-1] 

        #strip the leading and ending white space 
        courses[i] = courses[i].strip() 
    return courses


def detect_project(text):
    """
    Detect and return the projects as a list by looking for the word “Projects” in the list until hit a line that contains '----------'.
    """
    #find the start and the end position of project
    for i in range(len(text)):
        if 'Projects' in text[i]:
            start = i + 1
        if '------' in text[i]:
            end = i

    #if valid, return project, else return missing 
    return text[start:end] if start < end else [] 
    


def surround_block(tag, text):
    """
    Surrounds the given text with the given html tag and returns the string.
    """
    
    #format of <P>xxx</p>
    return '<' + tag + '>' + text + '</' + tag + '>'


def create_email_link(email_address):
    """
    Creates an email link with the given email_address.
    To cut down on spammers harvesting the email address from the webpage,
    displays the email address with [aT] instead of @.

    Example: Given the email address: lbrandon@wharton.upenn.edu
    Generates the email link: <a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>

    Note: If, for some reason the email address does not contain @,
    use the email address as is and don't replace anything.
    """
    formatted_email = []

    #if using '@', generate format of xxx[aT]xxx and return 
    if '@' in email_address:
        formatted_email = email_address.split('@')
        return '<a href="mailto:' + email_address + '">' + formatted_email[0] + '[aT]' + formatted_email[1] + '</a>'

    #if using 'at', generate format of xxx.at.xxx
    elif 'at' in email_address:
        return '<a href="mailto:' + email_address + '">' + email_address + '</a>'


def copy_file(file_from, file_to):
    """
    This function copy the content from 'from file' to the 'to file'
    """

    #open two files, one in read mode, one if write mode
    f1 = open(file_from, 'r')
    f2 = open(file_to,'w')

    #read from f1 and write those to f2
    content = f1.readlines()
    f2.writelines(content)

    #close two files
    f1.close()
    f2.close()


def generate_html(txt_input_file, html_output_file):
    """
    Loads given txt_input_file,
    gets the name, email address, list of projects, and list of courses,
    then writes the info to the given html_output_file.

    # call function(s) to write the name, email address, list of projects, and list of courses to the given html_output_file
    """
    #load the file and extract information
    content = load_resume(txt_input_file)   
    name = detect_name(content[0])
    email = detect_email(content)
    courses = detect_course(content)
    projects = detect_project(content)

    #copy the header from the template to new html file
    copy_file('resume_template.html', html_output_file)

    #create html output file in append mode
    with open(html_output_file, 'a') as file:
        
        #add wrapper 
        file.write("<div id='page-wrap'>\n")

        #add name and email

        #if not have valid email ,print empty 
        file.write('<div>\n')
        file.write(surround_block('h1', name)) 
        file.write('\n')
        if email:
            file.write(surround_block('p', 'Email:' + create_email_link(email))) #make email block as paragraph by surrounding it with <p>
        else:
            file.write(surround_block('p', 'Email:'))
        file.write('\n')
        file.write('</div>\n')

        #add projects

        #skip the empty line
        file.write('<div>\n') 
        file.write(surround_block('h2', 'Projects')) #header 
        file.write('\n')
        file.write('<ul>\n') #unordered list starts
        for project in projects:
            if project: 
                file.write(surround_block('li', project[:-1]))  #make each project (remove '\n') as an list element by surrounding it with <li>
                file.write('\n')
        file.write('</ul>\n')#unordered list ends
        file.write('</div>\n') 

        #add courses with ','
        file.write('<div>\n')
        file.write(surround_block('h3', 'Courses'))
        file.write('\n')
        file.write(surround_block('span', ', '.join(courses)))
        file.write('\n')
        file.write('</div>\n')

        #add html close tag
        file.write('</div>\n') #end wrapper 
        file.write('</body>\n') #end body
        file.write('</html>\n') #end html file


def main():

    #global html template file so it can be read at other function

    # DO NOT REMOVE OR UPDATE THIS CODE
    # generate resume.html file from provided sample resume.txt
    #generate_html('resume.txt', 'resume.html')

    # DO NOT REMOVE OR UPDATE THIS CODE.
    # Uncomment each call to the generate_html function when you’re ready
    # to test how your program handles each additional test resume.txt file
    #generate_html('TestResumes/resume_bad_name_lowercase/resume.txt', 'TestResumes/resume_bad_name_lowercase/resume.html')
    #generate_html('TestResumes/resume_courses_w_whitespace/resume.txt', 'TestResumes/resume_courses_w_whitespace/resume.html')
    #generate_html('TestResumes/resume_courses_weird_punc/resume.txt', 'TestResumes/resume_courses_weird_punc/resume.html')
    #generate_html('TestResumes/resume_projects_w_whitespace/resume.txt', 'TestResumes/resume_projects_w_whitespace/resume.html')
    #generate_html('TestResumes/resume_projects_with_blanks/resume.txt', 'TestResumes/resume_projects_with_blanks/resume.html')
    #generate_html('TestResumes/resume_template_email_w_whitespace/resume.txt', 'TestResumes/resume_template_email_w_whitespace/resume.html')
    generate_html('TestResumes/resume_wrong_email/resume.txt', 'TestResumes/resume_wrong_email/resume.html')

    # If you want to test additional resume files, call the generate_html function with the given .txt file
    # and desired name of output .html file

if __name__ == '__main__':
    main()