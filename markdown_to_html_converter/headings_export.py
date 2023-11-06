from search_and_replace import find_occurances_of

folder_path = "D:\\Computational Design Book\\section_html_pages\\"
out_folder_path = "D:\\Computational Design Book\\section_heading_lists\\"

documents = [
    "System Basics\\Rhino UI Basics.html",
    "Essential Mathematics for CAD Designers.html",
    "System Basics\\Introduction to Rhino.html",
    "System Basics\\The Non-Uniform-Rational-Basis-Spline.html",
    "System Basics\\Modeling in Rhino.html",
    "Preface.html"
]

in_path = folder_path + documents[1]
out_path = out_folder_path + documents[1][0 : len(documents[2]) - 3] + ".txt"

# Extracts the tags and titles and returns a list
def extract_headings(document):
    # assuming the previous step worked as expected, these two lists should be parallel
    heading_open_tags = find_occurances_of("<h", document)
    heading_close_tags = find_occurances_of("</h", document)
    hr_tags = find_occurances_of("<hr>", document)

    for tag in hr_tags:
        if(tag in heading_open_tags):
            heading_open_tags.remove(tag)

    print(heading_open_tags)
    print(heading_close_tags)
    tag_list = []
    for x in range(len(heading_open_tags)):
        heading_number = document[heading_open_tags[x] + 2]
        heading_text = document[heading_open_tags[x] + 4 : heading_close_tags[x]]
        # print(heading_number)
        # print(heading_text)
        tag_list.append((heading_number, heading_text))
    
    return tag_list


def convert_list_to_string(delimeter, data):
    data_string = ""
    for item in data:
        data_string += (item[0] + delimeter)
        data_string += (item[1] + delimeter)
    data_string = data_string[0 : len(data_string) - 1]
    return data_string

file_in = open(in_path, 'r')
file_out = open(out_path, 'w')
raw_file_contents = file_in.read()
# print(raw_file_contents)

headings_list = extract_headings(raw_file_contents)
# print(headings_list)
stringified_list = convert_list_to_string(",", headings_list)
stringified_list = "," + stringified_list

# print(stringified_list)

file_out.write(stringified_list)